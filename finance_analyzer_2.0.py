
import os
import argparse
import subprocess
import csv
import pandas as pd
from senitment_tracker import fetch_yahoo_news, analyze_sentiment


from report_generator import generate_pdf_report  # New PDF report function

# CLI Argument Parsing
parser = argparse.ArgumentParser(description="Full Financial Analysis Pipeline")
parser.add_argument("--tickers", type=str, required=True, help="Path to the CSV file with tickers & URLs")
parser.add_argument("--data-dir", type=str, required=True, help="Path to the output directory for financial data")
parser.add_argument("--report-dir", type=str, required=True, help="Path to save PDF reports")
args = parser.parse_args()

# Run the Web Scraper
print(f"📡 Running web scraper using ticker CSV: {args.tickers}...")
scraper_cmd = ["python", "C:/Users/ccape/Downloads/Company_value_pipeline/Finance_data_scaper_version_3.0.py", "--tickers", args.tickers]

result = subprocess.run(scraper_cmd)

if result.returncode != 0:
    print("❌ Scraper encountered an error. Exiting pipeline.")
    exit(1)
print("✅ Web scraping completed successfully.")

# Extract tickers from the CSV
tickers = []
with open(args.tickers, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    tickers = [row["ticker"].strip().upper() for row in reader if "ticker" in row]

if not tickers:
    print("❌ No valid tickers found in CSV. Exiting pipeline.")
    exit(1)

ticker_str = ",".join(tickers)

# Run the Stock Picker
print(f"📊 Running stock picker with tickers: {ticker_str}...")
stock_picker_cmd = ["python", "stock_picker.py", "--data-dir", args.data_dir, "--tickers", ticker_str]
result = subprocess.run(stock_picker_cmd)

if result.returncode != 0:
    print("❌ Stock picker encountered an error. Exiting pipeline.")
    exit(1)
print("✅ Stock picker completed successfully.")

# Run the Plot Generator (Trend Analysis)
print(f"📊 Running trend plots for tickers: {ticker_str}...")
plot_cmd = ["python", "plot_trends.py", "--data-dir", args.data_dir, "--tickers", ticker_str]
result = subprocess.run(plot_cmd)

if result.returncode != 0:
    print("❌ Plot generator encountered an error. Exiting pipeline.")
    exit(1)
print("✅ Trend plots generated successfully.")

# Run Sentiment Analysis
print(f"📰 Fetching news & analyzing sentiment for tickers: {ticker_str}...")
sentiment_data = {}

for ticker in tickers:
    headlines = fetch_yahoo_news(ticker)
    sentiment_results, sentiment_count = analyze_sentiment(headlines)
    sentiment_data[ticker] = {
        "sentiment_results": sentiment_results,
        "sentiment_summary": sentiment_count
    }

print("✅ Sentiment analysis completed.")

# Generate Final PDF Report
print(f"📄 Generating final financial reports for tickers: {ticker_str}...")
for ticker in tickers:
    generate_pdf_report(ticker, args.data_dir, args.report_dir, sentiment_data[ticker])

print("\n🎉 Full pipeline executed successfully! Reports saved in:", args.report_dir)
