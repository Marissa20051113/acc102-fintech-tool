{\rtf1\ansi\ansicpg936\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # FinTech Stock Performance Analysis Tool\
## ACC102 Mini-Assignment (Track 4: Interactive Data Analysis Tool)\
\
## 1. Problem & User\
This project builds an interactive stock analysis tool for FinTech companies using real WRDS data. It helps financial analysts, investors, and business students quickly view stock trends, compare companies, and assess risk levels without coding.\
\
## 2. Data\
- Source: WRDS CRSP Daily Stock File (dsf)\
- Access Date: 8th April 2026\
- Key fields: date, closing price, trading volume\
- Fallback: Simulated data for public demonstration\
\
## 3. Methods\
1. Connect to WRDS database to pull real stock data\
2. Data cleaning: remove missing values, standardize dates\
3. Calculate key metrics: average price, volatility, total volume\
4. Build interactive UI with Streamlit (company selection, year slider, comparison)\
5. Visualize price trends and dual-company comparison\
6. Provide risk evaluation and investment suggestions\
\
## 4. Key Findings\
- Payment network stocks (Visa, Mastercard) show low volatility and high stability\
- Platform and crypto-related stocks have higher volatility and risk\
- Monthly average price smooths short\uc0\u8209 term fluctuations\
- Volatility directly reflects risk level for different FinTech sectors\
\
## 5. How to run\
### Local run\
pip install -r requirements.txt\
streamlit run app.py\
\
### Online access\
[Your Streamlit link here]\
\
## 6. Product link / Demo\
- Streamlit App: [Your Streamlit link here]\
- GitHub Repository: [Your GitHub link here]\
\
## 7. Limitations & next steps\
Limitations:\
- Requires WRDS account for real data\
- Analysis is historical only\
- Comparison uses simulated data for public deployment\
\
Next steps:\
- Add real\uc0\u8209 time API data\
- Include more financial indicators (ROE, P/E ratio)\
- Support global FinTech companies\
- Add portfolio simulation\
\
---\
\
### Disclaimer\
This tool is for educational and analytical purposes only. Historical data does not guarantee future results. No content constitutes financial advice.\
\
### Author\
Yue MAO\
Xi'an Jiaotong-Liverpool University\
ACC102 Mini-Assignment, Track 4\
\
### AI Disclosure\
AI tool (Doubao) assisted with code structure, visualization, and documentation. All final work and logic are completed by the author.}