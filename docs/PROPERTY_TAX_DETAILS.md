# Property Tax in Georgia - Detailed Documentation

## Overview

Property tax in Georgia is an annual tax levied on real estate and movable property owned by individuals and legal entities. The tax is calculated based on the market value of the property.

## Tax Rate

### Standard Rate
- **Up to 1%** of property market value annually
- The exact rate may vary by municipality (typically 0.5% - 1%)
- Most municipalities use **1%** as the standard rate

### Rate Variations
- **Residential properties:** Typically 0.5% - 1%
- **Commercial properties:** Typically 1% - 1.5%
- **Agricultural land:** May have different rates
- **Municipal variations:** Each municipality may set its own rate within legal limits

## Income Threshold

### Current Threshold (2025)

#### According to Georgian Tax Code (RS.ge)
- **40,000 GEL** annual income from Georgian sources (individual income)
- Property tax applies only if annual income exceeds this threshold
- Below threshold: **Property tax is exempt**

#### Calculator Implementation
- **✅ FIXED:** The calculator now defaults to **40,000 GEL** (RS.ge official threshold)
- **Configurable:** Users can select:
  1. **RS.ge Official (40,000 GEL)** - Default, for individual income
  2. **Custom Threshold** - Users can set custom threshold (e.g., 65,000 GEL for family income if applicable)
- **Verification:** Users are warned to verify with RS.ge which threshold applies to their situation

### Important Note
**✅ RESOLVED:** 
- **Default threshold:** 40,000 GEL (RS.ge official - individual income)
- **Custom threshold option:** Available for users who need different threshold (e.g., 65,000 GEL for family income)
- **Action:** Users should verify with RS.ge which threshold applies to their specific situation

## Calculation Method

### Basic Formula
```
Step 1: Determine if income exceeds threshold
    If Annual Income ≤ Threshold:
        Property Tax = 0 (Exempt)
    
    If Annual Income > Threshold:
        Proceed to Step 2

Step 2: Calculate property tax
    For each property:
        Property Tax = Property Market Value × Tax Rate
    
    Total Property Tax = Sum of all individual property taxes
```

### Detailed Calculation
```
Property Tax = Σ (Property Market Value × Tax Rate)

Where:
- Property Market Value = Market value or purchase price
- Tax Rate = Typically 1% (0.01)
- Σ = Sum of all properties owned
```

## Property Valuation

### Valuation Basis
1. **Market Value:** Current market value of the property
2. **Purchase Price:** Price paid when property was acquired
3. **RS.ge Assessment:** Official assessment by Revenue Service (may differ from market value)

### Valuation Methods
- **Self-declaration:** Property owner declares market value
- **RS.ge assessment:** Revenue Service may assess independently
- **Professional appraisal:** Certified appraiser valuation

### Important Notes
- Property values should reflect **actual market conditions**
- RS.ge may challenge self-declared values
- For accurate calculations, use RS.ge assessed values when available

## Examples

### Example 1: Single Property, Above Threshold
- **Property value:** 150,000 GEL
- **Annual income:** 80,000 GEL (above 65,000 GEL threshold)
- **Tax rate:** 1%
- **Calculation:** 150,000 × 0.01 = **1,500 GEL/year**

### Example 2: Multiple Properties, Above Threshold
- **Property 1 value:** 100,000 GEL
- **Property 2 value:** 200,000 GEL
- **Property 3 value:** 50,000 GEL
- **Annual income:** 90,000 GEL (above threshold)
- **Tax rate:** 1%
- **Calculation:**
  - Property 1: 100,000 × 0.01 = 1,000 GEL
  - Property 2: 200,000 × 0.01 = 2,000 GEL
  - Property 3: 50,000 × 0.01 = 500 GEL
  - **Total: 3,500 GEL/year**

### Example 3: Below Threshold (Exempt)
- **Property value:** 300,000 GEL
- **Annual income:** 50,000 GEL (below 65,000 GEL threshold)
- **Tax:** **0 GEL (exempt)**

### Example 4: Different Tax Rates by Property Type
- **Residential property:** 200,000 GEL × 0.01 = 2,000 GEL
- **Commercial property:** 300,000 GEL × 0.015 = 4,500 GEL
- **Total:** 6,500 GEL/year

## Tax Payment

### Payment Schedule
- Property tax is an **annual tax**
- Typically due by a specific date each year (check RS.ge for current deadlines)
- May be paid in installments (verify with RS.ge)

### Payment Methods
- Online through RS.ge portal
- Bank transfer
- Other methods as specified by RS.ge

## Exemptions and Deductions

### Income Threshold Exemption
- If annual income ≤ threshold, property tax is **fully exempt**

### Other Possible Exemptions
- Primary residence (conditions apply - verify with RS.ge)
- Properties used for specific purposes (agricultural, etc.)
- Properties owned by certain categories of individuals

**Note:** Exemptions may vary - always verify with RS.ge or current tax legislation.

## Compliance

### Declaration Requirements
- Property owners must declare property values
- RS.ge may verify declarations
- Penalties may apply for incorrect declarations

### Record Keeping
- Keep records of property purchases
- Keep records of property valuations
- Keep records of tax payments

## Current Implementation in Calculator

### How It Works
1. User selects income threshold (RS.ge official 40,000 GEL or custom)
2. User enters property values (market value or purchase price)
3. User sets property tax rate (default 1%, can be adjusted)
4. System calculates total property value
5. System checks if income exceeds selected threshold
6. If above threshold: Calculates tax as (rate% × property value)
7. If below threshold: Tax = 0 (exempt)

### Current Features
- **Tax rate:** User-configurable (default 1%, can be 0-2%)
- **Threshold:** User-selectable (default: 40,000 GEL RS.ge official, or custom)
- **Valuation:** Based on user-provided market value or purchase price
- **Verification warnings:** Clear notices about threshold discrepancies

### Current Features
- **Property Types:** Support for residential, commercial, and agricultural properties
- **Municipality Presets:** Quick selection for common municipalities (Tbilisi, Batumi, Kutaisi, etc.)
- **Custom Rates:** Full flexibility to set custom tax rates
- **Property Type Tracking:** Each property can be categorized by type
- **Verification Warnings:** Clear notices about verifying rates with local municipality

### Remaining Limitations
- Uses user-provided values (not RS.ge assessed values)
- Property type-specific rates are informational only (users set the actual rate)
- Users should verify threshold applicability and exact rates with RS.ge

## Verification and Updates

### Always Verify
1. **Current tax rate** with RS.ge or municipality
2. **Current threshold** (40,000 GEL vs 65,000 GEL)
3. **Property valuations** with RS.ge official assessments
4. **Exemptions** applicable to your situation

### Official Sources
- **RS.ge Website:** https://www.rs.ge/
- **RS.ge Taxpayer Portal:** https://www.rs.ge/TaxPayer-en
- **Local Municipality:** Check local property tax regulations

## References

- RS.ge - Property Tax Law
- Tax Code of Georgia - Property Tax Article
- Local Municipality Tax Regulations
- RS.ge Official Property Tax Calculator

---

## Last Updated
- **Document Version:** 1.0
- **Last Updated:** 2025-01-19
- **Tax Year:** 2025

**⚠️ Important:** This documentation is based on available information. Tax laws change frequently. Always verify current regulations with RS.ge or a qualified tax advisor.

