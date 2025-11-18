"""Streamlit app for Georgian Tax Calculator."""
import streamlit as st
from tax_core.models import (
    UserProfile,
    ResidencyStatus,
    SalaryIncome,
    MicroBusinessIncome,
    SmallBusinessIncome,
    RentalIncome,
    CapitalGainsIncome,
    DividendsIncome,
    InterestIncome,
    PropertyTaxInput,
)
from tax_core.calculators import calculate_all
from tax_core.error_logger import log_app_error


# Page config
st.set_page_config(
    page_title="Georgian Tax Calculator",
    page_icon="🇬🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🇬🇪 Georgian Tax Calculator")
st.subheader("For individuals – unofficial estimation tool")

# Sidebar - Profile & Settings
with st.sidebar:
    st.header("Profile & Settings")
    
    tax_year = st.selectbox("Tax Year", [2024, 2025], index=1)
    residency = st.radio(
        "Residency Status",
        ["Resident", "Non-resident"],
        index=0
    )
    
    st.divider()
    st.caption(f"Rules Version: v{tax_year}.01")
    st.caption("Currency: GEL (Georgian Lari)")
    
    st.divider()
    st.caption("⚠️ **Disclaimer:**")
    st.caption("Unofficial calculator, may be outdated or simplified, not professional tax advice.")
    
    st.divider()
    # Link to error logs page - use navigation
    # Streamlit automatically creates navigation for pages in the pages/ directory
    # Users can access it via the sidebar navigation menu
    st.caption("📋 **Error Logs** available in sidebar navigation")

# Main content - Income Inputs
st.header("Income Inputs")

# Create tabs for different income types
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💰 Salary",
    "🏢 Micro Business",
    "🏪 Small Business",
    "🏠 Rental",
    "📈 Capital Gains",
    "💵 Dividends",
    "💎 Interest",
    "🏘️ Property Tax"
])

# Initialize session state for inputs
if 'salary_inputs' not in st.session_state:
    st.session_state.salary_inputs = []
if 'micro_inputs' not in st.session_state:
    st.session_state.micro_inputs = []
if 'small_inputs' not in st.session_state:
    st.session_state.small_inputs = []
if 'rental_inputs' not in st.session_state:
    st.session_state.rental_inputs = []
if 'cg_inputs' not in st.session_state:
    st.session_state.cg_inputs = []
if 'dividends_inputs' not in st.session_state:
    st.session_state.dividends_inputs = []
if 'interest_inputs' not in st.session_state:
    st.session_state.interest_inputs = []
if 'property_inputs' not in st.session_state:
    st.session_state.property_inputs = []

