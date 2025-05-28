import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sympy import symbols, Eq, solve

# -----------------------
# Title & Overview
# -----------------------
st.title("📊 Milo Company Business & Financial Dashboard")
st.markdown("""
Welcome to the interactive dashboard for simulating operations of a Milo company in Nigeria.  
We'll explore monthly profits, what-if analysis, and financial projections.
""")

# -----------------------
# Monthly Operations Simulation
# -----------------------
st.header("🏭 Monthly Revenue, Expenses & Profit Simulation")

price_per_bag = 2000
bags_per_day = 500
investment = 700_000
days_per_month = {"January": 31, "February": 28, "December": 31}

data = []
for month, days in days_per_month.items():
    revenue = price_per_bag * bags_per_day * days
    transport = 0.02 * revenue
    salary = 0.30 * revenue
    advert = 150_000
    expenses = transport + salary + advert
    profit = (revenue + investment) - expenses
    data.append([month, revenue, transport, salary, advert, expenses, profit])

df_monthly = pd.DataFrame(data, columns=["Month", "Revenue (₦)", "Transport (₦)", "Salary (₦)", "Adverts (₦)", "Total Expenses (₦)", "Profit (₦)"])

month_choice = st.selectbox("📅 Select Month", df_monthly["Month"])
st.dataframe(df_monthly[df_monthly["Month"] == month_choice])

# -----------------------
# What-If Analysis
# -----------------------
st.header("🔍 What-If Analysis (CEO's Questions)")

st.subheader("a. Bags/day needed for ₦30M profit")

x = symbols('x')
days = 31
revenue_expr = 2000 * x * days
transport_expr = 0.02 * revenue_expr
salary_expr = 0.30 * revenue_expr
expenses_expr = transport_expr + salary_expr + 150000
profit_expr = (revenue_expr + investment) - expenses_expr
eq = Eq(profit_expr, 30_000_000)
bags_needed = solve(eq, x)[0]
st.write(f"✅ To earn ₦30M profit: **{int(bags_needed)} bags/day**")

st.subheader("b. Price/bag for ₦35M profit at 600 bags/day")

p = symbols('p')
revenue_expr_b = p * 600 * 31
transport_expr_b = 0.02 * revenue_expr_b
salary_expr_b = 0.30 * revenue_expr_b
expenses_expr_b = transport_expr_b + salary_expr_b + 150000
profit_expr_b = (revenue_expr_b + investment) - expenses_expr_b
eq_b = Eq(profit_expr_b, 35_000_000)
price_needed = solve(eq_b, p)[0]
st.write(f"✅ Required price: **₦{int(price_needed)} per bag**")

st.subheader("c. Ad budget for max expense of ₦10,250,000")

revenue = 2000 * 500 * 31
transport = 0.02 * revenue
salary = 0.30 * revenue
a = symbols('a')
eq_c = Eq(transport + salary + a, 10_250_000)
ad_budget = solve(eq_c, a)[0]
st.write(f"✅ Max allowed ad budget: **₦{int(ad_budget)}**")

# -----------------------
# Ben's House Savings
# -----------------------
st.header("🏠 Ben's House Savings Planner")

house_price = st.number_input("Enter house price (₦)", 1_000_000, 50_000_000, 9_000_000)
rate = 0.02
years = [15, 16, 17, 18, 25]
results = {}

for t in years:
    P = symbols('P')
    A = P * ((1 + rate)**t - 1) / rate
    eq = Eq(A, house_price)
    ans = solve(eq, P)[0]
    results[t] = round(ans, 2)

df_ben = pd.DataFrame.from_dict(results, orient='index', columns=["Annual Deposit (₦)"])
st.dataframe(df_ben)

# -----------------------
# Mary’s Compound Savings
# -----------------------
st.header("💵 Mary's Savings Forecast")

monthly_savings = 1200
rates = [0.015, 0.02, 0.025, 0.03, 0.04, 0.045, 0.05]
durations = [10, 12, 14, 16, 18, 20]

mary_savings = []
for r in rates:
    row = []
    for y in durations:
        months = y * 12
        fv = monthly_savings * (((1 + r/12)**months - 1) / (r/12))
        row.append(round(fv, 2))
    mary_savings.append(row)

df_mary = pd.DataFrame(mary_savings, index=[f"{int(r*100)}%" for r in rates], columns=[f"{y} yrs" for y in durations])
st.dataframe(df_mary)

# -----------------------
# Visualizations
# -----------------------
st.header("📈 Visual Insights")

st.subheader("Monthly Profit")
fig, ax = plt.subplots()
sns.barplot(data=df_monthly, x="Month", y="Profit (₦)", ax=ax)
ax.set_title("Monthly Profit")
st.pyplot(fig)

st.subheader("Mary’s Compound Savings Heatmap")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.heatmap(df_mary, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax2)
st.pyplot(fig2)

# -----------------------
# Conclusion
# -----------------------
st.header("✅ Conclusion & Insights")
st.markdown("""
- To reach ₦30M profit → ~**715 bags/day**.
- Max 600 bags/day → need to charge ~**₦2,369/bag**.
- For ₦10.25M expense cap → ad budget should be ~**₦721K**.
- Ben should save ₦400K–₦500K/year depending on years.
- Mary benefits greatly from long-term saving even at modest interest.

This dashboard is built using **Python + Streamlit** and is an example of real-life business analytics.
""")
