# Georgian Tax Rules - According to RS.ge and Georgian Law

This document describes the tax calculation rules implemented in the Georgian Tax Calculator, based on RS.ge (Revenue Service of Georgia) regulations and Georgian tax law.

## Table of Contents

1. [Personal Income Tax (Salary)](#personal-income-tax-salary)
2. [Micro Business Tax](#micro-business-tax)
3. [Small Business Tax](#small-business-tax)
4. [Rental Income Tax](#rental-income-tax)
5. [Capital Gains Tax](#capital-gains-tax)
6. [Dividends Tax](#dividends-tax)
7. [Interest Income Tax](#interest-income-tax)
8. [Property Tax](#property-tax)
9. [Residency Status](#residency-status)
10. [References](#references)

---

## Personal Income Tax (Salary)

### Rate
- **20%** of gross salary income

### Pension Contributions
- **Employee contribution:** 2% of gross salary (mandatory)
- **Employer contribution:** 18% of gross salary (not included in employee tax calculation)

### Calculation Formula
```
Annual Gross Salary = Monthly Gross × Number of Months
Employee Pension Contribution = Annual Gross × 2%
Personal Income Tax (PIT) = Annual Gross × 20%
```

### Example
- Monthly gross salary: 5,000 GEL
- Months worked: 12
- Annual gross: 5,000 × 12 = 60,000 GEL
- Employee pension: 60,000 × 0.02 = 1,200 GEL
- PIT: 60,000 × 0.20 = 12,000 GEL

### Legal Reference
- RS.ge - Personal Income Tax Law
- Tax Code of Georgia, Article on Personal Income Tax

---

## Micro Business Tax

### Eligibility
- Annual turnover **up to 200,000 GEL**

### Tax Rate
- **1%** of turnover (simplified tax regime)

### Calculation Formula
```
Tax = Turnover × 1%
```

### Example
- Annual turnover: 150,000 GEL
- Tax: 150,000 × 0.01 = 1,500 GEL

### Important Notes
- If turnover exceeds 200,000 GEL, the business must register as Small Business
- Micro business tax is a simplified regime with minimal compliance requirements

### Legal Reference
- RS.ge - Micro Business Tax Regime
- Tax Code of Georgia, Article on Simplified Tax Regimes

---

## Small Business Tax

### Eligibility
- Annual turnover **exceeds 200,000 GEL** or business chooses to register as Small Business

### Tax Rate
- **1%** of turnover (simplified tax regime)

### Calculation Formula
```
Tax = Turnover × 1%
```

### Example
- Annual turnover: 500,000 GEL
- Tax: 500,000 × 0.01 = 5,000 GEL

### Important Notes
- Small business tax is also a simplified regime
- Different compliance requirements than micro business
- Must be registered with RS.ge

### Legal Reference
- RS.ge - Small Business Tax Regime
- Tax Code of Georgia, Article on Small Business Taxation

---

## Rental Income Tax

### Tax Rate Options

#### Option 1: Standard Rate
- **20%** of net rental income (after deductions)

#### Option 2: Simplified Rate (5% Special Rate)
- **5%** of gross rental income (if eligible)
- Available for certain types of rental properties

### Calculation Formula

**Standard Rate:**
```
Net Rental Income = Gross Rental Income - Allowable Deductions
Tax = Net Rental Income × 20%
```

**Simplified Rate (5%):**
```
Tax = Gross Rental Income × 5%
```

### Example (5% Rate)
- Monthly rent: 1,000 GEL
- Months: 12
- Annual gross rental: 1,000 × 12 = 12,000 GEL
- Tax: 12,000 × 0.05 = 600 GEL

### Legal Reference
- RS.ge - Rental Income Taxation
- Tax Code of Georgia, Article on Rental Income

---

## Capital Gains Tax

### Tax Rate
- **5%** of capital gain (profit from sale)

### Calculation Formula
```
Capital Gain = Sale Price - Purchase Price
Tax = Capital Gain × 5%
```

### Exemptions
- Primary residence may be exempt (conditions apply)
- Losses can offset gains

### Example
- Purchase price: 100,000 GEL
- Sale price: 120,000 GEL
- Capital gain: 120,000 - 100,000 = 20,000 GEL
- Tax: 20,000 × 0.05 = 1,000 GEL

### Important Notes
- Only applies to gains (if sale price > purchase price)
- If sale price ≤ purchase price, no tax is due
- Applies to real estate, vehicles, and other capital assets

### Legal Reference
- RS.ge - Capital Gains Tax
- Tax Code of Georgia, Article on Capital Gains

---

## Dividends Tax

### Tax Rate
- **5%** final withholding tax

### Calculation Formula
```
Tax = Dividends Amount × 5%
```

### Example
- Dividends received: 10,000 GEL
- Tax: 10,000 × 0.05 = 500 GEL

### Important Notes
- This is a **final withholding tax**
- No additional tax is due on dividends
- Tax is typically withheld at source

### Legal Reference
- RS.ge - Dividends Taxation
- Tax Code of Georgia, Article on Dividends

---

## Interest Income Tax

### Tax Rate
- **5%** final withholding tax

### Calculation Formula
```
Tax = Interest Amount × 5%
```

### Example
- Interest received: 5,000 GEL
- Tax: 5,000 × 0.05 = 250 GEL

### Important Notes
- This is a **final withholding tax**
- No additional tax is due on interest income
- Tax is typically withheld at source

### Legal Reference
- RS.ge - Interest Income Taxation
- Tax Code of Georgia, Article on Interest Income

---

## Property Tax

### Tax Rate
- **Up to 1%** of property market value annually
- Rate may vary by municipality (typically 0.5% - 1%)
- **✅ Confirmed:** Calculator uses 1% (0.01) - correct

### Income Threshold
- **40,000 GEL** annual income from Georgian sources (per Georgian Tax Code and RS.ge)
- Property tax applies only if income exceeds this threshold
- **⚠️ IMPORTANT:** The calculator currently uses **65,000 GEL** as the threshold
  - This may be for **family income** (combined household income)
  - OR this may need to be updated to 40,000 GEL
  - **VERIFY with RS.ge** which threshold applies: individual income (40,000 GEL) or family income (65,000 GEL)

### Calculation Formula
```
If Annual Income ≤ Threshold:
    Property Tax = 0 (Exempt)

If Annual Income > Threshold:
    Property Tax = Property Market Value × Tax Rate (typically 1%)
```

### Property Valuation
- Based on **market value** or **purchase price**
- Property values should reflect actual market conditions
- RS.ge may assess property values independently

### Example
- Property market value: 200,000 GEL
- Annual income: 80,000 GEL (above threshold)
- Tax rate: 1%
- Property tax: 200,000 × 0.01 = 2,000 GEL/year

### Multiple Properties
- Each property is taxed separately
- Total property tax = Sum of (Property Value × Tax Rate) for all properties

### Important Notes
- Property tax is an annual tax
- Tax rates may vary by:
  - Municipality
  - Property type (residential, commercial, etc.)
  - Property location
- Always consult RS.ge for official property valuations
- Threshold may be based on individual or family income (verify current law)

### Legal Reference
- RS.ge - Property Tax Law
- Tax Code of Georgia, Article on Property Tax
- Local municipality tax regulations

**See [PROPERTY_TAX_DETAILS.md](./PROPERTY_TAX_DETAILS.md) for comprehensive property tax documentation.**

---

## Residency Status

### Resident
- Individual who is a tax resident of Georgia
- Generally: spends 183+ days per year in Georgia or has permanent residence
- Subject to tax on worldwide income (with certain exemptions)

### Non-Resident
- Individual who is not a tax resident of Georgia
- Subject to tax only on Georgian-source income

### Important Notes
- Residency status affects tax obligations
- Consult RS.ge or tax advisor to determine residency status
- Residency rules may have changed - verify current regulations

### Legal Reference
- RS.ge - Tax Residency Rules
- Tax Code of Georgia, Article on Tax Residency

---

## References

### Official Sources
- **RS.ge (Revenue Service of Georgia):** https://www.rs.ge/
- **Tax Code of Georgia:** Available on RS.ge website
- **RS.ge Taxpayer Portal:** https://www.rs.ge/TaxPayer-en
- **RS.ge Property Tax Information:** https://www.rs.ge/PropertyTaxLiability

### Important Disclaimers
1. **This calculator is unofficial** - Always verify calculations with RS.ge or a qualified tax advisor
2. **Tax laws change** - Regulations may be updated annually
3. **Individual circumstances vary** - This tool provides estimates only
4. **Property valuations** - Official RS.ge assessments may differ from market values
5. **Thresholds and rates** - Verify current rates and thresholds with RS.ge

### Verification
- For official tax calculations, consult RS.ge directly
- For complex situations, consult a qualified tax advisor
- RS.ge provides official tax calculation tools and guidance

---

## Last Updated
- **Document Version:** 1.0
- **Last Updated:** 2025-01-19
- **Tax Year Covered:** 2025

**Note:** Tax rules and rates are subject to change. Always verify current regulations with RS.ge or a qualified tax professional.