# Salary tab
with tab1:
    st.subheader("Salary / Employment Income")
    
    with st.expander("Add Salary Source", expanded=True):
        monthly_gross = st.number_input(
            "Monthly Gross Salary (GEL)",
            min_value=0.0,
            value=3000.0,
            step=100.0,
            key="salary_monthly"
        )
        months = st.number_input(
            "Months Worked",
            min_value=1,
            max_value=12,
            value=12,
            key="salary_months"
        )
        pension_rate = st.selectbox(
            "Employee Pension Contribution Rate",
            [0.02, 0.04],
            index=0,
            format_func=lambda x: f"{x * 100:.0f}%",
            key="salary_pension"
        )
        
        if st.button("Add Salary Source", key="add_salary"):
            try:
                st.session_state.salary_inputs.append({
                    'monthly_gross': monthly_gross,
                    'months': int(months),
                    'pension_rate': pension_rate
                })
                st.success(f"Added salary source: {monthly_gross:,.0f} GEL/month × {months} months")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Salary Source", monthly_gross=monthly_gross, months=months)
                st.error(f"Error adding salary source: {str(e)}")
    
    if st.session_state.salary_inputs:
        st.subheader("Current Salary Sources")
        for idx, sal in enumerate(st.session_state.salary_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Source {idx + 1}:** {sal['monthly_gross']:,.0f} GEL/month × {sal['months']} months")
            with col2:
                if st.button("Remove", key=f"remove_salary_{idx}"):
                    try:
                        st.session_state.salary_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Salary Source", index=idx)
                        st.error(f"Error removing salary source: {str(e)}")
                        st.rerun()

# Micro Business tab
with tab2:
    st.subheader("Micro Business")
    
    with st.expander("Add Micro Business", expanded=True):
        turnover = st.number_input(
            "Annual Turnover (GEL)",
            min_value=0.0,
            value=25000.0,
            step=1000.0,
            key="micro_turnover"
        )
        no_employees = st.checkbox("No employees", value=True, key="micro_no_employees")
        activity_allowed = st.checkbox("Activity allowed for micro regime", value=True, key="micro_activity")
        
        if st.button("Add Micro Business", key="add_micro"):
            try:
                st.session_state.micro_inputs.append({
                    'turnover': turnover,
                    'no_employees': no_employees,
                    'activity_allowed': activity_allowed
                })
                st.success(f"Added micro business: {turnover:,.0f} GEL turnover")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Micro Business", turnover=turnover)
                st.error(f"Error adding micro business: {str(e)}")
    
    if st.session_state.micro_inputs:
        st.subheader("Current Micro Businesses")
        for idx, micro in enumerate(st.session_state.micro_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Business {idx + 1}:** {micro['turnover']:,.0f} GEL turnover")
            with col2:
                if st.button("Remove", key=f"remove_micro_{idx}"):
                    try:
                        st.session_state.micro_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Micro Business", index=idx)
                        st.error(f"Error removing micro business: {str(e)}")
                        st.rerun()

# Small Business tab
with tab3:
    st.subheader("Small Business")
    
    with st.expander("Add Small Business", expanded=True):
        turnover = st.number_input(
            "Annual Turnover (GEL)",
            min_value=0.0,
            value=100000.0,
            step=10000.0,
            key="small_turnover"
        )
        registered = st.checkbox("Registered as small business", value=True, key="small_registered")
        
        if st.button("Add Small Business", key="add_small"):
            try:
                st.session_state.small_inputs.append({
                    'turnover': turnover,
                    'registered': registered
                })
                st.success(f"Added small business: {turnover:,.0f} GEL turnover")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Small Business", turnover=turnover)
                st.error(f"Error adding small business: {str(e)}")
    
    if st.session_state.small_inputs:
        st.subheader("Current Small Businesses")
        for idx, small in enumerate(st.session_state.small_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Business {idx + 1}:** {small['turnover']:,.0f} GEL turnover")
            with col2:
                if st.button("Remove", key=f"remove_small_{idx}"):
                    try:
                        st.session_state.small_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Small Business", index=idx)
                        st.error(f"Error removing small business: {str(e)}")
                        st.rerun()

# Rental tab
with tab4:
    st.subheader("Residential Rental Income")
    
    with st.expander("Add Rental Property", expanded=True):
        monthly_rent = st.number_input(
            "Monthly Rent (GEL)",
            min_value=0.0,
            value=800.0,
            step=50.0,
            key="rental_monthly"
        )
        months = st.number_input(
            "Months Rented",
            min_value=1,
            max_value=12,
            value=12,
            key="rental_months"
        )
        special_5_percent = st.checkbox("Apply 5% special regime", value=True, key="rental_5pct")
        
        if st.button("Add Rental Property", key="add_rental"):
            try:
                st.session_state.rental_inputs.append({
                    'monthly_rent': monthly_rent,
                    'months': int(months),
                    'special_5_percent': special_5_percent
                })
                st.success(f"Added rental property: {monthly_rent:,.0f} GEL/month × {months} months")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Rental Property", monthly_rent=monthly_rent, months=months)
                st.error(f"Error adding rental property: {str(e)}")
    
    if st.session_state.rental_inputs:
        st.subheader("Current Rental Properties")
        for idx, rental in enumerate(st.session_state.rental_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Property {idx + 1}:** {rental['monthly_rent']:,.0f} GEL/month × {rental['months']} months")
            with col2:
                if st.button("Remove", key=f"remove_rental_{idx}"):
                    try:
                        st.session_state.rental_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Rental Property", index=idx)
                        st.error(f"Error removing rental property: {str(e)}")
                        st.rerun()

# Capital Gains tab
with tab5:
    st.subheader("Capital Gains (Property/Vehicle)")
    
    with st.expander("Add Capital Gain", expanded=True):
        purchase_price = st.number_input(
            "Purchase Price (GEL)",
            min_value=0.0,
            value=100000.0,
            step=1000.0,
            key="cg_purchase"
        )
        sale_price = st.number_input(
            "Sale Price (GEL)",
            min_value=0.0,
            value=120000.0,
            step=1000.0,
            key="cg_sale"
        )
        is_primary = st.checkbox("Primary residence (exempt)", value=False, key="cg_primary")
        
        if st.button("Add Capital Gain", key="add_cg"):
            try:
                gain = sale_price - purchase_price
                st.session_state.cg_inputs.append({
                    'purchase_price': purchase_price,
                    'sale_price': sale_price,
                    'is_primary_residence': is_primary
                })
                st.success(f"Added capital gain: {gain:,.0f} GEL gain")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Capital Gain", purchase_price=purchase_price, sale_price=sale_price)
                st.error(f"Error adding capital gain: {str(e)}")
    
    if st.session_state.cg_inputs:
        st.subheader("Current Capital Gains")
        for idx, cg in enumerate(st.session_state.cg_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                try:
                    gain = cg.get('sale_price', 0) - cg.get('purchase_price', 0)
                    st.write(f"**Transaction {idx + 1}:** {gain:,.0f} GEL gain")
                except (KeyError, TypeError) as e:
                    log_app_error(e, user_action="Display Capital Gain", index=idx, cg_data=cg)
                    st.write(f"**Transaction {idx + 1}:** Error displaying gain")
            with col2:
                if st.button("Remove", key=f"remove_cg_{idx}"):
                    try:
                        st.session_state.cg_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Capital Gain", index=idx)
                        st.error(f"Error removing capital gain: {str(e)}")
                        st.rerun()

# Dividends tab
with tab6:
    st.subheader("Dividends Income")
    
    with st.expander("Add Dividends", expanded=True):
        amount = st.number_input(
            "Dividends Amount (GEL)",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            key="dividends_amount"
        )
        
        if st.button("Add Dividends", key="add_dividends"):
            try:
                st.session_state.dividends_inputs.append({
                    'amount': amount
                })
                st.success(f"Added dividends: {amount:,.0f} GEL")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Dividends", amount=amount)
                st.error(f"Error adding dividends: {str(e)}")
    
    if st.session_state.dividends_inputs:
        st.subheader("Current Dividends")
        for idx, div in enumerate(st.session_state.dividends_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Dividends {idx + 1}:** {div['amount']:,.0f} GEL")
            with col2:
                if st.button("Remove", key=f"remove_dividends_{idx}"):
                    try:
                        st.session_state.dividends_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Dividends", index=idx)
                        st.error(f"Error removing dividends: {str(e)}")
                        st.rerun()

# Interest tab
with tab7:
    st.subheader("Interest Income")
    
    with st.expander("Add Interest", expanded=True):
        amount = st.number_input(
            "Interest Amount (GEL)",
            min_value=0.0,
            value=1000.0,
            step=100.0,
            key="interest_amount"
        )
        
        if st.button("Add Interest", key="add_interest"):
            try:
                st.session_state.interest_inputs.append({
                    'amount': amount
                })
                st.success(f"Added interest: {amount:,.0f} GEL")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Interest", amount=amount)
                st.error(f"Error adding interest: {str(e)}")
    
    if st.session_state.interest_inputs:
        st.subheader("Current Interest")
        for idx, interest in enumerate(st.session_state.interest_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Interest {idx + 1}:** {interest['amount']:,.0f} GEL")
            with col2:
                if st.button("Remove", key=f"remove_interest_{idx}"):
                    try:
                        st.session_state.interest_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Interest", index=idx)
                        st.error(f"Error removing interest: {str(e)}")
                        st.rerun()

# Property Tax tab
with tab8:
    st.subheader("Property Tax")
    
    with st.expander("Add Property Tax Info", expanded=True):
        family_income = st.number_input(
            "Approximate Annual Family Income (GEL)",
            min_value=0.0,
            value=65000.0,
            step=1000.0,
            key="property_income"
        )
        properties = st.number_input(
            "Number of Properties",
            min_value=0,
            value=1,
            key="property_count"
        )
        
        if st.button("Add Property Tax Info", key="add_property"):
            try:
                st.session_state.property_inputs.append({
                    'family_income': family_income,
                    'properties': int(properties)
                })
                st.success(f"Added property tax info: {properties} properties")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Property Tax Info", family_income=family_income, properties=properties)
                st.error(f"Error adding property tax info: {str(e)}")
    
    if st.session_state.property_inputs:
        st.subheader("Current Property Tax Info")
        for idx, prop in enumerate(st.session_state.property_inputs):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Info {idx + 1}:** {prop['properties']} properties, {prop['family_income']:,.0f} GEL family income")
            with col2:
                if st.button("Remove", key=f"remove_property_{idx}"):
                    try:
                        st.session_state.property_inputs.pop(idx)
                        st.rerun()
                    except (IndexError, KeyError) as e:
                        log_app_error(e, user_action="Remove Property Tax Info", index=idx)
                        st.error(f"Error removing property tax info: {str(e)}")
                        st.rerun()

# Results Section
st.divider()
st.header("📊 Calculation Results")

# Build profile from inputs
try:
    profile = UserProfile(
        year=tax_year,
        residency=ResidencyStatus.RESIDENT if residency == "Resident" else ResidencyStatus.NON_RESIDENT,
        salary=[SalaryIncome(
            monthly_gross=s.get('monthly_gross', 0),
            months=s.get('months', 12),
            pension_employee_rate=s.get('pension_rate', 0.02)
        ) for s in st.session_state.salary_inputs],
        micro_business=[MicroBusinessIncome(
            turnover=m.get('turnover', 0),
            no_employees=m.get('no_employees', True),
            activity_allowed=m.get('activity_allowed', True)
        ) for m in st.session_state.micro_inputs],
        small_business=[SmallBusinessIncome(
            turnover=s.get('turnover', 0),
            registered=s.get('registered', True)
        ) for s in st.session_state.small_inputs],
        rental=[RentalIncome(
            monthly_rent=r.get('monthly_rent', 0),
            months=r.get('months', 12),
            special_5_percent=r.get('special_5_percent', True)
        ) for r in st.session_state.rental_inputs],
        capital_gains=[CapitalGainsIncome(
            purchase_price=cg.get('purchase_price', 0),
            sale_price=cg.get('sale_price', 0),
            is_primary_residence=cg.get('is_primary_residence', False)
        ) for cg in st.session_state.cg_inputs],
        dividends=[DividendsIncome(amount=d.get('amount', 0)) for d in st.session_state.dividends_inputs],
        interest=[InterestIncome(amount=i.get('amount', 0)) for i in st.session_state.interest_inputs],
        property_tax=[PropertyTaxInput(
            family_income=p.get('family_income', 0),
            properties=p.get('properties', 0)
        ) for p in st.session_state.property_inputs]
    )
except Exception as e:
    log_app_error(e, user_action="Build User Profile", 
                  tax_year=tax_year, residency=residency)
    st.error(f"Error building profile: {str(e)}")
    st.stop()

# Calculate
try:
    result = calculate_all(profile)
    
    # Summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tax Due", f"{result.total_tax:,.2f} GEL")
    
    with col2:
        st.metric("Total Income", f"{result.total_income:,.2f} GEL")
    
    with col3:
        st.metric("Effective Tax Rate", f"{result.effective_rate * 100:.2f}%")
    
    # Breakdown by regime
    st.subheader("Breakdown by Regime")
    
    if result.by_regime:
        # Sort by tax amount (descending) for better visibility
        sorted_regimes = sorted(result.by_regime, key=lambda x: x.tax, reverse=True)
        
        breakdown_data = {
            "Regime": [r.regime_id.replace("_", " ").title() for r in sorted_regimes],
            "Tax (GEL)": [f"{r.tax:,.2f}" for r in sorted_regimes],
            "Percentage": [f"{(r.tax / result.total_tax * 100):.1f}%" if result.total_tax > 0 else "0.0%" for r in sorted_regimes]
        }
        st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
        
        # Show summary of income sources
        st.caption(f"📊 **Total Income Sources:** {len([r for r in sorted_regimes if r.tax > 0])} regime(s) with taxable income")
        
        # Warnings
        all_warnings = []
        for regime in sorted_regimes:
            all_warnings.extend(regime.warnings)
        
        if all_warnings:
            st.warning("⚠️ **Warnings:**")
            for warning in all_warnings:
                st.warning(f"  • {warning}")
        
        # Step-by-step calculations
        st.subheader("Step-by-Step Calculations")
        st.caption("Click on each regime below to see detailed calculation steps")
        
        # Use sorted regimes for consistency
        for regime in sorted_regimes:
            if regime.steps:
                # Create a more descriptive title
                regime_name = regime.regime_id.replace("_", " ").title()
                tax_amount = f"{regime.tax:,.2f}"
                percentage = f"{(regime.tax / result.total_tax * 100):.1f}%" if result.total_tax > 0 else "0.0%"
                
                with st.expander(
                    f"📋 **{regime_name}** - Tax: {tax_amount} GEL ({percentage} of total)", 
                    expanded=False
                ):
                    # Show summary first
                    st.write(f"**Total Tax for {regime_name}:** {tax_amount} GEL")
                    if regime.warnings:
                        st.warning("⚠️ **Warnings:**")
                        for warning in regime.warnings:
                            st.warning(f"  • {warning}")
                    
                    st.divider()
                    st.write("**Calculation Steps:**")
                    
                    # Display steps in a table
                    steps_data = {
                        "Step": [step.id for step in regime.steps],
                        "Description": [step.description for step in regime.steps],
                        "Formula": [step.formula for step in regime.steps],
                        "Values": [step.values for step in regime.steps],
                        "Result (GEL)": [f"{step.result:,.2f}" for step in regime.steps]
                    }
                    st.dataframe(steps_data, use_container_width=True, hide_index=True)
                    
                    # Show legal references from steps if available
                    legal_refs = [step.legal_ref for step in regime.steps if step.legal_ref]
                    if legal_refs:
                        unique_refs = list(set(legal_refs))  # Remove duplicates
                        st.divider()
                        if len(unique_refs) == 1:
                            st.caption(f"**Legal Reference:** {unique_refs[0]}")
                        else:
                            st.caption("**Legal References:**")
                            for ref in unique_refs:
                                st.caption(f"  • {ref}")
    else:
        st.info("No income sources added. Please add income sources above to see calculations.")
        
except Exception as e:
    log_app_error(e, user_action="Calculate Taxes", 
                  tax_year=tax_year, residency=residency,
                  has_salary=len(st.session_state.salary_inputs) > 0,
                  has_micro=len(st.session_state.micro_inputs) > 0,
                  has_small=len(st.session_state.small_inputs) > 0)
    st.error(f"Error calculating taxes: {str(e)}")
    st.exception(e)
    st.info("💡 Check the Error Logs page for more details.")

# Footer
st.divider()
st.caption("**Disclaimer:** This is an unofficial calculator for estimation purposes only. Tax laws may change. Please verify calculations with RS.ge or consult a professional tax advisor.")
st.caption("**Links:** [RS.ge](https://www.rs.ge) | [RS.ge Tax Portal](https://www.rs.ge)")

