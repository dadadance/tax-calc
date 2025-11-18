# How Users See Their Results - Visual Guide

## Example Scenario

**User has:**
- Salary: 5,000 GEL/month × 12 months
- Dividends: 15,000 GEL
- Interest: 3,000 GEL
- Rental Income: 1,200 GEL/month × 12 months (5% regime)
- Capital Gains:
  - Car 1: Purchased 20k, Sold 25k
  - Car 2: Purchased 15k, Sold 18k
  - Apartment: Purchased 80k, Sold 120k
  - House 1: Purchased 150k, Sold 180k
  - House 2: Purchased 200k, Sold 250k (primary residence - exempt)

## What Users See in the Streamlit App

### 1. **Top Summary Cards** (Always Visible)

```
┌─────────────────┬─────────────────┬─────────────────┐
│ Total Tax Due   │ Total Income    │ Effective Rate  │
│ 17,520.00 GEL   │ 220,400.00 GEL  │ 7.95%          │
└─────────────────┴─────────────────┴─────────────────┘
```

### 2. **Breakdown by Regime Table**

```
┌──────────────────────┬──────────────┬─────────────┐
│ Regime               │ Tax (GEL)   │ Percentage │
├──────────────────────┼──────────────┼─────────────┤
│ Salary               │ 12,000.00   │ 68.5%       │
│ Capital Gains        │  3,900.00   │ 22.3%       │
│ Dividends            │    750.00    │  4.3%       │
│ Rental               │    720.00    │  4.1%       │
│ Interest             │    150.00    │  0.9%       │
└──────────────────────┴──────────────┴─────────────┘
```

### 3. **Expandable Step-by-Step Calculations**

Each regime has an expandable section showing detailed calculations:

#### **📋 Salary - Tax: 12,000.00 GEL** (Click to expand)

```
Step 1: Annual gross salary (source 1)
Formula: gross = monthly_gross * months
Values: gross = 5,000.00 * 12
Result: 60,000.00 GEL
Legal Reference: RS.ge - Personal Income Tax

Step 2: Employee pension contribution (2%)
Formula: pension = gross * pension_rate
Values: pension = 60,000.00 * 0.02
Result: 1,200.00 GEL
Legal Reference: RS.ge - Pension Contributions

Step 3: Personal Income Tax (PIT) 20% on salary
Formula: pit = gross * 0.20
Values: pit = 60,000.00 * 0.20
Result: 12,000.00 GEL
Legal Reference: RS.ge - Personal Income Tax Law, Article X
```

#### **📋 Capital Gains - Tax: 3,900.00 GEL** (Click to expand)

```
Step 1: Capital gain (property/vehicle 1) - Car 1
Formula: gain = sale_price - purchase_price
Values: gain = 25,000.00 - 20,000.00
Result: 5,000.00 GEL
Legal Reference: RS.ge - Capital Gains Tax

Step 2: Capital gains tax (5%)
Formula: tax = gain * 0.05
Values: tax = 5,000.00 * 0.05
Result: 250.00 GEL
Legal Reference: RS.ge - Capital Gains Tax (5%)

Step 3: Capital gain (property/vehicle 2) - Car 2
Formula: gain = sale_price - purchase_price
Values: gain = 18,000.00 - 15,000.00
Result: 3,000.00 GEL

Step 4: Capital gains tax (5%)
Formula: tax = gain * 0.05
Values: tax = 3,000.00 * 0.05
Result: 150.00 GEL

Step 5: Capital gain (property/vehicle 3) - Apartment
Formula: gain = sale_price - purchase_price
Values: gain = 120,000.00 - 80,000.00
Result: 40,000.00 GEL

Step 6: Capital gains tax (5%)
Formula: tax = gain * 0.05
Values: tax = 40,000.00 * 0.05
Result: 2,000.00 GEL

Step 7: Capital gain (property/vehicle 4) - House 1
Formula: gain = sale_price - purchase_price
Values: gain = 180,000.00 - 150,000.00
Result: 30,000.00 GEL

Step 8: Capital gains tax (5%)
Formula: tax = gain * 0.05
Values: tax = 30,000.00 * 0.05
Result: 1,500.00 GEL

Step 9: Capital gain (property/vehicle 5) - House 2
Formula: gain = sale_price - purchase_price
Values: gain = 250,000.00 - 200,000.00
Result: 50,000.00 GEL

Step 10: Capital gains tax (exempt: primary residence)
Formula: tax = 0 (exempt)
Values: tax = 0
Result: 0.00 GEL
Legal Reference: RS.ge - Capital Gains Tax (Primary Residence Exemption)
```

#### **📋 Dividends - Tax: 750.00 GEL** (Click to expand)

```
Step 1: Total dividends received
Formula: total = sum(dividends)
Values: total = 15,000.00
Result: 15,000.00 GEL
Legal Reference: RS.ge - Dividends Tax

Step 2: Dividends tax (5% final withholding)
Formula: tax = total * 0.05
Values: tax = 15,000.00 * 0.05
Result: 750.00 GEL
Legal Reference: RS.ge - Dividends Tax (5%)
```

#### **📋 Rental - Tax: 720.00 GEL** (Click to expand)

```
Step 1: Annual rental income (property 1)
Formula: annual_rent = monthly_rent * months
Values: annual_rent = 1,200.00 * 12
Result: 14,400.00 GEL
Legal Reference: RS.ge - Rental Income Tax

Step 2: Rental tax (5% special regime)
Formula: tax = annual_rent * 0.05
Values: tax = 14,400.00 * 0.05
Result: 720.00 GEL
Legal Reference: RS.ge - Rental Income Special Regime (5%)
```

#### **📋 Interest - Tax: 150.00 GEL** (Click to expand)

```
Step 1: Total interest received
Formula: total = sum(interest)
Values: total = 3,000.00
Result: 3,000.00 GEL
Legal Reference: RS.ge - Interest Income Tax

Step 2: Interest tax (5% final withholding)
Formula: tax = total * 0.05
Values: tax = 3,000.00 * 0.05
Result: 150.00 GEL
Legal Reference: RS.ge - Interest Income Tax (5%)
```

## Key Features Users See

1. **Clear Summary**: Total tax, income, and effective rate at a glance
2. **Regime Breakdown**: See which income types contribute most to tax
3. **Detailed Steps**: Every calculation is shown step-by-step
4. **Formulas**: Understand how each tax is calculated
5. **Legal References**: Know which RS.ge rules apply
6. **Exemptions**: Clearly marked (e.g., primary residence exemption)
7. **Warnings**: If any thresholds are exceeded or conditions not met

## Navigation

- **Sidebar**: Profile settings, tax year, residency status
- **Tabs**: Add different income types (Salary, Micro Business, Small Business, Rental, Capital Gains, Dividends, Interest, Property Tax)
- **Results Section**: Always visible at the bottom, updates automatically
- **Error Logs**: Available via sidebar navigation

## Example Calculation Summary

For this scenario:
- **Total Income**: 220,400 GEL
  - Salary: 60,000 GEL
  - Capital Gains: 128,000 GEL (78,000 taxable)
  - Rental: 14,400 GEL
  - Dividends: 15,000 GEL
  - Interest: 3,000 GEL

- **Total Tax**: 17,520 GEL
  - Salary PIT: 12,000 GEL (20%)
  - Capital Gains: 3,900 GEL (5% on 78k taxable)
  - Dividends: 750 GEL (5%)
  - Rental: 720 GEL (5%)
  - Interest: 150 GEL (5%)

- **Effective Rate**: 7.95%
- **Note**: House 2 (primary residence) is exempt from capital gains tax, saving 2,500 GEL

