# FinTech Stock Performance Analysis Tool
## ACC102 Mini-Assignment (Track 4: Interactive Data Analysis Tool)

## 1. Problem & User
This project builds an interactive stock analysis tool for FinTech companies using real WRDS data. It helps financial analysts, investors, and business students quickly view stock trends, compare companies, and assess risk levels without coding.

## 2. Data
- Source: WRDS CRSP Daily Stock File (dsf)
- Access Date: 8th April 2026
- Key fields: date, closing price, trading volume
- Fallback: Simulated data for public demonstration

## 3. Methods
1. Connect to WRDS database to pull real stock data
2. Data cleaning: remove missing values, standardize dates
3. Calculate key metrics: average price, volatility, total volume
4. Risk metrics: Beta, annualized volatility, maximum drawdown, Sharpe ratio
5. Build interactive UI with Streamlit (company selection, year slider, comparison)
6. Visualize price trends, cumulative returns, and Bollinger Bands
7. Perform cross-company comparison and DuPont financial analysis
8. Provide risk evaluation and investment suggestions

## 4. Key Findings
- Payment network stocks (Visa, Mastercard) show low volatility and high stability
- Platform and crypto-related stocks have higher volatility and risk
- Monthly average price smooths short‑term fluctuations
- Volatility directly reflects risk level for different FinTech sectors
- DuPont analysis shows that payment networks maintain higher profit margins and ROE, while platform firms rely more on asset turnover and leverage

## 5. How to run
### Local run
pip install -r requirements.txt
streamlit run app.py

### Online access
[Your Streamlit link here]

## 6. Product link / Demo
- Streamlit App: [Your Streamlit link here]
- GitHub Repository: [Your GitHub link here]

## 7. Limitations & next steps
Limitations:
- Requires WRDS account for real data; simulated fallback is used for public deployment
- Analysis is based on historical data only
- Cross-company comparison may use simulated data if WRDS connection fails

Next steps:
- Add real‑time price API integration
- Expand to include more financial indicators (P/E ratio, free cash flow)
- Support more global FinTech companies
- Add portfolio risk simulation and backtesting

---
This project aligns with ACC102’s learning objectives of applying data analytics to real-world business problems.

### Disclaimer
This tool is for educational and analytical purposes only. Historical data does not guarantee future results. No content constitutes financial advice.

### Author
Yue MAO
Xi'an Jiaotong-Liverpool University
ACC102 Mini-Assignment, Track 4

### AI Disclosure
AI tool (Doubao) assisted with code structure, visualization, and documentation. All final work and logic are completed by the author.

Note: The tool uses WRDS data with simulated fallback for public deployment. First load may take 1-2 minutes due to dependency installation.
