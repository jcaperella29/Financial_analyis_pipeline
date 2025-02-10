import os
import subprocess
import argparse
import csv

# CLI argument parsing
parser = argparse.ArgumentParser(description="Finance Analyzer: Full financial data pipeline.")
parser.add_argument(
    "--tickers", 
    type=str, 
    required=True, 
    help="Path to the ticker CSV file (e.g., 'tickers.csv')."
)
parser.add_argument(
    "--data-dir", 
    type=str, 
    default="financial_data", 
    help="Path where the scraped financial data will be saved (default: 'financial_data')."
)
args = parser.parse_args()

# Paths to scripts
scraper_script = r"C:\Users\ccape\Downloads\Company_value_pipeline\Finance_data_scaper_version_3.0.py"
stock_picker_script = r"C:\Users\ccape\Downloads\Company_value_pipeline\stock_picker.py"

# Create the output directory if it doesn't exist
os.makedirs(args.data_dir, exist_ok=True)

# Run the web scraper
print(f"📡 Running web scraper using ticker CSV: {args.tickers}...")
try:
    subprocess.run(
        ["python", scraper_script, "--tickers", args.tickers, "--data-dir", args.data_dir],
        check=True
    )
    print("✅ Web scraping completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"❌ Scraper encountered an error:\n{e}")
    exit(1)

# Extract tickers from the CSV
print("🔍 Extracting tickers from the CSV...")
def extract_tickers(ticker_file):
    tickers = []
    with open(ticker_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tickers.append(row["ticker"])  # Extract ticker column
    return ",".join(tickers)

tickers_arg = extract_tickers(args.tickers)

# Run the stock picker with the scraper's output directory
print(f"📊 Running stock picker with tickers: {tickers_arg}...")
try:
    subprocess.run(
        ["python", stock_picker_script, "--data-dir", args.data_dir, "--tickers", tickers_arg],
        check=True
    )
    print("✅ Stock picker completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"❌ Stock picker encountered an error:\n{e}")
    exit(1)

print("\n🎉 Full pipeline executed successfully!")
