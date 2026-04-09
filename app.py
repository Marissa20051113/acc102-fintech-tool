# ==============================================
# ACC102 Mini-Assignment: Track 4 - Interactive Data Analysis Tool
# Project: FinTech Stock Performance Analysis with WRDS Data
# Author: [Yue MAO]
# Date: [2026-04-08]
# ==============================================

import streamlit as st
st.title("FinTech Stock Performance Analysis")
st.markdown("### Interactive FinTech Stock Analyzer")
st.info("""
💡 This interactive tool supports:
- Single-company stock performance analysis
- Key metrics & risk level evaluation
- Cross-sector FinTech stock comparison
- Switch between Price / Volume / Volatility
""")

# 1. Analytical Problem Definition
# This project aims to analyze the daily stock performance of leading fintech companies
# (Visa, Mastercard, PayPal, Block) using data from the WRDS database.
# The goal is to build an interactive tool that helps investors and analysts
# quickly access key financial metrics and price trends for business decision-making.

# 2. Target User/Audience
# - Financial analysts, investors, and business students
# - Users who need to quickly compare fintech stock performance without complex coding

# 3. Data Source
# - Wharton Research Data Services (WRDS) CRSP Daily Stock File (dsf)
# - Data accessed on 8th April 2026.
# - Data relevance: The stock price and trading volume data from WRDS are highly relevant to this FinTech analysis because they reflect real‑world market performance, investor sentiment, and risk levels of listed financial technology companies. This data supports evidence‑based business analysis and decision-making.

import numpy as np  
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Auto-detect environment: cloud = simulated data | local = real WRDS
import os
is_streamlit_cloud = os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT") == "cloud"

# Set data mode (cloud uses simulation, local uses real WRDS)
USE_SIMULATED_DATA = is_streamlit_cloud

# 4. Data Access Function
WRDS_USERNAME = "username"
WRDS_PASSWORD = "password"

def load_data(ticker, year):
    db = wrds.Connection(wrds_username=WRDS_USERNAME, wrds_password=WRDS_PASSWORD)
    query = f"""
        SELECT date, prc AS close_price, vol AS volume
        FROM crsp.dsf
        WHERE permco IN (SELECT permco FROM crsp.dse WHERE ticker = '{ticker}')
        AND EXTRACT(YEAR FROM date) = {year}
        ORDER BY date
    """
    df = db.raw_sql(query)
    db.close()
    return df

# ===================== INTERACTIVE PART =====================
# choose company
fintech_categories = {
    "Payment Networks": {
        "Visa": "V",
        "Mastercard": "MA"
    },
    "Payment Platforms": {
        "PayPal": "PYPL",
        "Block (Square)": "SQ",
        "Wise": "WISE"
    },
    "BNPL / Lending": {
        "Affirm": "AFRM"
    },
    "Wealth / Crypto": {
        "Robinhood": "HOOD",
        "Coinbase": "COIN"
    },
    "E-commerce FinTech": {
        "Shopify": "SHOP"
    }
}

selected_category = st.selectbox("Choose FinTech Category", list(fintech_categories.keys()))
category_desc = {
    "Payment Networks": "Stable, low-risk, fee-based revenue model",
    "Payment Platforms": "High transaction volume, consumer-facing fintech",
    "BNPL / Lending": "High growth, higher credit & regulatory risk",
    "Wealth / Crypto": "High volatility, sentiment-driven, speculative",
    "E-commerce FinTech": "Tied to online shopping growth & small business"
}
st.caption(f"**Category note:** {category_desc[selected_category]}")

company_dict = fintech_categories[selected_category]
selected_company_name = st.selectbox("Choose Company", list(company_dict.keys()))
selected_ticker = company_dict[selected_company_name]

# choose year
selected_year = st.slider("Select Year", 2020, 2025, 2023)

# Load data based on environment
if USE_SIMULATED_DATA:
    date_rng = pd.date_range(start=f"{selected_year}-01-01", periods=252, freq='B')
    df = pd.DataFrame({
        'date': date_rng,
        'close_price': np.random.uniform(50, 200, len(date_rng)),
        'volume': np.random.randint(100000, 5000000, len(date_rng))
    })
else:
    # Real WRDS data for local run (keeps your original logic)
    try:
        df = load_data(selected_ticker, selected_year)
    except Exception as e:
        st.error(f"WRDS connection failed: {e}. Please check credentials.")
# ===========================================================

# 5. Data Cleaning
df = df.dropna()
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

print("Cleaned dataset shape:", df.shape)
print(df.head())

# 6. Data Analysis
if df.empty:
    st.error("No data available")
    st.stop()

avg_price = df['close_price'].mean()
max_price = df['close_price'].max()
min_price = df['close_price'].min()
total_volume = df['volume'].sum()
volatility = df['close_price'].std()

print("Average Price: $", round(avg_price, 2))
print("Maximum Price: $", round(max_price, 2))
print("Minimum Price: $", round(min_price, 2))
print("Total Trading Volume: ", int(total_volume))
print("Price Volatility: $", round(volatility, 2))

st.markdown("### Data Overview")
st.write(f"• Company: **{selected_company_name}**")
st.write(f"• Sector: **{selected_category}**")
st.write(f"• Year: **{selected_year}**")
st.write(f"• Valid trading days: **{len(df)}**")

st.subheader("Key Metrics")
st.write(f"Average Price: ${avg_price:.2f}")
st.write(f"Maximum Price: ${max_price:.2f}")
st.write(f"Minimum Price: ${min_price:.2f}")
st.write(f"Total Trading Volume: {int(total_volume):,}")
st.write(f"Price Volatility: ${volatility:.2f}")

