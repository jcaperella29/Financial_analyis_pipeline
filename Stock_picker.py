import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# CLI Argument Parsing
parser = argparse.ArgumentParser(description="Plot F-Score & Valuation Trends")
parser.add_argument("--data-dir", type=str, required=True, help="Path to the scraped financial data directory")
parser.add_argument("--tickers", type=str, required=True, help="Comma-separated tickers to analyze")
args = parser.parse_args()

# Create directories for saving plots & CSV data
f_score_plot_dir = os.path.join(args.data_dir, "f_score_trends")
valuation_plot_dir = os.path.join(args.data_dir, "valuation_trends")
trend_data_dir = os.path.join(args.data_dir, "trend_data")  # New directory for trend CSVs

os.makedirs(f_score_plot_dir, exist_ok=True)
os.makedirs(valuation_plot_dir, exist_ok=True)
os.makedirs(trend_data_dir, exist_ok=True)

# ✅ Use the exact column names from `stock_picker.py`
F_SCORE_METRICS = [
    "Return on Assets (ROA)", "Operating Cash Flow", "Net Income",
    "Current Ratio", "Debt / Equity Ratio", "Total Common Shares Outstanding",
    "Gross Margin", "Asset Turnover"
]

VALUATION_METRICS = ["PE Ratio", "PB Ratio", "P/FCF Ratio", "PEG Ratio", "EV/EBITDA Ratio"]

def load_and_transform_data(ticker, metric_list, metric_type):
    """
    Loads financial data and extracts yearly data for the given metrics.
    """
    file_path = f"{args.data_dir}/{ticker}_ratios.csv"

    if not os.path.exists(file_path):
        print(f"❌ Missing data file: {file_path}. Skipping {ticker}.")
        return None

    df = pd.read_csv(file_path)

    # ✅ Ensure the first column is treated as the index (i.e., financial metric names)
    df.set_index(df.columns[0], inplace=True)

    # ✅ Transpose: Now rows are years and columns are metrics
    df = df.T

    # ✅ Check if requested metrics exist in the data
    available_metrics = [metric for metric in metric_list if metric in df.columns]

    if not available_metrics:
        print(f"⚠️ No valid {metric_type} metrics found for {ticker}. Skipping...")
        return None

    # ✅ Extract only the available metrics
    df_filtered = df[available_metrics].dropna(how="all")

    return df_filtered

def save_trend_data(ticker, metric_type, data):
    """
    Saves extracted trend data as a CSV file for report generation.
    """
    if data is None:
        return

    save_path = os.path.join(trend_data_dir, f"{ticker}_{metric_type}_trend.csv")
    data.to_csv(save_path, index=True)  # Index = Years
    print(f"💾 Saved {metric_type} trend data: {save_path}")

def plot_trend(data, ticker, metric_type, save_dir):
    """
    Creates a scatter plot of metric trends over years.
    """
    if data is None:
        return

    plt.figure(figsize=(10, 6))
    
    for column in data.columns:
        plt.scatter(data.index, data[column], label=column, alpha=0.7)
        plt.plot(data.index, data[column], marker="o", linestyle="-")

    plt.xlabel("Year")
    plt.ylabel(f"{metric_type} Score")
    plt.title(f"{metric_type} Trends for {ticker}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()

    save_path = os.path.join(save_dir, f"{ticker}.png")
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"📊 Saved plot: {save_path}")

# Process each ticker
tickers = args.tickers.split(",")

for ticker in tickers:
    print(f"📈 Processing {ticker} for F-Score & Valuation trends...")

    # Load, save, and plot F-Score trends
    f_score_data = load_and_transform_data(ticker, F_SCORE_METRICS, "F-Score")
    save_trend_data(ticker, "F1_Score", f_score_data)  # Save for report generation
    plot_trend(f_score_data, ticker, "F-Score", f_score_plot_dir)

    # Load, save, and plot Valuation trends
    valuation_data = load_and_transform_data(ticker, VALUATION_METRICS, "Valuation")
    save_trend_data(ticker, "Valuation", valuation_data)  # Save for report generation
    plot_trend(valuation_data, ticker, "Valuation", valuation_plot_dir)

print("✅ Trend plotting completed!")

