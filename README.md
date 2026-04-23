# FinTech Stock Performance Analysis Tool
## ACC102 Mini-Assignment (Track 4: Interactive Data Analysis Tool)

## 1. Problem & User
This project develops an interactive data analysis tool for evaluating the stock performance of major FinTech companies using historical data from WRDS. The tool is designed for financial analysts, investors, and business students who want to quickly explore price trends, compare firm performance, and evaluate risk metrics without advanced coding knowledge.

## 2. Data
- Source: WRDS CRSP Daily Stock File (dsf)
- Access Date: 8th April 2026
- Key fields: date, closing price, trading volume,net income, assets, equity
- Fallback: Simulated data for public demonstration

## 3. Methods
1. Establish connection to WRDS database and extract daily stock and fundamental data
2. Data cleaning: remove missing values, standardize date formats, align time series
3. Calculate core metrics: average price, volatility, total return, and trading volume
4. Compute professional risk indicators: Beta, annualized volatility, max drawdown, Sharpe ratio
5. Build an interactive web interface using Streamlit with company and year selection
6. Visualize price trends, cumulative returns, Bollinger Bands, and rolling volatility
7. Support cross-company comparison of price and volume trends
8. Conduct financial ratio analysis and DuPont decomposition (ROE, profit margin, asset turnover, leverage)
9. Generate automated analysis summaries and investment insights

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
[https://acc102-fintech-tool-anxi5f842owvxr946r3laq.streamlit.app]

## 6. Product link / Demo
- Streamlit App: [https://acc102-fintech-tool-anxi5f842owvxr946r3laq.streamlit.app]
- GitHub Repository: [https://github.com/Marissa20051113/acc102-fintech-tool/edit/main/README.md]

## 7. Limitations & next steps
Limitations:
- Real data access requires a valid WRDS account; simulated data is used for public deployment
- Analysis is limited to historical performance and does not predict future returns
- Some financial indicators may be incomplete if Compustat data is unavailable
- Analysis does not include macroeconomic factors or external market shocks
  
Next steps:
- Integrate real-time stock price API for up-to-date market data
- Expand financial indicators to include P/E ratio, P/B ratio, and free cash flow
- Include more global and regional FinTech firms for wider comparison
- Add portfolio construction and risk backtesting functions
- Incorporate macroeconomic variables to improve explanatory power
  
---
This project aligns with ACC102’s learning objectives of applying data analytics to real-world business problems.

### Disclaimer
This tool is for educational and analytical purposes only. Historical data does not guarantee future results. No content constitutes financial advice.

### Author
Yue MAO
Xi'an Jiaotong-Liverpool University
ACC102 Mini-Assignment, Track 4

### AI Disclosure
AI tool (Doubao,Gemini) assisted with code structure, visualization, and documentation. All final work and logic are completed by the author.

Note: The tool uses WRDS data with simulated fallback for public deployment. First load may take 1-2 minutes due to dependency installation.
