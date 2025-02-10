

md
Copy
Edit
# 📊 Financial Analysis Pipeline  
A **rule-based AI** financial analysis pipeline that scrapes stock data, calculates **Piotroski F-Score** & **Stock Valuation**, and generates trend plots.  

## 🚀 Features  
✔ **Automated Financial Data Scraping** via Selenium  
✔ **Piotroski F-Score Calculation** (average over historical data)  
✔ **Stock Valuation Calculation** (using current year data)  
✔ **Classification System**: Categorizes stocks as `Strong`, `Medium`, or `Weak`  
✔ **Trend Plots**: Generates **F-Score & Valuation** trends over time  
✔ **One-Click CLI Execution**  

## 📂 File Structure  
Financial_analyis_pipeline/ │── finance_analyzer_2.0.py # 🚀 Main pipeline script
│── Finance_data_scraper.py # 📡 Web scraper for stock data
│── stock_picker.py # 📊 Financial metric calculations
│── plot_trends.py # 📈 Generates F-Score & Valuation trend plots
│── ticker.csv # 🏷️ Input file with stock tickers & URLs
│── financial_data/ # 💾 Stores scraped data & results
│ ├── financial_classification_results.csv # Final stock classifications
│ ├── f_score_trends/ # F-Score trend plots
│ ├── valuation_trends/ # Valuation trend plots

bash
Copy
Edit

## 🔧 Installation  
1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/jcaperella29/Financial_analyis_pipeline.git  
cd Financial_analyis_pipeline
2️⃣ Install Dependencies

sh
Copy
Edit
pip install -r requirements.txt
3️⃣ Setup Selenium WebDriver

Download Geckodriver
Update GECKODRIVER_PATH & FIREFOX_BINARY_PATH in Finance_data_scraper.py
⚡ Usage
Run Full Pipeline


python finance_analyzer_2.0.py --tickers ticker.csv --data-dir financial_data
Scrapes stock financials
Computes F-Score & Stock Valuation
Generates trend plots
Outputs classification results


python finance_analyzer_2.0.py --tickers ticker.csv --data-dir financial_data --skip-scraper
📊 Example Output
Final Classification (financial_classification_results.csv)
Ticker	Piotroski_F	Stock_Valuation	Classification
AAPL	6.3	24.1	Medium
GM	5.8	9.2	Strong
TSLA	3.7	32.5	Weak
Generated Trend Plots
📈 F-Score Trend (Years vs. F-Score)
📊 Valuation Trend (Years vs. Valuation Score)
Saved in:


financial_data/f_score_trends/
financial_data/valuation_trends/
(Each ticker has its own .png file showing the trend over the years.)

🛠️ Roadmap
🔹 Improve classification logic 📈
🔹 Support more valuation metrics 💰
🔹 Add interactive visualization 📊

🤝 Contributing
Fork the repo & create a new branch
Make changes & commit
Submit a Pull Request
⚖️ License
MIT License