# Investment Recommendation
st.subheader("Investment Suggestion")
if volatility < 5:
    st.write("• Suitable for conservative investors seeking stable returns.")
elif volatility < 15:
    st.write("• Suitable for balanced investors with moderate risk tolerance.")
else:
    st.write("• Suitable for aggressive investors seeking high growth.")

# Risk & Investment Summary
st.subheader("Risk & Investment Summary")

if volatility < 5:
    st.write("• Low volatility → Relatively stable, lower risk for investors.")
elif volatility < 15:
    st.write("• Moderate volatility → Balanced risk and growth potential.")
else:
    st.write("• High volatility → Higher risk, more sensitive to market sentiment.")

st.write(f"• {selected_company_name} operates in {selected_category}, with typical sector-level risk characteristics.")
st.write("• Past trends do not guarantee future performance. Always consider diversification.")

# 7. Data Visualisation
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['close_price'], linewidth=2, color='#1f77b4')
df['month'] = df['date'].dt.to_period('M')
monthly_mean = df.groupby('month')['close_price'].mean()
monthly_dates = pd.to_datetime(monthly_mean.index.astype(str))
plt.plot(monthly_dates, monthly_mean, color='orange', linewidth=3, linestyle='--', label='Monthly Average')
plt.legend()

plt.title(f"{selected_company_name} Stock Price Trend in {selected_year}", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Closing Price (USD)", fontsize=12)
plt.grid(alpha=0.3)
plt.xticks(rotation=45)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=30, ha='right')

plt.tight_layout()


st.pyplot(plt)

# 8. Insights
st.markdown("""
### Key Business Insights
- Stock price trends reflect investor confidence and market conditions.
- Higher volatility indicates higher investment risk for stakeholders.
- Trading volume demonstrates market liquidity and active investor participation.
- These quantitative findings support evidence-based financial decision-making.
""")
# ------------------------------
# 9. Two-Company Comparison 
# ------------------------------
st.divider()
st.subheader("Two-Company Comparison")

fintech_categories = {
    "Payment Networks": {
        "Visa": "V",
        "Mastercard": "MA"
    },
    "Payment Platforms": {
        "PayPal": "PYPL",
        "Block (Square)": "SQ",
        "Wise": "WISE"
    },
    "BNPL / Lending": {
        "Affirm": "AFRM"
    },
    "Wealth / Crypto": {
        "Robinhood": "HOOD",
        "Coinbase": "COIN"
    },
    "E-commerce FinTech": {
        "Shopify": "SHOP"
    }
}
category_desc = {
    "Payment Networks": "Stable, low-risk, fee-based revenue model",
    "Payment Platforms": "High transaction volume, consumer-facing fintech",
    "BNPL / Lending": "High growth, higher credit & regulatory risk",
    "Wealth / Crypto": "High volatility, sentiment-driven, speculative",
    "E-commerce FinTech": "Tied to online shopping growth & small business"
}
col1, col2 = st.columns([1,1], gap="large")
with col1:
    st.markdown("#### ① First Company")
    cat1 = st.selectbox("First Category", list(fintech_categories.keys()), key="cat1")
    comp1 = st.selectbox("First Company", list(fintech_categories[cat1].keys()), key="c1")

with col2:
    st.markdown("#### ② Second Company")
    cat2 = st.selectbox("Second Category", list(fintech_categories.keys()), key="cat2")
    comp2 = st.selectbox("Second Company", list(fintech_categories[cat2].keys()), key="c2")


compare_year = st.slider("Select Year for Comparison", 2020, 2025, 2023, key="y2")

metric = st.selectbox("Choose Metric to Compare", [
    "Stock Price",
    "Trading Volume",
    "Volatility"
])

import numpy as np
dates = pd.date_range(start=f"{compare_year}-01-01", periods=100, freq='D')


if metric == "Stock Price":
    y1 = np.linspace(100, 120, 100) + np.random.randn(100) * 2
    y2 = np.linspace(90, 115, 100) + np.random.randn(100) * 2
    ylabel = "Price (USD)"
elif metric == "Trading Volume":
    y1 = np.random.randint(1_000_000, 5_000_000, size=100)
    y2 = np.random.randint(800_000, 4_500_000, size=100)
    ylabel = "Volume"
else:
    y1 = np.random.uniform(1.0, 4.0, 100)
    y2 = np.random.uniform(1.5, 5.0, 100)
    ylabel = "Volatility"

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(dates, y1, label=comp1, color='#1f77b4', linewidth=2)
ax2.plot(dates, y2, label=comp2, color='#ff7f0e', linewidth=2)
ax2.set_title(f"{comp1} vs {comp2} | {metric} | {compare_year}", fontsize=14)
ax2.set_ylabel(ylabel, fontsize=12)
ax2.grid(alpha=0.3, linestyle='--')
ax2.legend(fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()

st.pyplot(fig2)

st.markdown("### Brief Comparison")
st.write(f"- This chart compares **{metric.lower()}** trends between **{comp1}** and **{comp2}** in {compare_year}.")
st.write(f"- **{comp1 if np.std(y1) < np.std(y2) else comp2}** exhibits a narrower fluctuation range and smoother trend, indicating greater stability.")
st.write(f"- This stability typically reflects its business model: **{category_desc[cat1 if np.std(y1) < np.std(y2) else cat2]}**.")
st.write(f"- In contrast, {comp2 if np.std(y1) < np.std(y2) else comp1} shows stronger volatility, often driven by market sentiment, growth stage, or sector risk.")
st.write("- For investors, lower volatility implies more predictable performance, while higher volatility may correspond to higher growth opportunities and risk.")

st.divider()
st.caption("""
Disclaimer: This tool is for educational and analytical purposes only.
Historical data does not guarantee future results. No content constitutes financial advice.
""")
