"""Tax Rules and Formulas information page."""
import streamlit as st


st.set_page_config(
    page_title="Tax Rules & Formulas - Tax Calculator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Tax Rules & Formulas")
st.caption("Complete reference guide for Georgian tax calculations")

st.info("💡 **Note:** These are simplified formulas for common cases. Actual tax law may have additional conditions and exceptions. Always verify with RS.ge or a tax advisor.")

# Table of Contents
st.header("📑 Table of Contents")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    - [Salary Income](#salary-income)
    - [Micro Business](#micro-business)
    - [Small Business](#small-business)
    """)
with col2:
    st.markdown("""
    - [Rental Income](#rental-income)
    - [Capital Gains](#capital-gains)
    - [Dividends & Interest](#dividends--interest)
    """)
with col3:
    st.markdown("""
    - [Property Tax](#property-tax)
    - [General Rules](#general-rules)
    """)

st.divider()

# Salary Income
st.header("💰 Salary Income")
st.subheader("Personal Income Tax (PIT)")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Formula:**
    ```
    Annual Gross Salary = Monthly Gross × Months Worked
    PIT = Annual Gross Salary × 20%
    ```
    
    **Employee Pension Contribution:**
    ```
    Pension = Annual Gross Salary × Pension Rate (2% or 4%)
    ```
    
    **Example:**
    - Monthly salary: 5,000 GEL
    - Months worked: 12
    - Annual gross: 5,000 × 12 = 60,000 GEL
    - PIT: 60,000 × 0.20 = 12,000 GEL
    - Pension (2%): 60,000 × 0.02 = 1,200 GEL
    """)
with col2:
    st.metric("PIT Rate", "20%")
    st.metric("Pension Rate", "2% or 4%")
    st.caption("**Legal Reference:** RS.ge - Personal Income Tax Law")

st.divider()

# Micro Business
st.header("🏢 Micro Business")
st.subheader("Micro Business Tax Regime")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Eligibility Conditions:**
    - No employees
    - Activity allowed for micro regime
    - Meets turnover requirements
    
    **Formula:**
    ```
    If Eligible:
        Tax = 0% (Zero tax)
    
    If Not Eligible (Fallback):
        Tax = Turnover × 20% (Standard PIT)
    ```
    
    **Example:**
    - Turnover: 30,000 GEL
    - Eligible: Yes (no employees, allowed activity)
    - Tax: 0 GEL (0%)
    
    - Turnover: 30,000 GEL
    - Eligible: No (has employees)
    - Tax: 30,000 × 0.20 = 6,000 GEL (20% fallback)
    """)
with col2:
    st.metric("Tax Rate (Eligible)", "0%")
    st.metric("Tax Rate (Not Eligible)", "20%")
    st.caption("**Legal Reference:** RS.ge - Micro Business Tax Regime")

st.divider()

# Small Business
st.header("🏪 Small Business")
st.subheader("Small Business Tax Regime")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Threshold:** 500,000 GEL annual turnover
    
    **Formula:**
    ```
    If Turnover ≤ 500,000 GEL:
        Tax = Turnover × 1%
    
    If Turnover > 500,000 GEL:
        Tax_500k = 500,000 × 1%
        Excess = Turnover - 500,000
        Tax_Excess = Excess × 3%
        Total Tax = Tax_500k + Tax_Excess
    ```
    
    **Examples:**
    
    *Below Threshold:*
    - Turnover: 300,000 GEL
    - Tax: 300,000 × 0.01 = 3,000 GEL
    
    *Above Threshold:*
    - Turnover: 600,000 GEL
    - Tax on first 500k: 500,000 × 0.01 = 5,000 GEL
    - Tax on excess 100k: 100,000 × 0.03 = 3,000 GEL
    - Total Tax: 5,000 + 3,000 = 8,000 GEL
    """)
with col2:
    st.metric("Rate (≤ 500k)", "1%")
    st.metric("Rate (> 500k)", "3%")
    st.metric("Threshold", "500,000 GEL")
    st.caption("**Legal Reference:** RS.ge - Small Business Tax Regime")

st.divider()

# Rental Income
st.header("🏠 Rental Income")
st.subheader("Residential Rental Tax")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Two Regimes Available:**
    
    **1. Special 5% Regime:**
    ```
    Annual Rent = Monthly Rent × Months Rented
    Tax = Annual Rent × 5%
    ```
    
    **2. Standard 20% PIT:**
    ```
    Annual Rent = Monthly Rent × Months Rented
    Tax = Annual Rent × 20%
    ```
    
    **Examples:**
    
    *5% Special Regime:*
    - Monthly rent: 1,200 GEL
    - Months: 12
    - Annual rent: 1,200 × 12 = 14,400 GEL
    - Tax: 14,400 × 0.05 = 720 GEL
    
    *Standard 20%:*
    - Same income: 14,400 GEL
    - Tax: 14,400 × 0.20 = 2,880 GEL
    """)
with col2:
    st.metric("Special Regime", "5%")
    st.metric("Standard Rate", "20%")
    st.caption("**Legal Reference:** RS.ge - Rental Income Tax")

st.divider()

# Capital Gains
st.header("📈 Capital Gains")
st.subheader("Capital Gains Tax on Property/Vehicles")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Formula:**
    ```
    Capital Gain = Sale Price - Purchase Price
    
    If Gain ≤ 0 (Loss):
        Tax = 0 (No tax on losses)
    
    If Primary Residence:
        Tax = 0 (Exempt)
    
    Otherwise:
        Tax = Capital Gain × 5%
    ```
    
    **Examples:**
    
    *Normal Capital Gain:*
    - Purchase: 100,000 GEL
    - Sale: 120,000 GEL
    - Gain: 120,000 - 100,000 = 20,000 GEL
    - Tax: 20,000 × 0.05 = 1,000 GEL
    
    *Primary Residence (Exempt):*
    - Purchase: 200,000 GEL
    - Sale: 250,000 GEL
    - Gain: 50,000 GEL
    - Tax: 0 GEL (exempt)
    
    *Loss (No Tax):*
    - Purchase: 120,000 GEL
    - Sale: 100,000 GEL
    - Gain: -20,000 GEL (loss)
    - Tax: 0 GEL
    """)
with col2:
    st.metric("Tax Rate", "5%")
    st.metric("Primary Residence", "Exempt")
    st.metric("Losses", "No Tax")
    st.caption("**Legal Reference:** RS.ge - Capital Gains Tax")

st.divider()

# Dividends and Interest
st.header("💵 Dividends & Interest")
st.subheader("Final Withholding Tax")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Dividends:**
    ```
    Tax = Dividends Amount × 5%
    ```
    
    **Interest:**
    ```
    Tax = Interest Amount × 5%
    ```
    
    **Examples:**
    
    *Dividends:*
    - Dividends received: 10,000 GEL
    - Tax: 10,000 × 0.05 = 500 GEL
    
    *Interest:*
    - Interest received: 5,000 GEL
    - Tax: 5,000 × 0.05 = 250 GEL
    
    **Note:** These are final withholding taxes - no additional tax due.
    """)
with col2:
    st.metric("Dividends Rate", "5%")
    st.metric("Interest Rate", "5%")
    st.metric("Type", "Final Withholding")
    st.caption("**Legal Reference:** RS.ge - Dividends/Interest Tax")

st.divider()

# Property Tax
st.header("🏘️ Property Tax")
st.subheader("Individual Property Tax")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    **Threshold:** 65,000 GEL annual family income
    
    **Formula:**
    ```
    If Family Income ≤ 65,000 GEL:
        Tax = 0 (Exempt - below threshold)
    
    If Family Income > 65,000 GEL:
        Tax ≈ Properties × Average Value × Rate
        (Simplified estimate - actual depends on property details)
    ```
    
    **Simplified Estimate:**
    - Assumes average property value: 100,000 GEL
    - Estimated rate: 1%
    - Formula: `Properties × 100,000 × 0.01`
    
    **Examples:**
    
    *Below Threshold (Exempt):*
    - Family income: 60,000 GEL
    - Properties: 2
    - Tax: 0 GEL (exempt)
    
    *Above Threshold:*
    - Family income: 80,000 GEL
    - Properties: 2
    - Estimated tax: 2 × 100,000 × 0.01 = 2,000 GEL
    
    **⚠️ Important:** Property tax calculation is simplified. Actual tax depends on:
    - Property values
    - Property locations
    - Property types
    - Detailed RS.ge assessment
    """)
with col2:
    st.metric("Threshold", "65,000 GEL")
    st.metric("Below Threshold", "Exempt")
    st.metric("Est. Rate (Above)", "~1%")
    st.caption("**Legal Reference:** RS.ge - Property Tax")
    st.warning("**Simplified calculation** - consult RS.ge for accurate assessment")

st.divider()

# General Rules
st.header("📋 General Rules")

st.subheader("Residency Status")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Resident:**
    - Taxed on worldwide income
    - All income sources included
    """)
with col2:
    st.markdown("""
    **Non-Resident:**
    - Taxed on Georgian-source income only
    - Same tax rates apply
    """)

st.subheader("Tax Year")
st.markdown("""
- Tax calculations are per calendar year
- Available years: 2024, 2025, 2026, 2027, 2028
- Rules may vary by year (check RS.ge for updates)
""")

st.subheader("Currency")
st.markdown("""
- All amounts in **GEL (Georgian Lari)**
- All calculations use GEL
""")

st.subheader("Effective Tax Rate")
st.markdown("""
```
Effective Tax Rate = Total Tax / Total Income × 100%
```

This shows the overall tax burden as a percentage of total income.
""")

st.divider()

# Summary Table
st.header("📊 Tax Rates Summary")

summary_data = {
    "Income Type": [
        "Salary (PIT)",
        "Micro Business (Eligible)",
        "Micro Business (Not Eligible)",
        "Small Business (≤ 500k)",
        "Small Business (> 500k)",
        "Rental (5% Regime)",
        "Rental (Standard)",
        "Capital Gains",
        "Dividends",
        "Interest",
        "Property Tax (Below Threshold)",
        "Property Tax (Above Threshold)"
    ],
    "Tax Rate": [
        "20%",
        "0%",
        "20%",
        "1%",
        "1% + 3%",
        "5%",
        "20%",
        "5%",
        "5%",
        "5%",
        "0% (Exempt)",
        "~1% (Estimated)"
    ],
    "Notes": [
        "On gross salary",
        "If conditions met",
        "Fallback rate",
        "On turnover",
        "1% on first 500k, 3% on excess",
        "Special regime",
        "Standard PIT",
        "On gains only",
        "Final withholding",
        "Final withholding",
        "Family income ≤ 65k",
        "Family income > 65k"
    ]
}

st.dataframe(summary_data, use_container_width=True, hide_index=True)

st.divider()

# Disclaimer
st.warning("""
**⚠️ Important Disclaimer:**

- This calculator is **unofficial** and for estimation purposes only
- Tax laws may change - always verify with RS.ge
- Calculations are simplified and may not cover all edge cases
- Property tax is estimated - actual tax requires detailed assessment
- Consult a professional tax advisor for official tax advice
- This tool is not a substitute for professional tax consultation
""")

st.caption("**Last Updated:** 2025 | **Rules Version:** v2025.01")
st.caption("**Links:** [RS.ge](https://www.rs.ge) | [RS.ge Tax Portal](https://www.rs.ge)")

