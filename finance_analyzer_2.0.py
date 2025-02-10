import os
import argparse
import subprocess

# CLI Argument Parsing
parser = argparse.ArgumentParser(description="Full Financial Analysis Pipeline")
parser.add_argument("--tickers", type=str, required=True, help="Path to the CSV file with tickers & URLs")
parser.add_argument("--data-dir", type=str, required=True, help="Path to the output directory for financial data")
args = parser.parse_args()

# Run the Web Scraper
print(f"📡 Running web scraper using ticker CSV: {args.tickers}...")
scraper_cmd = ["python", "Finance_data_scaper_version_3.0.py", "--tickers", args.tickers]
result = subprocess.run(scraper_cmd)

if result.returncode != 0:
    print("❌ Scraper encountered an error. Exiting pipeline.")
    exit(1)
print("✅ Web scraping completed successfully.")

# Extract tickers from the CSV
import csv

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

# Run the Plot Generator
print(f"📊 Running trend plots for tickers: {ticker_str}...")
plot_cmd = ["python", "plot_trends.py", "--data-dir", args.data_dir, "--tickers", ticker_str]
result = subprocess.run(plot_cmd)

if result.returncode != 0:
    print("❌ Plot generator encountered an error. Exiting pipeline.")
    exit(1)
print("✅ Trend plots generated successfully.")

print("\n🎉 Full pipeline executed successfully!")
