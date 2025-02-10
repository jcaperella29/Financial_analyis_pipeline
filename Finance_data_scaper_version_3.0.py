import csv
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

# 🏗️ Add CLI argument parsing
parser = argparse.ArgumentParser(description="Stock Analysis Data Scraper")
parser.add_argument("--tickers", type=str, required=True, help="Path to the CSV file with tickers & URLs")
parser.add_argument("--data-dir", type=str, default="financial_data", help="Path to store scraped financial data")
args = parser.parse_args()

# 📂 Set input and output directories
INPUT_FILE = args.tickers
OUTPUT_DIR = args.data_dir
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists

print(f"📄 Using ticker file: {INPUT_FILE}")
print(f"💾 Saving scraped data to: {OUTPUT_DIR}")

# 🔧 CONFIGURATION
GECKODRIVER_PATH = r"C:\Users\ccape\Downloads\geckodriver-v0.35.0-win32\geckodriver.exe"
FIREFOX_BINARY_PATH = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# Define financial tabs
TABS = {
    "Balance Sheet": "//a[contains(text(), 'Balance Sheet')]",
    "Cash Flow": "//a[contains(text(), 'Cash Flow')]",
    "Ratios": "//a[contains(text(), 'Ratios')]"
}

# Function to initialize WebDriver
def init_driver():
    options = Options()
    options.binary_location = FIREFOX_BINARY_PATH
    service = Service(GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    return driver

# Function to extract table data
def extract_table(driver, ticker, tab_name, output_dir):
    """Extracts financial table data and saves it as a CSV."""
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@data-test='financials']"))
        )
        print(f"✅ Table found for {ticker} - {tab_name}")

        # Extract rows
        rows = table.find_elements(By.XPATH, ".//tr")
        table_data = []
        for row in rows:
            cells = row.find_elements(By.XPATH, ".//th | .//td")
            table_data.append([cell.text for cell in cells])

        # Convert to DataFrame
        df = pd.DataFrame(table_data[1:], columns=table_data[0])

        # Save as CSV
        filename = os.path.join(output_dir, f"{ticker}_{tab_name.replace(' ', '_').lower()}.csv")
        df.to_csv(filename, index=False)
        print(f"💾 Saved: {filename}")

    except Exception as e:
        print(f"❌ Failed to extract table for {ticker} - {tab_name}. Error: {e}")

# Function to scrape a company's financials (🔥 Re-added!)
def scrape_financials(driver, url, ticker):
    """Scrapes financial tables for a given company."""
    print(f"\n🌐 Scraping: {ticker} ({url})")
    driver.get(url)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print(f"✅ Page loaded for {ticker}")

    # Income Statement (default)
    extract_table(driver, ticker, "income_statement", OUTPUT_DIR)

    # Loop through tabs
    for tab_name, tab_xpath in TABS.items():
        print(f"📊 Navigating to {tab_name} for {ticker}...")
        try:
            tab_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, tab_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", tab_element)
            time.sleep(1)

            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, tab_xpath))).click()
            print(f"✅ Clicked on {tab_name}")

        except Exception as e:
            print(f"⚠️ Click failed for {tab_name}. Trying JavaScript click...")
            try:
                driver.execute_script("arguments[0].click();", tab_element)
                print(f"✅ JavaScript click successful for {tab_name}")
            except Exception as js_error:
                print(f"❌ JavaScript click failed. Skipping {tab_name}. Error: {js_error}")
                continue

        time.sleep(2)
        extract_table(driver, ticker, tab_name, OUTPUT_DIR)

# Function to read tickers from CSV
def load_tickers_from_csv(filename):
    """Reads ticker symbols and URLs from a CSV file."""
    companies = {}
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found! Please create a CSV with tickers and URLs.")
        return {}

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ticker = row.get("ticker", "").strip().upper()
            url = row.get("url", "").strip()
            if ticker and url:
                companies[ticker] = url
            else:
                print(f"⚠️ Skipping invalid entry: {row}")

    return companies

# Main function
def main():
    """Runs the scraper for multiple stock financial pages."""
    companies = load_tickers_from_csv(INPUT_FILE)
    
    if not companies:
        print("❌ No valid tickers to process. Exiting...")
        return

    driver = init_driver()

    try:
        for ticker, url in companies.items():
            scrape_financials(driver, url, ticker)
    finally:
        driver.quit()
        print("\n🚪 Browser closed. All scraping completed!")

# Run the script
if __name__ == "__main__":
    main()
