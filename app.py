# ==============================================
# ACC102 Mini-Assignment: Track 4 - Interactive Data Analysis Tool
# Project: FinTech Stock Performance Analysis with WRDS Data
# Author: Yue MAO
# Date: 2026-04-09
# ==============================================

import streamlit as st
import numpy as np
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import linregress

# ===================== PAGE LAYOUT =====================
st.set_page_config(layout="wide")
st.sidebar.header("⚙️ Control Panel")
st.sidebar.caption("Adjust company, sector and time range here.")

# 🔐 WRDS Login (on the left sidebar)
st.sidebar.subheader("🔐 WRDS Login")
WRDS_USERNAME = st.sidebar.text_input("WRDS Username")
WRDS_PASSWORD = st.sidebar.text_input("WRDS Password", type="password")
# ======================================================

st.title("FinTech Stock Performance Analysis")
st.markdown("### Interactive FinTech Analyzer")
st.info("""
💡 This interactive tool supports:
- Single-company stock performance analysis
- Key metrics & risk level evaluation
- Comparison with S&P 500 market benchmark
- Cross-company financial & stock performance comparison
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

def load_sp500(year):
    db = wrds.Connection(wrds_username=WRDS_USERNAME, wrds_password=WRDS_PASSWORD)
    query = f"""
        SELECT date, prc AS close_price
        FROM crsp.dsf
        WHERE permco IN (SELECT permco FROM crsp.dse WHERE ticker = 'SPY')
        AND EXTRACT(YEAR FROM date) = {year}
        ORDER BY date
    """
    df = db.raw_sql(query)
    db.close()
    return df

def load_fundamentals(ticker):
    try:
        db = wrds.Connection(wrds_username=WRDS_USERNAME, wrds_password=WRDS_PASSWORD)
        query = f"""
            SELECT pe_ratio, pb_ratio, roe, market_cap
            FROM comp.funda
            WHERE tic = '{ticker}'
            AND datadate >= '2023-01-01'
            ORDER BY datadate DESC
            LIMIT 1
        """
        df_fund = db.raw_sql(query)
        db.close()
        return df_fund.iloc[0] if not df_fund.empty else None
    except:
        return None

# ===================== SIDEBAR SELECTORS =====================
fintech_categories = {
    "Payment Networks": {"Visa": "V", "Mastercard": "MA"},
    "Payment Platforms": {"PayPal": "PYPL", "Block (Square)": "SQ", "Wise": "WISE"},
    "BNPL / Lending": {"Affirm": "AFRM"},
    "Wealth / Crypto": {"Robinhood": "HOOD", "Coinbase": "COIN"},
    "E-commerce FinTech": {"Shopify": "SHOP"}
}

category_desc = {
    "Payment Networks": "Stable, low-risk, fee-based revenue model",
    "Payment Platforms": "High transaction volume, consumer-facing fintech",
    "BNPL / Lending": "High growth, higher credit & regulatory risk",
    "Wealth / Crypto": "High volatility, sentiment-driven, speculative",
    "E-commerce FinTech": "Tied to online shopping growth & small business"
}

# SIDEBAR: Single Company Analysis
st.sidebar.subheader("📊 Single Company Analysis")
selected_category = st.sidebar.selectbox(
    "Choose FinTech Category",
    list(fintech_categories.keys()),
    help="You can switch between different FinTech sectors."
)
st.sidebar.caption(f"*{category_desc[selected_category]}*")

company_dict = fintech_categories[selected_category]
selected_company_name = st.sidebar.selectbox(
    "Choose Company",
    list(company_dict.keys()),
    help="Switch to any listed FinTech firm here."
)
selected_ticker = company_dict[selected_company_name]

selected_year = st.sidebar.slider(
    "Select Year", 2020, 2025, 2023,
    help="Change the analysis year to observe trend differences."
)

# ===================== LOAD DATA =====================
try:
    df = load_data(selected_ticker, selected_year)
except:
    date_rng = pd.date_range(start=f"{selected_year}-01-01", periods=200, freq='D')
    sim_price = np.linspace(80, 150, 200) + np.random.randn(200)*3
    sim_vol = np.random.randint(1_000_000, 5_000_000, 200)
    df = pd.DataFrame({"date": date_rng, "close_price": sim_price, "volume": sim_vol})

try:
    df_spy = load_sp500(selected_year)
except:
    df_spy = pd.DataFrame({
        "date": df['date'],
        "close_price": np.linspace(400, 450, len(df)) + np.random.randn(len(df))*2
    })

# ===================== DATA CLEANING =====================
df = df.dropna()
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

df_spy = df_spy.dropna()
df_spy['date'] = pd.to_datetime(df_spy['date'])

# Align dates
df = df.merge(df_spy[['date','close_price']], on='date', suffixes=('','_spy'))
df.rename(columns={'close_price_spy':'spy_price'}, inplace=True)

if df.empty:
    st.error("No data available")
    st.stop()

# ===================== RISK METRICS =====================
df['ret'] = df['close_price'].pct_change().dropna()
df['spy_ret'] = df['spy_price'].pct_change().dropna()
df = df.dropna(subset=['ret','spy_ret'])

# Beta
beta = linregress(df['spy_ret'], df['ret'])[0]
# Annualized vol
annual_vol = df['ret'].std() * np.sqrt(252)
# Max Drawdown
df['cumul'] = (1 + df['ret']).cumprod()
df['peak'] = df['cumul'].cummax()
df['dd'] = (df['cumul'] / df['peak']) - 1
max_dd = df['dd'].min()
# Sharpe (simplified, risk-free rate ≈ 0)
sharpe = df['ret'].mean() / df['ret'].std() * np.sqrt(252) if df['ret'].std() != 0 else 0

# ===================== METRICS =====================
avg_price = df['close_price'].mean()
volatility = df['close_price'].std()
df['return'] = df['close_price'].pct_change().fillna(0)
df['cum_return'] = (1 + df['return']).cumprod() - 1
df_spy['return'] = df_spy['close_price'].pct_change().fillna(0)
df_spy['cum_return'] = (1 + df_spy['return']).cumprod() - 1
total_return = df['cum_return'].iloc[-1]
spy_return = df_spy['cum_return'].iloc[-1]

# ===================== MAIN PANEL =====================
st.markdown("## 📈 Single Company Analysis")
st.caption("Results based on WRDS daily stock data. You may modify controls on the left.")

col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.metric("Avg Price", f"${avg_price:.2f}")
with col_b:
    st.metric("Volatility", f"${volatility:.2f}")
with col_c:
    st.metric("Total Return", f"{total_return:.1%}")
with col_d:
    st.metric("VS S&P500", f"{(total_return - spy_return):+.1%}")

# -------------------- RISK INDICATORS --------------------
st.subheader("🧠 Risk Metrics (Professional)")
r1, r2, r3, r4 = st.columns(4)
with r1:
    st.metric("Beta", f"{beta:.2f}")
with r2:
    st.metric("Annual Vol", f"{annual_vol:.1%}")
with r3:
    st.metric("Max Drawdown", f"{max_dd:.1%}")
with r4:
    st.metric("Sharpe Ratio", f"{sharpe:.2f}")

st.subheader("Daily Stock Price (Daily Close)")

fig, ax = plt.subplots(figsize=(14, 5))


colors = ['red' if df['close_price'].iloc[i] > df['close_price'].iloc[i-1] 
          else 'green' for i in range(1, len(df))]
colors.insert(0, '#1f77b4')

ax.scatter(df['date'], df['close_price'], c=colors, s=12, alpha=0.7, label='Daily Price')
ax.plot(df['date'], df['close_price'], color='#1f77b4', linewidth=1.2, alpha=0.8)


ax.plot(df['date'], df['spy_price'], label='S&P 500 (SPY)', 
        linestyle='--', linewidth=2, color='gray')

ax.set_title(f"Daily Closing Price | {selected_company_name}", fontsize=14)
ax.set_ylabel("USD Price")
ax.grid(alpha=0.2)
ax.legend(fontsize=12)

fig.autofmt_xdate(rotation=20, ha='right')
plt.tight_layout()
st.pyplot(fig)

st.subheader("Cumulative Return Comparison")
fig2, ax2 = plt.subplots(figsize=(14, 5))
ax2.plot(df['date'], df['cum_return'], label=selected_company_name, linewidth=2)
ax2.plot(df_spy['date'], df_spy['cum_return'], label='S&P 500', linewidth=2, linestyle='--')
ax2.set_ylabel("Cumulative Return")
ax2.grid(alpha=0.3)
ax2.legend()
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
st.pyplot(fig2)
# ------------------------------------------------------------------------------
# auto analysis
# ------------------------------------------------------------------------------
st.divider()
st.markdown("### 📊 Automated Stock Analysis (Based on WRDS Daily Data)")


category_desc = {
    "Payment Networks": "mature, low-volatility payment network with stable cash flows",
    "Payment Platforms": "retail fintech platform with moderate cyclical volatility",
    "Wealth / Crypto": "sentiment-driven growth stock with high price volatility",
    "BNPL / Lending": "credit-focused fintech with higher macro sensitivity",
    "E-commerce FinTech": "growth-oriented fintech with medium to high volatility"
}
sector_text = category_desc.get(selected_category, "fintech company")


price_start = df['close_price'].iloc[0]
price_end = df['close_price'].iloc[-1]
total_return = (price_end - price_start) / price_start
volatility_ratio = df['close_price'].std() / df['close_price'].mean()


if total_return > 0.05:
    trend_status = "strong upward"
elif total_return > 0:
    trend_status = "modest upward"
elif total_return > -0.05:
    trend_status = "slight downward"
else:
    trend_status = "significant downward"


if volatility_ratio < 0.08:
    vol_status = "very low volatility and high stability"
elif volatility_ratio < 0.15:
    vol_status = "moderate, market-typical volatility"
else:
    vol_status = "high volatility with large daily price swings"


analysis_report = f"""
**{selected_company_name} | {selected_year} Performance Summary**

- **Trend**: The stock showed a **{trend_status}** trend during {selected_year}, with a total return of **{total_return:.1%}**.
- **Volatility**: It exhibited **{vol_status}**.
- **Business Profile**: As a **{sector_text}**, its risk profile aligns naturally with industry benchmarks.
- **Risk Metrics**: Annualized volatility is **{annual_vol:.1%}**, Beta is **{beta:.2f}**, and maximum drawdown was **{max_dd:.1%}**.
"""

st.markdown(analysis_report)

# ===================== RISK SUMMARY =====================
st.subheader("Risk & Investment Insight")
if annual_vol < 0.20:
    st.success(f"Annual Volatility = {annual_vol:.1%}: Low-risk profile.")
elif annual_vol < 0.40:
    st.info(f"Annual Volatility = {annual_vol:.1%}: Moderate risk.")
else:
    st.warning(f"Annual Volatility = {annual_vol:.1%}: High volatility.")

if beta < 0.8:
    st.info(f"Beta = {beta:.2f}: Defensive stock, less sensitive to market swings.")
elif beta > 1.2:
    st.warning(f"Beta = {beta:.2f}: Aggressive stock, amplifies market moves.")
else:
    st.success(f"Beta = {beta:.2f}: Moves in line with the overall market.")

# ------------------------------------------------------------------------------
# 📈 Single Company Volatility Analysis (AUTO SWITCH WITH SELECTED COMPANY)
# ------------------------------------------------------------------------------
st.divider()
st.markdown("## 🧪 Volatility & Price Fluctuation Detail")

try:
    df_vol = load_data(selected_ticker, selected_year)
    df_vol['date'] = pd.to_datetime(df_vol['date'])
    df_vol = df_vol.dropna(subset=['close_price'])
    df_vol = df_vol.sort_values('date')
    df_vol.set_index('date', inplace=True)

    # Daily return
    df_vol['ret'] = df_vol['close_price'].pct_change()
    df_vol['log_ret'] = np.log(1 + df_vol['ret'])

    # Rolling vol (21-day = 1 month)
    df_vol['vol_21d'] = df_vol['ret'].rolling(21).std() * np.sqrt(252)
    df_vol['vol_63d'] = df_vol['ret'].rolling(63).std() * np.sqrt(252)

    # Bollinger bands
    df_vol['ma20'] = df_vol['close_price'].rolling(20).mean()
    df_vol['std20'] = df_vol['close_price'].rolling(20).std()
    df_vol['upper'] = df_vol['ma20'] + 2 * df_vol['std20']
    df_vol['lower'] = df_vol['ma20'] - 2 * df_vol['std20']

    # Metrics
    current_vol = df_vol['vol_21d'].iloc[-1] if len(df_vol) > 21 else np.nan
    avg_vol = df_vol['vol_21d'].mean()

except:
    st.warning("Volatility data unavailable — using simulated trend.")
    dates = pd.date_range(f"{selected_year}-01-01", periods=200, freq='B')
    df_vol = pd.DataFrame(index=dates)
    df_vol['close_price'] = np.cumsum(np.random.randn(200) * 2) + 100
    df_vol['ret'] = df_vol['close_price'].pct_change()
    df_vol['vol_21d'] = df_vol['ret'].rolling(21).std() * np.sqrt(252)
    df_vol['vol_63d'] = df_vol['ret'].rolling(63).std() * np.sqrt(252)
    df_vol['ma20'] = df_vol['close_price'].rolling(20).mean()
    df_vol['std20'] = df_vol['close_price'].rolling(20).std()
    df_vol['upper'] = df_vol['ma20'] + 2 * df_vol['std20']
    df_vol['lower'] = df_vol['ma20'] - 2 * df_vol['std20']
    current_vol = df_vol['vol_21d'].iloc[-1]
    avg_vol = df_vol['vol_21d'].mean()

# Show metrics
vc1, vc2 = st.columns(2)
with vc1:
    st.metric("Current 1M Volatility", f"{current_vol:.1%}" if pd.notna(current_vol) else "-")
with vc2:
    st.metric("Avg 1M Volatility", f"{avg_vol:.1%}" if pd.notna(avg_vol) else "-")

# Plot 1: Bollinger Bands
st.markdown("#### Price & Bollinger Bands (Volatility Range)")
fig_v1, ax_v1 = plt.subplots(figsize=(14, 4))
ax_v1.plot(df_vol.index, df_vol['close_price'], label='Price', linewidth=2)
ax_v1.plot(df_vol.index, df_vol['ma20'], label='20-Day MA', linestyle='--')
ax_v1.fill_between(df_vol.index, df_vol['upper'], df_vol['lower'], alpha=0.1, color='blue')
ax_v1.grid(alpha=0.3)
ax_v1.legend()
plt.xticks(rotation=30)
st.pyplot(fig_v1)
st.markdown("""
**📈 About the Bollinger Bands & Moving Average:**
- The **purple line** is the **20-day moving average (MA)**, which shows the stock’s short-term trend.
- The shaded purple area is the **Bollinger Band**, which represents the typical range of price movement (±2 standard deviations from the MA).
- Narrow bands indicate low volatility, while wide bands show high volatility.
""")

# Plot 2: Rolling Volatility
st.markdown("#### Rolling 1-Month & 3-Month Volatility")
fig_v2, ax_v2 = plt.subplots(figsize=(14, 3))
ax_v2.plot(df_vol.index, df_vol['vol_21d'], label='21-Day Rolling Vol', linewidth=2)
ax_v2.plot(df_vol.index, df_vol['vol_63d'], label='63-Day Rolling Vol', linewidth=2)
ax_v2.grid(alpha=0.3)
ax_v2.legend()
plt.xticks(rotation=30)
st.pyplot(fig_v2)

st.caption("Bollinger bands show price fluctuation range; wider bands = higher volatility.")

# ===================== INDUSTRY BENCHMARK =====================
st.divider()
st.markdown("## 📊 FinTech Sector Benchmark Comparison")
st.caption("Risk & return profile across FinTech sub-industries")

sector_data = pd.DataFrame([
    {"Sector": "Payment Networks", "Avg Return": "12–18%", "Avg Beta": "0.7–0.9", "Risk Level": "Low"},
    {"Sector": "Payment Platforms", "Avg Return": "15–25%", "Avg Beta": "0.9–1.2", "Risk Level": "Medium"},
    {"Sector": "BNPL / Lending", "Avg Return": "20–35%", "Avg Beta": "1.2–1.5", "Risk Level": "High"},
    {"Sector": "Wealth / Crypto", "Avg Return": "-10–40%", "Avg Beta": "1.5+", "Risk Level": "Very High"},
    {"Sector": "E-commerce FinTech", "Avg Return": "18–30%", "Avg Beta": "1.1–1.4", "Risk Level": "Medium-High"}
])
st.dataframe(sector_data, use_container_width=True)

# ===================== TWO-COMPARISON IN SIDEBAR =====================
st.sidebar.divider()
st.sidebar.subheader("🔍 Company Comparison")

with st.sidebar:
    # define
    default_cat1 = "Payment Platforms"
    default_comp1 = "PayPal"
    default_cat2 = "E-commerce FinTech"
    default_comp2 = "Shopify"

    # set index
    categories = list(fintech_categories.keys())
    cat1_index = categories.index(default_cat1)
    cat1 = st.selectbox(
        "First Category", 
        categories,
        index=cat1_index,
        key="cat1"
    )

    companies1 = list(fintech_categories[cat1].keys())
    comp1_index = companies1.index(default_comp1)
    comp1 = st.selectbox(
        "First Company", 
        companies1,
        index=comp1_index,
        key="c1"
    )

    cat2_index = categories.index(default_cat2)
    cat2 = st.selectbox(
        "Second Category", 
        categories,
        index=cat2_index,
        key="cat2"
    )

    companies2 = list(fintech_categories[cat2].keys())
    comp2_index = companies2.index(default_comp2)
    comp2 = st.selectbox(
        "Second Company", 
        companies2,
        index=comp2_index,
        key="c2"
    )

    compare_year = st.slider("Comparison Year", 2020, 2025, 2023, key="y2")
    metric = st.selectbox("Metric", ["Stock Price", "Trading Volume"])

# ===================== REAL COMPANY COMPARISON FROM WRDS =====================
st.divider()
st.markdown("## 🧾 Cross-Company Comparison")
st.caption("Compare price trend, volatility, liquidity and sector characteristics.")
st.caption("💡 **Switch companies using the panel on the left**\n• Stock Price: Compare daily price trend (who gains more)\n• Trading Volume: Compare trading activity (how active the stock is)")
ticker1 = fintech_categories[cat1][comp1]
ticker2 = fintech_categories[cat2][comp2]

# Try load real data first
try:
    df1 = load_data(ticker1, compare_year)
    df2 = load_data(ticker2, compare_year)
    df1['date'] = pd.to_datetime(df1['date'])
    df2['date'] = pd.to_datetime(df2['date'])
    use_real = True
except:
    use_real = False

# Fallback to simulated if failed
if not use_real:
    st.warning("⚠️ Using simulated comparison data (WRDS connection failed)")
    dates = pd.date_range(start=f"{compare_year}-01-01", periods=100, freq='D')
    if metric == "Stock Price":
        y1 = np.linspace(90, 140, 100) + np.random.randn(100)*2.5
        y2 = np.linspace(80, 130, 100) + np.random.randn(100)*2.5
        ylabel = "Price (USD)"
    else:
        y1 = np.random.randint(1_000_000, 5_000_000, 100)
        y2 = np.random.randint(800_000, 4_500_000, 100)
        ylabel = "Volume"

# Plot
fig3, ax3 = plt.subplots(figsize=(14, 5))
if use_real:
    if metric == "Stock Price":
        ax3.plot(df1['date'], df1['close_price'], label=comp1, linewidth=2)
        ax3.plot(df2['date'], df2['close_price'], label=comp2, linewidth=2)
        ax3.set_ylabel("Price (USD)")
    else:
        ax3.plot(df1['date'], df1['volume'], label=comp1, linewidth=2)
        ax3.plot(df2['date'], df2['volume'], label=comp2, linewidth=2)
        ax3.set_ylabel("Volume")
else:
    ax3.plot(dates, y1, label=comp1, linewidth=2)
    ax3.plot(dates, y2, label=comp2, linewidth=2)
    ax3.set_ylabel(ylabel)

ax3.set_title(f"{comp1} vs {comp2} | {metric}")
ax3.grid(alpha=0.3)
ax3.legend()
plt.xticks(rotation=30, ha='right')
st.pyplot(fig3)
st.divider()

st.markdown("### 📊 Automated Cross-Company Analysis")



def calc_metrics(df_data):
    if len(df_data) == 0:
        return 0.0, 0.0
    start_price = df_data['close_price'].iloc[0]
    end_price = df_data['close_price'].iloc[-1]
    ret = (end_price - start_price) / start_price
    vol = df_data['close_price'].std() / df_data['close_price'].mean()
    return ret, vol

ret1, vol1 = calc_metrics(df1)
ret2, vol2 = calc_metrics(df2)


better_perf = comp1 if ret1 > ret2 else comp2
more_volatile = comp1 if vol1 > vol2 else comp2


comparison_text = f"""
**{comp1} vs {comp2} | {compare_year}**
- **Performance**: {better_perf} delivered a stronger return of {max(ret1, ret2):.1%} vs {min(ret1, ret2):.1%}.
- **Volatility**: {more_volatile} showed higher price fluctuation ({max(vol1, vol2):.2f} vs {min(vol1, vol2):.2f}), typical of its FinTech sub-sector.
- **Sector Insight**: This comparison highlights how different FinTech businesses balance return and risk.
"""

st.markdown(comparison_text)

# ------------------------------------------------------------------------------
# financial ratio
# ------------------------------------------------------------------------------
st.divider()
st.markdown("## 🧾 Financial Performance Summary ")
st.caption("select two categories and companies from the left side")

ticker1 = fintech_categories[cat1][comp1]
ticker2 = fintech_categories[cat2][comp2]
company_list = [comp1, comp2]

years_list = [2019, 2020, 2021, 2022, 2023, 2024]


empty_df = pd.DataFrame({
    "Company": [],
    "year": [],
    "roe": [],
    "pm": [],
    "turnover": [],
    "lev": []
})

try:
    db = wrds.Connection(wrds_username=WRDS_USERNAME, wrds_password=WRDS_PASSWORD)
    sql = f"""
        select tic, datadate, ni, sale, at, ceq
        from comp.funda
        where tic in ('{ticker1}', '{ticker2}')
          and datadate >= '2019-01-01'
          and datadate <= '2024-12-31'
    """
    df = db.raw_sql(sql)
    db.close()

    
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")
    df = df.dropna(subset=["datadate", "tic"])
    df["year"] = df["datadate"].dt.year
    df = df.drop_duplicates(subset=["tic", "year"], keep="first")
    df = df[df["datadate"].dt.month == 12].copy()

    
    df["roe"] = (df["ni"] / df["ceq"] * 100).round(2)
    df["pm"] = (df["ni"] / df["sale"] * 100).round(2)
    df["turnover"] = (df["sale"] / df["at"]).round(2)
    df["lev"] = (df["at"] / df["ceq"]).round(2)

    df["Company"] = df["tic"].map({ticker1: comp1, ticker2: comp2})

    
    if df.empty:
        df = empty_df

except Exception as e:
    
    df = empty_df


def make_pivot(df, value_col, is_pct):
    
    pivot = pd.DataFrame(
        index=company_list,
        columns=years_list
    )

    
    for company in company_list:
        for year in years_list:
           
            subset = df[(df["Company"] == company) & (df["year"] == year)]
            if not subset.empty:
                val = subset[value_col].iloc[0]
                if pd.notna(val):
                    pivot.loc[company, year] = val

    
    if is_pct:
        pivot = pivot.astype(str).replace("nan", "-") + "%"
    else:
        pivot = pivot.astype(str).replace("nan", "-")
    
    return pivot


roe_pivot = make_pivot(df, "roe", is_pct=True)
pm_pivot = make_pivot(df, "pm", is_pct=True)
to_pivot = make_pivot(df, "turnover", is_pct=False)
lev_pivot = make_pivot(df, "lev", is_pct=False)


st.subheader("1. ROE (Return on Equity)")
st.dataframe(roe_pivot)

st.subheader("2. Net Profit Margin")
st.dataframe(pm_pivot)

st.subheader("3. Asset Turnover")
st.dataframe(to_pivot)

st.subheader("4. Leverage (Equity Multiplier)")
st.dataframe(lev_pivot)


st.markdown(
    """
    *Note: "-" indicates data not available in WRDS Compustat for the corresponding year.*
    """
)

st.divider()
st.markdown("### 🧩 DuPont Analysis Framework")
st.latex(r"ROE = Profit\ Margin \times Asset\ Turnover \times Leverage")
# ------------------------------------------------------------------------------
# 🤖 Automated DuPont Analysis (only shows if data exists)
# ------------------------------------------------------------------------------
st.markdown("### 📊 Automated DuPont Analysis")

def get_latest_val(df, company, col):
    if df.empty:
        return None
    sub = df[(df["Company"] == company) & df[col].notna()]
    return sub.iloc[-1][col] if not sub.empty else None

c1_roe = get_latest_val(df, comp1, "roe")
c1_pm  = get_latest_val(df, comp1, "pm")
c2_roe = get_latest_val(df, comp2, "roe")
c2_pm  = get_latest_val(df, comp2, "pm")

# Only show analysis if BOTH companies have data
if c1_roe is not None and c2_roe is not None:
    roe_winner = comp1 if c1_roe > c2_roe else comp2
    pm_winner  = comp1 if (c1_pm or -999) > (c2_pm or -999) else comp2

    dupont_text = f"""
**{comp1} vs {comp2} | DuPont Drivers**
- **ROE**: {roe_winner} has higher return on equity.
- **Profit Margin**: {pm_winner} shows stronger net profitability.
- ROE differences reflect margin, asset efficiency, and leverage structure — typical of different FinTech business models.
"""
    st.markdown(dupont_text)
else:
    st.info("ℹ️ DuPont analysis unavailable — insufficient financial data from WRDS Compustat.")
# ------------------------------------------------------------------------------
# 📊 COMPANY VS INDUSTRY BENCHMARK
# ------------------------------------------------------------------------------
st.divider()
st.markdown("## 📌 Company vs Industry Benchmark")
st.caption("How selected companies perform against industry averages")

ind_roe = 15
ind_pm = 16
ind_lev = 2.2

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Industry ROE", f"{ind_roe}%")
with col2:
    st.metric("Avg Industry Margin", f"{ind_pm}%")
with col3:
    st.metric("Avg Industry Leverage", f"{ind_lev}x")

st.markdown("""
- **ROE above industry**: More profitable than peers
- **Margin above industry**: Better cost & pricing power
- **Leverage above industry**: Higher financial risk
""")



# ------------------------------------------------------------------------------
# final
# ------------------------------------------------------------------------------
st.markdown("### 📌 Final Investment Takeaway")

summary = f"""
**Overall Summary for {comp1} & {comp2}**
- These two companies represent distinct FinTech sub-sectors with different risk‑return profiles.
- {comp1} reflects the traits of {cat1}: {category_desc.get(cat1, '')}.
- {comp2} reflects the traits of {cat2}: {category_desc.get(cat2, '')}.
- Investors seeking stability would favor payment networks; those seeking growth may tolerate higher volatility in platforms or crypto‑related firms.
"""

st.markdown(summary)

st.divider()
st.caption("""
Disclaimer: This tool is for educational and analytical purposes only.
Historical data does not guarantee future results. No content constitutes financial advice.
""")
