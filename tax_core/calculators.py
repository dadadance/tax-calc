"""Tax calculation logic for each regime."""
from typing import List
from tax_core.models import (
    UserProfile,
    RegimeResult,
    CalculationStep,
    CalculationResult,
    SalaryIncome,
    MicroBusinessIncome,
    SmallBusinessIncome,
    RentalIncome,
    CapitalGainsIncome,
    DividendsIncome,
    InterestIncome,
    PropertyTaxInput,
)


def calculate_salary(salary_incomes: List[SalaryIncome]) -> RegimeResult:
    """Calculate tax for salary income."""
    steps = []
    total_tax = 0.0
    
    for idx, salary in enumerate(salary_incomes):
        if salary.monthly_gross <= 0 or salary.months <= 0:
            continue
            
        # Annual gross salary
        annual_gross = salary.monthly_gross * salary.months
        steps.append(CalculationStep(
            id=f"salary_{idx}_gross",
            description=f"Annual gross salary (source {idx + 1})",
            formula="gross = monthly_gross * months",
            values=f"gross = {salary.monthly_gross:,.2f} * {salary.months}",
            result=annual_gross,
            legal_ref="RS.ge - Personal Income Tax"
        ))
        
        # Pension contribution (employee)
        pension_contribution = annual_gross * salary.pension_employee_rate
        steps.append(CalculationStep(
            id=f"salary_{idx}_pension",
            description=f"Employee pension contribution ({salary.pension_employee_rate * 100:.0f}%)",
            formula="pension = gross * pension_rate",
            values=f"pension = {annual_gross:,.2f} * {salary.pension_employee_rate}",
            result=pension_contribution,
            legal_ref="RS.ge - Pension Contributions"
        ))
        
        # PIT on salary (20%)
        pit = annual_gross * 0.20
        steps.append(CalculationStep(
            id=f"salary_{idx}_pit",
            description=f"Personal Income Tax (PIT) 20% on salary",
            formula="pit = gross * 0.20",
            values=f"pit = {annual_gross:,.2f} * 0.20",
            result=pit,
            legal_ref="RS.ge - Personal Income Tax Law, Article X"
        ))
        
        total_tax += pit
    
    return RegimeResult(
        regime_id="salary",
        tax=total_tax,
        steps=steps
    )


def calculate_micro_business(micro_incomes: List[MicroBusinessIncome]) -> RegimeResult:
    """Calculate tax for micro business income."""
    steps = []
    total_tax = 0.0
    warnings = []
    
    for idx, micro in enumerate(micro_incomes):
        if micro.turnover <= 0:
            continue
        
        # Check eligibility
        if not micro.no_employees:
            warnings.append(f"Micro business {idx + 1}: Has employees - may not qualify for 0% rate")
        if not micro.activity_allowed:
            warnings.append(f"Micro business {idx + 1}: Activity may not be allowed for micro regime")
        
        # Micro business: 0% tax if eligible
        if micro.no_employees and micro.activity_allowed:
            steps.append(CalculationStep(
                id=f"micro_{idx}_tax",
                description=f"Micro business tax (0% if eligible)",
                formula="tax = turnover * 0.00",
                values=f"tax = {micro.turnover:,.2f} * 0.00",
                result=0.0,
                legal_ref="RS.ge - Micro Business Tax Regime"
            ))
        else:
            # Fallback: standard PIT (20%)
            fallback_tax = micro.turnover * 0.20
            steps.append(CalculationStep(
                id=f"micro_{idx}_tax",
                description=f"Micro business tax (fallback: 20% PIT - conditions not met)",
                formula="tax = turnover * 0.20",
                values=f"tax = {micro.turnover:,.2f} * 0.20",
                result=fallback_tax,
                legal_ref="RS.ge - Personal Income Tax"
            ))
            total_tax += fallback_tax
    
    return RegimeResult(
        regime_id="micro_business",
        tax=total_tax,
        steps=steps,
        warnings=warnings
    )


