# FinTech Stock Performance Analysis Tool
## ACC102 Mini-Assignment | Track 4 Interactive Tool

## 1. Problem & User
This interactive tool analyzes FinTech stock performance using real WRDS data. It helps investors, analysts, and business students quickly view price trends, key metrics, risk levels, and compare two companies.

## 2. Data
- Source: WRDS CRSP Daily Stock File (dsf)
- Access date: 8 April 2026
- Key fields: date, closing price, trading volume

## 3. Methods
1. Connect to WRDS to retrieve historical stock data
2. Data cleaning: remove missing values, standardize dates
3. Calculate key metrics: average price, max/min price, volatility, total volume
4. Build interactive interface with Streamlit
5. Visualize price trends and monthly average
6. Provide risk evaluation and investment suggestions
7. Support two-company comparison (price, volume, volatility)

## 4. Key Findings
- Payment network stocks (Visa, Mastercard) show low volatility and high stability
- FinTech stocks in crypto/wealth sectors have higher volatility and risk
- Volatility reflects sector risk and business model characteristics
- Monthly average price shows long‑term trend more clearly

## 5. How to run
1. Install required packages: pip install -r requirements.txt
2. Enter your WRDS username and password in the code
3. Run: streamlit run app.py

 Note:
- The cloud preview link uses simulated data automatically for stable display.
- For real WRDS data on your local machine:
  1. Enter your WRDS username and password in the code
  2. The system will auto-switch to real WRDS data when run locally

## 6. Product link / Demo
- App link: 【Streamlit链接】
- GitHub repo: 【GitHub仓库链接】

## 7. Limitations & next steps
Limitations:
- Requires WRDS account to access real data
- Analysis is historical only
- First load may take time due to data retrieval

Next steps:
- Add more financial indicators (ROE, P/E ratio)
- Support more global FinTech companies
- Add portfolio analysis function

---

### Disclaimer
This tool is for educational and analytical purposes only.  
Historical data does not guarantee future results. No content constitutes financial advice.

### Author
Yue MAO  
ACC102 Mini-Assignment Track 4

### AI Disclosure
AI tool assisted with code structure, visualization, and documentation. All logic and final work are completed by the author.
