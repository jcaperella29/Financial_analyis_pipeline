# 📊 Financial Analysis Pipeline 🚀

This project is a **Python-based financial data scraper and stock classifier** that:  
✅ Scrapes financial data from **StockAnalysis**  
✅ Processes company financials  
✅ Classifies stocks using **Piotroski F-Score & Valuation**  

## 🔧 Features  
- **📡 Web Scraper**: Uses Selenium to extract stock financials  
- **📊 Stock Analysis**: Computes Piotroski F-Score & Valuation  
- **📂 Full Pipeline**: Automates scraping & analysis in one command  

---

## 🚀 How to Use

### **1️⃣ Install Dependencies**  
Make sure you have **Python 3+** installed, then install the required libraries:  

```bash
pip install pandas selenium
2️⃣ Run the Full Pipeline
Use the following command to scrape data and analyze stocks in one step:

bash
Copy
Edit
python finance_analyzer.py --tickers ticker.csv --data-dir financial_data
📌 Arguments:

--tickers → Path to CSV with stock tickers & URLs
--data-dir → Directory to store scraped financial data
3️⃣ View Results
After execution, check financial_classification_results.csv for the stock classification results.

📂 Generated Files:

financial_data/ → Contains scraped financial reports
financial_classification_results.csv → Final stock analysis
🛠 Configuration
Scraper: Uses Selenium & GeckoDriver
Stock Picker: Reads scraped financials, applies scoring
CLI Interface: Works with command-line arguments
📜 License
MIT License. Free to use and modify.

⭐ Contributing
Want to improve the project? Feel free to fork, submit issues, or contribute!