def calculate_small_business(small_incomes: List[SmallBusinessIncome]) -> RegimeResult:
    """Calculate tax for small business income."""
    steps = []
    total_tax = 0.0
    warnings = []
    
    for idx, small in enumerate(small_incomes):
        if small.turnover <= 0:
            continue
        
        if not small.registered:
            warnings.append(f"Small business {idx + 1}: Not registered as small business")
        
        # Small business: 1% up to 500,000, 3% above
        threshold = 500000.0
        
        if small.turnover <= threshold:
            tax = small.turnover * 0.01
            steps.append(CalculationStep(
                id=f"small_{idx}_tax",
                description=f"Small business tax (1% up to 500,000 GEL)",
                formula="tax = turnover * 0.01",
                values=f"tax = {small.turnover:,.2f} * 0.01",
                result=tax,
                legal_ref="RS.ge - Small Business Tax Regime"
            ))
        else:
            # Composite: 1% on first 500k + 3% on excess
            tax_500k = threshold * 0.01
            excess = small.turnover - threshold
            tax_excess = excess * 0.03
            tax = tax_500k + tax_excess
            
            steps.append(CalculationStep(
                id=f"small_{idx}_tax_500k",
                description=f"Small business tax: 1% on first 500,000 GEL",
                formula="tax_500k = min(turnover, 500000) * 0.01",
                values=f"tax_500k = 500,000.00 * 0.01",
                result=tax_500k,
                legal_ref="RS.ge - Small Business Tax Regime"
            ))
            steps.append(CalculationStep(
                id=f"small_{idx}_tax_excess",
                description=f"Small business tax: 3% on excess above 500,000 GEL",
                formula="tax_excess = max(turnover - 500000, 0) * 0.03",
                values=f"tax_excess = {excess:,.2f} * 0.03",
                result=tax_excess,
                legal_ref="RS.ge - Small Business Tax Regime"
            ))
            steps.append(CalculationStep(
                id=f"small_{idx}_tax_total",
                description=f"Total small business tax",
                formula="total_tax = tax_500k + tax_excess",
                values=f"total_tax = {tax_500k:,.2f} + {tax_excess:,.2f}",
                result=tax,
                legal_ref="RS.ge - Small Business Tax Regime"
            ))
            
            warnings.append(f"Small business {idx + 1}: Turnover exceeds 500,000 GEL threshold")
        
        total_tax += tax
    
    return RegimeResult(
        regime_id="small_business",
        tax=total_tax,
        steps=steps,
        warnings=warnings
    )


def calculate_rental(rental_incomes: List[RentalIncome]) -> RegimeResult:
    """Calculate tax for rental income."""
    steps = []
    total_tax = 0.0
    
    for idx, rental in enumerate(rental_incomes):
        if rental.monthly_rent <= 0 or rental.months <= 0:
            continue
        
        # Annual rental income
        annual_rent = rental.monthly_rent * rental.months
        steps.append(CalculationStep(
            id=f"rental_{idx}_gross",
            description=f"Annual rental income (property {idx + 1})",
            formula="annual_rent = monthly_rent * months",
            values=f"annual_rent = {rental.monthly_rent:,.2f} * {rental.months}",
            result=annual_rent,
            legal_ref="RS.ge - Rental Income Tax"
        ))
        
        # 5% special regime
        if rental.special_5_percent:
            tax = annual_rent * 0.05
            steps.append(CalculationStep(
                id=f"rental_{idx}_tax",
                description=f"Rental tax (5% special regime)",
                formula="tax = annual_rent * 0.05",
                values=f"tax = {annual_rent:,.2f} * 0.05",
                result=tax,
                legal_ref="RS.ge - Rental Income Special Regime (5%)"
            ))
        else:
            # Standard PIT (20%)
            tax = annual_rent * 0.20
            steps.append(CalculationStep(
                id=f"rental_{idx}_tax",
                description=f"Rental tax (standard 20% PIT)",
                formula="tax = annual_rent * 0.20",
                values=f"tax = {annual_rent:,.2f} * 0.20",
                result=tax,
                legal_ref="RS.ge - Personal Income Tax"
            ))
        
        total_tax += tax
    
    return RegimeResult(
        regime_id="rental",
        tax=total_tax,
        steps=steps
    )


