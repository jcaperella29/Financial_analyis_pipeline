from fpdf import FPDF
import os
import pandas as pd
import numpy as np
from scipy.stats import linregress  # For trend analysis

def analyze_trend_with_regression(trend_data):
    """
    Analyze trends using linear regression and return the numerical slope.
    """
    if len(trend_data) < 2:
        return None  # Return None instead of a string

    x = np.arange(len(trend_data))  # Time points (0, 1, 2, ..., n)
    y = np.array(trend_data)  # Actual data points

    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    return slope  # ✅ Return only the numerical slope

def analyze_multiple_valuation_trends(valuation_data):
    """
    Compute the average numerical slope from multiple valuation metrics.
    """
    slopes = []
    
    for metric, values in valuation_data.items():
        # ✅ Convert values to numeric and remove invalid values
        values = pd.to_numeric(values, errors="coerce")  # Convert strings to numbers, NaN if invalid
        values = values[~np.isnan(values)]  # Remove NaN values

        if len(values) >= 2:  # Ensure enough points for regression
            slope = analyze_trend_with_regression(values)
            if slope is not None:  # ✅ Ensure we only store numerical values
                slopes.append(slope)
                print(f"✅ {metric} Slope: {slope}")  # Debugging Output
    
    if not slopes:
        return "insufficient data"

    avg_slope = np.mean(slopes)  # ✅ Compute the average of numerical slopes

    # ✅ Now we determine if it's increasing or decreasing based on the average slope
    if avg_slope > 0:
        return "increasing"
    elif avg_slope < 0:
        return "decreasing"
    else:
        return "stable"


def compute_f1_score(df):
    """
    Computes F1 Score the same way as stock_picker.py, but for all rows.
    """
    if df is None or df.empty:
        return None

    f1_scores = []

    for i in range(1, len(df)):  # Start from index 1 to compare with previous year
        f1 = 0

        # ✅ Return on Assets (ROA) should increase
        if df.iloc[i]["Return on Assets (ROA)"] > df.iloc[i - 1]["Return on Assets (ROA)"]:
            f1 += 1

        # ✅ Current Ratio should increase
        if df.iloc[i]["Current Ratio"] > df.iloc[i - 1]["Current Ratio"]:
            f1 += 1

        # ✅ Debt/Equity Ratio should decrease
        if df.iloc[i]["Debt / Equity Ratio"] < df.iloc[i - 1]["Debt / Equity Ratio"]:
            f1 += 1

        # ✅ Asset Turnover should increase
        if df.iloc[i]["Asset Turnover"] > df.iloc[i - 1]["Asset Turnover"]:
            f1 += 1

        # ✅ Additional financial metrics
        if "Operating Cash Flow" in df.columns and df.iloc[i]["Operating Cash Flow"] > df.iloc[i - 1]["Operating Cash Flow"]:
            f1 += 1

        if "Net Income" in df.columns and df.iloc[i]["Net Income"] > df.iloc[i - 1]["Net Income"]:
            f1 += 1

        if "Total Common Shares Outstanding" in df.columns and df.iloc[i]["Total Common Shares Outstanding"] < df.iloc[i - 1]["Total Common Shares Outstanding"]:
            f1 += 1  # Lower shares outstanding is better

        if "Gross Margin" in df.columns and df.iloc[i]["Gross Margin"] > df.iloc[i - 1]["Gross Margin"]:
            f1 += 1

        f1_scores.append(f1)  # Store F1 score for this row

    return f1_scores
def generate_pdf_report(ticker, data_dir, report_dir, sentiment_data):
    """
    Generate a financial report PDF summarizing stock classification, trends, and sentiment.
    """
    # Ensure we look in the correct trend data directory
    trend_data_dir = os.path.join(data_dir, "trend_data")
    
    # ✅ Define paths correctly
    valuation_path = os.path.join(trend_data_dir, f"{ticker}_valuation_trend.csv")
    f1_score_path = os.path.join(trend_data_dir, f"{ticker}_f1_trend.csv")

    # 📄 DEBUGGING: Print paths to check if they exist
    print(f"🔍 Checking valuation trend file: {valuation_path}")
    print(f"🔍 Checking F1 Score trend file: {f1_score_path}")

    # Load F1 Score trend data
    if os.path.exists(f1_score_path):
        f1_df = pd.read_csv(f1_score_path)
        if not f1_df.empty:
            f1_scores = compute_f1_score(f1_df)  # Compute F1 Score for all years
            if f1_scores:
                f1_trend_status = analyze_trend_with_regression(f1_scores)
            else:
                f1_trend_status = "insufficient data"
        else:
            f1_trend_status = "insufficient data"
    else:
        print(f"⚠️ Missing F1 Score file: {f1_score_path}")
        f1_trend_status = "insufficient data"

    # Load Valuation trend data
    if os.path.exists(valuation_path):
        valuation_df = pd.read_csv(valuation_path)
        print(f"📄 Loaded valuation data for {ticker}:\n{valuation_df.head()}")  # Debugging

        valuation_metrics = ["PE Ratio", "PB Ratio", "P/FCF Ratio", "PEG Ratio", "EV/EBITDA Ratio"]
        valuation_data = {}

        for metric in valuation_metrics:
            if metric in valuation_df.columns:
                values = valuation_df[metric].dropna().astype(str)  # Convert to string temporarily
                print(f"🔍 {metric} Raw Values: {values.tolist()}")  # Debugging Output

                values = pd.to_numeric(values, errors="coerce")  # Convert to numeric
                print(f"✅ {metric} Numeric Values: {values.dropna().tolist()}")  # Debugging Output

                valuation_data[metric] = values.dropna().values

        if valuation_data:
            valuation_trend_status = analyze_multiple_valuation_trends(valuation_data)
        else:
            print(f"⚠️ No valid valuation metrics found for {ticker}.")
            valuation_trend_status = "insufficient data"
    else:
        print(f"⚠️ Missing Valuation trend file: {valuation_path}")
        valuation_trend_status = "insufficient data"


    # Sentiment Summary
    sentiment_summary = sentiment_data["sentiment_summary"]
    most_common_sentiment = max(sentiment_summary, key=sentiment_summary.get)

    # Final Score System
    score = 0
    if f1_trend_status == "increasing":
        score += 1
    if valuation_trend_status == "decreasing":  # We want valuation to decrease for a good buy
        score += 1
    if most_common_sentiment == "POSITIVE":
        score += 1

    # Score Interpretation
    score_interpretation = {
        0: "Very Weak Stock",
        1: "Weak Stock",
        2: "Moderate Stock",
        3: "Good Investment Potential"
    }
    recommendation = score_interpretation.get(score, "Unknown")

    # Create PDF Report
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Title
    pdf.cell(200, 10, f"Financial Report for {ticker}", ln=True, align="C")
    pdf.ln(10)

    # Trend Analysis
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Trend Analysis", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"F1 Score Trend: {f1_trend_status}", ln=True)
    pdf.cell(200, 10, f"Valuation Trend: {valuation_trend_status}", ln=True)
    pdf.ln(10)

    # Sentiment Analysis
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Sentiment Analysis", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Most Common Sentiment: {most_common_sentiment}", ln=True)
    pdf.ln(10)

    # Final Verdict & Score
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, f"Final Score: {score} / 3", ln=True)
    pdf.cell(200, 10, f"Verdict: {recommendation}", ln=True)

    # Save PDF
    os.makedirs(report_dir, exist_ok=True)
    pdf_path = os.path.join(report_dir, f"{ticker}_financial_report.pdf")
    pdf.output(pdf_path)

    print(f"✅ PDF Report Generated: {pdf_path}")
