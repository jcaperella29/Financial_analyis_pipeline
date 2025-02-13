# 📊 Company Value Pipeline  

A financial data pipeline that scrapes company financials, evaluates stock strength, analyzes sentiment, and generates reports.  

## 🚀 Features  
✅ **Web Scraper** – Fetches financial data from stockanalysis.com  
✅ **Stock Picker** – Calculates Piotroski F-Score & stock valuation  
✅ **Trend Analysis** – Uses regression to detect stock performance trends  
✅ **Sentiment Analysis** – Extracts news & determines sentiment  
✅ **Report Generator** – Produces PDFs summarizing all findings  

---

## 🛠️ **Installation**  
1. **Clone the repository**  
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Company_value_pipeline.git
cd Company_value_pipeline
Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔥 How to Run the Pipeline
To analyze financial data, run:

bash
Copy
Edit
python finance_analyzer_3.0.py --tickers tickers.csv --data-dir financial_data --report-dir reports
This will:
📡 Scrape financial data
📊 Evaluate stocks
📈 Analyze trends (F1 Score & valuation)
📰 Perform sentiment analysis
📄 Generate PDF reports

📂 File Structure
graphql
Copy
Edit
Company_value_pipeline/
│── finance_analyzer_3.0.py      # Main pipeline script  
│── Finance_data_scraper.py      # Scrapes financial data  
│── stock_picker.py              # Calculates stock scores  
│── plot_trends.py               # Generates trend plots & saves data  
│── sentiment_tracker.py         # Fetches & analyzes stock news  
│── report_generator.py          # Generates final reports  
│── data/                        # Stores scraped financial data  
│── reports/                     # Contains generated PDF reports  
│── tickers.csv                  # List of tickers to analyze  
│── README.md                    # Project documentation  
📄 Generated Reports
The final PDF reports summarize:
✅ Stock Classification (Strong, Weak, etc.)
✅ F1 Score Trend – Determines if stock strength is improving
✅ Valuation Trend – Detects if the stock is becoming a good buy
✅ Sentiment Analysis – Evaluates positive/negative news impact
✅ Final Verdict – Recommends Buy / Hold / Sell

🛠 Troubleshooting
Issue: Missing trend data in reports?
✔ Run plot_trends.py manually to regenerate CSV files

bash
Copy
Edit
python plot_trends.py --data-dir financial_data --tickers "AAPL,TSLA,GM"
Issue: Sentiment analysis failing?
✔ Ensure sentiment_tracker.py is properly fetching news

Issue: Reports not generating?
✔ Check financial_data/trend_data/ for missing files

🏆 Contributing
Feel free to submit PRs for new features, bug fixes, or optimizations!