def calculate_capital_gains(cg_incomes: List[CapitalGainsIncome]) -> RegimeResult:
    """Calculate tax for capital gains."""
    steps = []
    total_tax = 0.0
    
    for idx, cg in enumerate(cg_incomes):
        if cg.sale_price <= 0 or cg.purchase_price <= 0:
            continue
        
        # Capital gain
        gain = cg.sale_price - cg.purchase_price
        steps.append(CalculationStep(
            id=f"cg_{idx}_gain",
            description=f"Capital gain (property/vehicle {idx + 1})",
            formula="gain = sale_price - purchase_price",
            values=f"gain = {cg.sale_price:,.2f} - {cg.purchase_price:,.2f}",
            result=gain,
            legal_ref="RS.ge - Capital Gains Tax"
        ))
        
        if gain <= 0:
            steps.append(CalculationStep(
                id=f"cg_{idx}_tax",
                description=f"No tax on capital loss",
                formula="tax = 0 (loss, no tax)",
                values="tax = 0",
                result=0.0,
                legal_ref="RS.ge - Capital Gains Tax"
            ))
            continue
        
        # Check exemptions (simplified)
        if cg.is_primary_residence:
            steps.append(CalculationStep(
                id=f"cg_{idx}_tax",
                description=f"Capital gains tax (exempt: primary residence)",
                formula="tax = 0 (exempt)",
                values="tax = 0",
                result=0.0,
                legal_ref="RS.ge - Capital Gains Tax (Primary Residence Exemption)"
            ))
            continue
        
        # 5% on gains
        tax = gain * 0.05
        steps.append(CalculationStep(
            id=f"cg_{idx}_tax",
            description=f"Capital gains tax (5%)",
            formula="tax = gain * 0.05",
            values=f"tax = {gain:,.2f} * 0.05",
            result=tax,
            legal_ref="RS.ge - Capital Gains Tax (5%)"
        ))
        
        total_tax += tax
    
    return RegimeResult(
        regime_id="capital_gains",
        tax=total_tax,
        steps=steps
    )


def calculate_dividends(dividends_incomes: List[DividendsIncome]) -> RegimeResult:
    """Calculate tax for dividends."""
    steps = []
    total_tax = 0.0
    
    total_dividends = sum(d.amount for d in dividends_incomes if d.amount > 0)
    
    if total_dividends > 0:
        # 5% final withholding
        tax = total_dividends * 0.05
        steps.append(CalculationStep(
            id="dividends_total",
            description="Total dividends received",
            formula="total = sum(dividends)",
            values=f"total = {total_dividends:,.2f}",
            result=total_dividends,
            legal_ref="RS.ge - Dividends Tax"
        ))
        steps.append(CalculationStep(
            id="dividends_tax",
            description="Dividends tax (5% final withholding)",
            formula="tax = total * 0.05",
            values=f"tax = {total_dividends:,.2f} * 0.05",
            result=tax,
            legal_ref="RS.ge - Dividends Tax (5%)"
        ))
        total_tax = tax
    
    return RegimeResult(
        regime_id="dividends",
        tax=total_tax,
        steps=steps
    )


def calculate_interest(interest_incomes: List[InterestIncome]) -> RegimeResult:
    """Calculate tax for interest income."""
    steps = []
    total_tax = 0.0
    
    total_interest = sum(i.amount for i in interest_incomes if i.amount > 0)
    
    if total_interest > 0:
        # 5% final withholding
        tax = total_interest * 0.05
        steps.append(CalculationStep(
            id="interest_total",
            description="Total interest received",
            formula="total = sum(interest)",
            values=f"total = {total_interest:,.2f}",
            result=total_interest,
            legal_ref="RS.ge - Interest Income Tax"
        ))
        steps.append(CalculationStep(
            id="interest_tax",
            description="Interest tax (5% final withholding)",
            formula="tax = total * 0.05",
            values=f"tax = {total_interest:,.2f} * 0.05",
            result=tax,
            legal_ref="RS.ge - Interest Income Tax (5%)"
        ))
        total_tax = tax
    
    return RegimeResult(
        regime_id="interest",
        tax=total_tax,
        steps=steps
    )


