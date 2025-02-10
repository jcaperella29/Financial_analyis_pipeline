import os
import argparse
import pandas as pd

# Parse CLI arguments
parser = argparse.ArgumentParser(description="Stock Picker: Analyze and classify financial data.")
parser.add_argument(
    "--data-dir", 
    type=str, 
    required=True, 
    help="Path to the directory containing financial data CSV files."
)
parser.add_argument(
    "--tickers", 
    type=str, 
    required=True, 
    help="Comma-separated list of tickers to process (e.g., 'GM,TSLA,AAPL')."
)
args = parser.parse_args()

# Set directory path and tickers
data_dir = args.data_dir
tickers = args.tickers.split(",")  # Convert comma-separated string into a list

# Function to load and merge financial data for a ticker
def load_ticker_data(ticker):
    """Loads and merges financial data CSVs for a given ticker."""
    files = {
        "ratios": f"{data_dir}/{ticker}_ratios.csv",
        "cash_flow": f"{data_dir}/{ticker}_cash_flow.csv",
        "balance_sheet": f"{data_dir}/{ticker}_balance_sheet.csv",
        "income_statement": f"{data_dir}/{ticker}_income_statement.csv",
    }
    
    dataframes = {}
    for key, file_path in files.items():
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            df = pd.read_csv(file_path)
            df["Ticker"] = ticker  # Add ticker column
            dataframes[key] = df
        else:
            print(f"Warning: Missing or empty file for {ticker}: {file_path}")

    if dataframes:
        merged_df = pd.concat(dataframes.values(), axis=0, ignore_index=True)  # Stack yearly data
        return merged_df
    return None

# Reshape Data
def reshape_data(df, ticker):
    """Converts 'Fiscal Year' row values into column headers and ensures the Ticker column is aligned."""
    df = df.set_index("Fiscal Year").T  # Transpose the dataset
    df = df.rename_axis("Date").reset_index()  # Reset index
    df["Ticker"] = ticker  # Add the ticker column to every row
    df = df.loc[:, ~df.columns.duplicated()]  # Remove duplicate columns
    return df

# Load and reshape data for all tickers
all_ticker_data = []
for ticker in tickers:
    raw_data = load_ticker_data(ticker)
    if raw_data is not None:
        reshaped_data = reshape_data(raw_data, ticker)
        all_ticker_data.append(reshaped_data)

if all_ticker_data:
    all_tickers_df = pd.concat(all_ticker_data, ignore_index=True)
else:
    print("Error: No valid financial data found. Check your CSV files.")
    exit()

# Debugging: Print available columns
print("Available Columns in DataFrame:", all_tickers_df.columns.tolist())

# Ensure numeric conversion
def ensure_numeric(df, columns):
    """Converts specified columns to numeric, handling errors."""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)  # Convert invalid values to NaN, then fill with 0
    return df

# Compute Financial Health Metrics
def compute_financial_metrics(df):
    metrics = {}

    # Compute Piotroski F-Score (average across all years)
    try:
        f_score_cols = [
            "Return on Assets (ROA)", "Operating Cash Flow", "Net Income",
            "Current Ratio", "Debt / Equity Ratio", "Total Common Shares Outstanding",
            "Gross Margin", "Asset Turnover"
        ]

        # Ensure numeric conversion for F-Score columns
        df = ensure_numeric(df, f_score_cols)

        # Apply F-Score calculation
        metrics["Piotroski_F"] = (df[f_score_cols] > 0).sum(axis=1)
    except Exception as e:
        print(f"Error in Piotroski F-Score calculation: {e}")
        metrics["Piotroski_F"] = None

    # Compute Stock Valuation (based on current valuation metrics)
    try:
        # Select the ratios table and extract the first (current year) column for valuation
        valuation_cols = [
            "PE Ratio", "PB Ratio", "P/FCF Ratio", "PEG Ratio", "EV/EBITDA Ratio"
        ]

        # Ensure numeric conversion for all relevant valuation metrics
        recent_data = ensure_numeric(df, valuation_cols)

        # Check the first column of the ratios table
        metrics["Stock_Valuation"] = recent_data[valuation_cols].iloc[0].mean()
    except Exception as e:
        print(f"Error in Stock Valuation calculation: {e}")
        metrics["Stock_Valuation"] = 0

    return pd.DataFrame(metrics)

# Apply metrics calculation
all_tickers_metrics = compute_financial_metrics(all_tickers_df)

# Concatenate metrics with the original DataFrame
all_tickers_df = pd.concat([all_tickers_df, all_tickers_metrics], axis=1)

# Group data by ticker to calculate averages for Piotroski F-Score
average_f_scores = all_tickers_df.groupby("Ticker", as_index=False)["Piotroski_F"].mean()

# Keep only Stock Valuation for the most recent year
recent_valuations = all_tickers_df.sort_values("Date").drop_duplicates(subset="Ticker", keep="last")[["Ticker", "Stock_Valuation"]]

# Merge the averaged F-Score and recent valuation
aggregated_df = pd.merge(average_f_scores, recent_valuations, on="Ticker")

# Classification
def classify_company(row):
    f_score = row.get("Piotroski_F", None)
    valuation = row.get("Stock_Valuation", None)

    if pd.isnull(f_score) or pd.isnull(valuation):
        return "Unknown"  # Assign "Unknown" if any score is missing
    elif f_score >= 7 and valuation < 20:
        return "Strong"
    elif f_score >= 4 and valuation < 30:
        return "Medium"
    else:
        return "Weak"

# Apply classification
aggregated_df["Classification"] = aggregated_df.apply(classify_company, axis=1)

# Save results
output_file = os.path.join(data_dir, "financial_classification_results.csv")
aggregated_df.to_csv(output_file, index=False)

print(f"Classification results saved to {output_file}")