def calculate_property_tax(property_inputs: List[PropertyTaxInput]) -> RegimeResult:
    """Calculate property tax (simplified)."""
    steps = []
    total_tax = 0.0
    warnings = []
    
    # Simplified: check if family income exceeds threshold
    # Threshold is typically around 60,000-65,000 GEL per year
    threshold = 65000.0
    
    for idx, prop in enumerate(property_inputs):
        if prop.family_income <= 0:
            continue
        
        steps.append(CalculationStep(
            id=f"property_{idx}_check",
            description=f"Family income check (property set {idx + 1})",
            formula=f"family_income > {threshold:,.0f}",
            values=f"{prop.family_income:,.2f} > {threshold:,.0f}",
            result=prop.family_income,
            legal_ref="RS.ge - Property Tax"
        ))
        
        steps.append(CalculationStep(
            id=f"property_{idx}_properties",
            description=f"Number of properties (property set {idx + 1})",
            formula="properties = count",
            values=f"properties = {prop.properties}",
            result=float(prop.properties),
            legal_ref="RS.ge - Property Tax"
        ))
        
        if prop.family_income <= threshold:
            steps.append(CalculationStep(
                id=f"property_{idx}_tax",
                description=f"Property tax (exempt: below threshold)",
                formula="tax = 0 (below threshold exemption)",
                values=f"tax = 0 (income {prop.family_income:,.2f} ≤ {threshold:,.0f})",
                result=0.0,
                legal_ref="RS.ge - Property Tax (Threshold Exemption)"
            ))
            warnings.append(f"Property set {idx + 1}: Exempt from property tax (family income below {threshold:,.0f} GEL threshold)")
        else:
            # Simplified property tax calculation
            # Basic estimate: property tax typically ranges from 0.5% to 1.5% of property value
            # For MVP, we use a simplified formula based on number of properties
            # Note: Actual property tax depends on property value, location, type, etc.
            
            # Very simplified estimate: assume average property value and rate
            # This is a placeholder - actual calculation requires property details
            estimated_property_value_per_unit = 100000.0  # Placeholder average
            estimated_tax_rate = 0.01  # 1% placeholder rate
            
            estimated_tax = prop.properties * estimated_property_value_per_unit * estimated_tax_rate
            
            steps.append(CalculationStep(
                id=f"property_{idx}_estimate",
                description=f"Estimated property tax (simplified calculation)",
                formula="tax ≈ properties × avg_value × rate",
                values=f"tax ≈ {prop.properties} × {estimated_property_value_per_unit:,.0f} × {estimated_tax_rate}",
                result=estimated_tax,
                legal_ref="RS.ge - Property Tax (Simplified estimate)"
            ))
            
            steps.append(CalculationStep(
                id=f"property_{idx}_tax",
                description=f"Property tax for {prop.properties} properties",
                formula="tax = estimated_tax",
                values=f"tax = {estimated_tax:,.2f}",
                result=estimated_tax,
                legal_ref="RS.ge - Property Tax"
            ))
            
            total_tax += estimated_tax
            warnings.append(
                f"Property set {idx + 1}: Property tax is estimated. "
                f"Actual tax depends on property values, locations, and types. "
                f"Consult RS.ge or a tax advisor for accurate calculation."
            )
    
    if not warnings:
        warnings = []
    else:
        # Add general warning
        warnings.insert(0, "Property tax calculation is simplified. Actual tax depends on property values, locations, and types.")
    
    return RegimeResult(
        regime_id="property_tax",
        tax=total_tax,
        steps=steps,
        warnings=warnings
    )


def calculate_all(profile: UserProfile) -> CalculationResult:
    """Calculate all taxes for the given profile."""
    results = []
    
    # Calculate each regime
    if profile.salary:
        results.append(calculate_salary(profile.salary))
    
    if profile.micro_business:
        results.append(calculate_micro_business(profile.micro_business))
    
    if profile.small_business:
        results.append(calculate_small_business(profile.small_business))
    
    if profile.rental:
        results.append(calculate_rental(profile.rental))
    
    if profile.capital_gains:
        results.append(calculate_capital_gains(profile.capital_gains))
    
    if profile.dividends:
        results.append(calculate_dividends(profile.dividends))
    
    if profile.interest:
        results.append(calculate_interest(profile.interest))
    
    if profile.property_tax:
        results.append(calculate_property_tax(profile.property_tax))
    
    # Calculate totals
    total_tax = sum(r.tax for r in results)
    
    # Calculate total income (simplified)
    total_income = 0.0
    for salary in profile.salary:
        total_income += salary.monthly_gross * salary.months
    for micro in profile.micro_business:
        total_income += micro.turnover
    for small in profile.small_business:
        total_income += small.turnover
    for rental in profile.rental:
        total_income += rental.monthly_rent * rental.months
    for cg in profile.capital_gains:
        if cg.sale_price > cg.purchase_price:
            total_income += cg.sale_price - cg.purchase_price
    for div in profile.dividends:
        total_income += div.amount
    for interest in profile.interest:
        total_income += interest.amount
    
    effective_rate = (total_tax / total_income) if total_income > 0 else 0.0
    
    return CalculationResult(
        year=profile.year,
        rules_version="2025.01",
        residency=profile.residency,
        total_tax=total_tax,
        effective_rate=effective_rate,
        by_regime=results,
        total_income=total_income
    )

