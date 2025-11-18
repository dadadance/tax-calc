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
from tax_core.example_profiles import EXAMPLE_PROFILES, get_example_profile
from tax_core.profile_db import save_profile, load_profile, list_profiles, delete_profile, get_profile_info, init_db


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
    
    # Example Profiles Loader
    st.subheader("📋 Example Profiles")
    st.caption("Load example profiles to see how calculations work")
    
    profile_options = ["None (Start Fresh)"] + [EXAMPLE_PROFILES[k]["name"] for k in EXAMPLE_PROFILES.keys()]
    selected_example = st.selectbox(
        "Load Example Profile",
        profile_options,
        index=0,
        key="example_profile_selector",
        help="Select an example profile to quickly populate the form with sample data"
    )
    
    # Track previous selection to detect change to "None (Start Fresh)"
    if 'previous_profile_selection' not in st.session_state:
        st.session_state.previous_profile_selection = selected_example
    
    # If user switched to "None (Start Fresh)", clear all inputs
    if selected_example == "None (Start Fresh)" and st.session_state.previous_profile_selection != "None (Start Fresh)":
        st.session_state.salary_inputs = []
        st.session_state.micro_inputs = []
        st.session_state.small_inputs = []
        st.session_state.rental_inputs = []
        st.session_state.cg_inputs = []
        st.session_state.dividends_inputs = []
        st.session_state.interest_inputs = []
        st.session_state.property_inputs = []
        st.session_state.previous_profile_selection = selected_example
        st.rerun()
    
    # Update previous selection
    st.session_state.previous_profile_selection = selected_example
    
    if selected_example != "None (Start Fresh)":
        # Find the profile key
        profile_key = None
        for key, data in EXAMPLE_PROFILES.items():
            if data["name"] == selected_example:
                profile_key = key
                break
        
        if profile_key and st.button("🔄 Load Profile", use_container_width=True):
            example_data = EXAMPLE_PROFILES[profile_key]
            example_profile = example_data["profile"]
            
            # Clear existing inputs
            st.session_state.salary_inputs = []
            st.session_state.micro_inputs = []
            st.session_state.small_inputs = []
            st.session_state.rental_inputs = []
            st.session_state.cg_inputs = []
            st.session_state.dividends_inputs = []
            st.session_state.interest_inputs = []
            st.session_state.property_inputs = []
            
            # Populate salary
            for salary in example_profile.salary:
                st.session_state.salary_inputs.append({
                    'monthly_gross': salary.monthly_gross,
                    'months': salary.months,
                    'pension_rate': salary.pension_employee_rate
                })
            
            # Populate micro business
            for micro in example_profile.micro_business:
                st.session_state.micro_inputs.append({
                    'turnover': micro.turnover,
                    'no_employees': micro.no_employees,
                    'activity_allowed': micro.activity_allowed
                })
            
            # Populate small business
            for small in example_profile.small_business:
                st.session_state.small_inputs.append({
                    'turnover': small.turnover,
                    'registered': small.registered
                })
            
            # Populate rental
            for rental in example_profile.rental:
                st.session_state.rental_inputs.append({
                    'monthly_rent': rental.monthly_rent,
                    'months': rental.months,
                    'special_5_percent': rental.special_5_percent
                })
            
            # Populate capital gains
            for cg in example_profile.capital_gains:
                st.session_state.cg_inputs.append({
                    'purchase_price': cg.purchase_price,
                    'sale_price': cg.sale_price,
                    'is_primary_residence': cg.is_primary_residence
                })
            
            # Populate dividends
            for div in example_profile.dividends:
                st.session_state.dividends_inputs.append({
                    'amount': div.amount
                })
            
            # Populate interest
            for interest in example_profile.interest:
                st.session_state.interest_inputs.append({
                    'amount': interest.amount
                })
            
            # Populate property tax
            for prop in example_profile.property_tax:
                st.session_state.property_inputs.append({
                    'family_income': prop.family_income,
                    'properties': prop.properties
                })
            
            # Update tax year and residency in session state
            st.session_state.example_tax_year = example_profile.year
            st.session_state.example_residency = "Resident" if example_profile.residency == ResidencyStatus.RESIDENT else "Non-resident"
            
            st.success(f"✓ Loaded: {example_data['name']}")
            st.info(f"💡 {example_data['description']}")
            # Update previous selection
            st.session_state.previous_profile_selection = selected_example
            st.rerun()
    
    if selected_example != "None (Start Fresh)":
        # Show profile description
        for key, data in EXAMPLE_PROFILES.items():
            if data["name"] == selected_example:
                st.caption(f"**{data['description']}**")
                break
    
    st.divider()
    
    # Tax year and residency (use example values if loaded)
    tax_years = [2024, 2025, 2026, 2027, 2028]
    default_year_idx = 1  # Default to 2025
    
    if 'example_tax_year' in st.session_state:
        try:
            default_year_idx = tax_years.index(st.session_state.example_tax_year)
        except ValueError:
            default_year_idx = 1
    
    tax_year = st.selectbox(
        "Tax Year", 
        tax_years, 
        index=default_year_idx
    )
    
    default_residency_idx = 0
    if 'example_residency' in st.session_state:
        default_residency_idx = 0 if st.session_state.example_residency == "Resident" else 1
    
    residency = st.radio(
        "Residency Status",
        ["Resident", "Non-resident"],
        index=default_residency_idx
    )
    
    st.divider()
    st.caption(f"Rules Version: v{tax_year}.01")
    st.caption("Currency: GEL (Georgian Lari)")
    
    st.divider()
    
    # Saved Profiles Section
    st.subheader("💾 Saved Profiles")
    st.caption("Save and load your profiles")
    
    # Initialize DB if needed
    try:
        init_db()
    except Exception:
        pass  # DB might already exist
    
    # Save current profile
    with st.expander("💾 Save Current Profile", expanded=False):
        profile_name = st.text_input(
            "Profile Name",
            key="save_profile_name",
            placeholder="e.g., My Tax Profile 2025",
            help="Enter a unique name for this profile"
        )
        profile_description = st.text_area(
            "Description (optional)",
            key="save_profile_desc",
            placeholder="Brief description of this profile",
            max_chars=200
        )
        
        if st.button("💾 Save Profile", use_container_width=True, key="save_profile_btn"):
            if not profile_name or not profile_name.strip():
                st.error("Please enter a profile name")
            else:
                try:
                    # Build profile from current inputs
                    profile_to_save = UserProfile(
                        year=tax_year,
                        residency=ResidencyStatus.RESIDENT if residency == "Resident" else ResidencyStatus.NON_RESIDENT,
                        salary=[SalaryIncome(
                            monthly_gross=s.get('monthly_gross', 0),
                            months=s.get('months', 0),
                            pension_employee_rate=s.get('pension_rate', 0.02)
                        ) for s in st.session_state.salary_inputs],
                        micro_business=[MicroBusinessIncome(
                            turnover=m.get('turnover', 0),
                            no_employees=m.get('no_employees', False),
                            activity_allowed=m.get('activity_allowed', False)
                        ) for m in st.session_state.micro_inputs],
                        small_business=[SmallBusinessIncome(
                            turnover=s.get('turnover', 0),
                            registered=s.get('registered', False)
                        ) for s in st.session_state.small_inputs],
                        rental=[RentalIncome(
                            monthly_rent=r.get('monthly_rent', 0),
                            months=r.get('months', 0),
                            special_5_percent=r.get('special_5_percent', False)
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
                    
                    save_profile(profile_name.strip(), profile_to_save, profile_description.strip())
                    st.success(f"✓ Profile '{profile_name}' saved successfully!")
                    st.rerun()
                except Exception as e:
                    log_app_error(e, user_action="Save Profile", profile_name=profile_name)
                    st.error(f"Error saving profile: {str(e)}")
    
    # Load saved profiles
    saved_profiles = list_profiles()
    if saved_profiles:
        with st.expander("📂 Load Saved Profile", expanded=False):
            profile_names = [p["name"] for p in saved_profiles]
            selected_saved = st.selectbox(
                "Select Profile",
                ["None"] + profile_names,
                key="load_profile_select"
            )
            
            if selected_saved != "None":
                profile_info = get_profile_info(selected_saved)
                if profile_info:
                    st.caption(f"**Description:** {profile_info['description'] or 'No description'}")
                    st.caption(f"**Updated:** {profile_info['updated_at']}")
                    
                    # Show income summary
                    summary = profile_info['income_summary']
                    income_types = []
                    if summary['salary_count'] > 0:
                        income_types.append(f"{summary['salary_count']} salary")
                    if summary['micro_business_count'] > 0:
                        income_types.append(f"{summary['micro_business_count']} micro")
                    if summary['small_business_count'] > 0:
                        income_types.append(f"{summary['small_business_count']} small")
                    if summary['rental_count'] > 0:
                        income_types.append(f"{summary['rental_count']} rental")
                    if summary['capital_gains_count'] > 0:
                        income_types.append(f"{summary['capital_gains_count']} CG")
                    if summary['dividends_count'] > 0:
                        income_types.append(f"{summary['dividends_count']} dividends")
                    if summary['interest_count'] > 0:
                        income_types.append(f"{summary['interest_count']} interest")
                    if summary['property_tax_count'] > 0:
                        income_types.append(f"{summary['property_tax_count']} property")
                    
                    if income_types:
                        st.caption(f"**Income sources:** {', '.join(income_types)}")
                
                if st.button("📂 Load Profile", use_container_width=True, key="load_profile_btn"):
                    try:
                        loaded_profile = load_profile(selected_saved)
                        if loaded_profile:
                            # Clear existing inputs
                            st.session_state.salary_inputs = []
                            st.session_state.micro_inputs = []
                            st.session_state.small_inputs = []
                            st.session_state.rental_inputs = []
                            st.session_state.cg_inputs = []
                            st.session_state.dividends_inputs = []
                            st.session_state.interest_inputs = []
                            st.session_state.property_inputs = []
                            
                            # Populate from loaded profile
                            for salary in loaded_profile.salary:
                                st.session_state.salary_inputs.append({
                                    'monthly_gross': salary.monthly_gross,
                                    'months': salary.months,
                                    'pension_rate': salary.pension_employee_rate
                                })
                            
                            for micro in loaded_profile.micro_business:
                                st.session_state.micro_inputs.append({
                                    'turnover': micro.turnover,
                                    'no_employees': micro.no_employees,
                                    'activity_allowed': micro.activity_allowed
                                })
                            
                            for small in loaded_profile.small_business:
                                st.session_state.small_inputs.append({
                                    'turnover': small.turnover,
                                    'registered': small.registered
                                })
                            
                            for rental in loaded_profile.rental:
                                st.session_state.rental_inputs.append({
                                    'monthly_rent': rental.monthly_rent,
                                    'months': rental.months,
                                    'special_5_percent': rental.special_5_percent
                                })
                            
                            for cg in loaded_profile.capital_gains:
                                st.session_state.cg_inputs.append({
                                    'purchase_price': cg.purchase_price,
                                    'sale_price': cg.sale_price,
                                    'is_primary_residence': cg.is_primary_residence
                                })
                            
                            for div in loaded_profile.dividends:
                                st.session_state.dividends_inputs.append({
                                    'amount': div.amount
                                })
                            
                            for interest in loaded_profile.interest:
                                st.session_state.interest_inputs.append({
                                    'amount': interest.amount
                                })
                            
                            for prop in loaded_profile.property_tax:
                                st.session_state.property_inputs.append({
                                    'family_income': prop.family_income,
                                    'properties': prop.properties
                                })
                            
                            # Update tax year and residency
                            st.session_state.example_tax_year = loaded_profile.year
                            st.session_state.example_residency = "Resident" if loaded_profile.residency == ResidencyStatus.RESIDENT else "Non-resident"
                            
                            st.success(f"✓ Loaded profile: {selected_saved}")
                            st.rerun()
                    except Exception as e:
                        log_app_error(e, user_action="Load Profile", profile_name=selected_saved)
                        st.error(f"Error loading profile: {str(e)}")
        
        # Manage profiles
        with st.expander("🗑️ Manage Profiles", expanded=False):
            for profile in saved_profiles[:5]:  # Show first 5
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"**{profile['name']}**")
                    if profile['description']:
                        st.caption(profile['description'][:50] + "..." if len(profile['description']) > 50 else profile['description'])
                with col2:
                    if st.button("🗑️", key=f"delete_{profile['name']}", use_container_width=True, help=f"Delete {profile['name']}"):
                        try:
                            if delete_profile(profile['name']):
                                st.success(f"✓ Deleted: {profile['name']}")
                                st.rerun()
                            else:
                                st.error("Profile not found")
                        except Exception as e:
                            log_app_error(e, user_action="Delete Profile", profile_name=profile['name'])
                            st.error(f"Error deleting profile: {str(e)}")
    
    st.divider()
    st.caption("⚠️ **Disclaimer:**")
    st.caption("Unofficial calculator, may be outdated or simplified, not professional tax advice.")
    
    st.divider()
    # Navigation links
    st.caption("📚 **Tax Rules & Formulas** - See sidebar navigation")
    st.caption("📋 **Error Logs** - See sidebar navigation")

# Main content - Income Inputs
col_header1, col_header2 = st.columns([4, 1])
with col_header1:
    st.header("Income Inputs")
with col_header2:
    if st.button("🗑️ Clear All", use_container_width=True, help="Remove all income inputs"):
        try:
            st.session_state.salary_inputs = []
            st.session_state.micro_inputs = []
            st.session_state.small_inputs = []
            st.session_state.rental_inputs = []
            st.session_state.cg_inputs = []
            st.session_state.dividends_inputs = []
            st.session_state.interest_inputs = []
            st.session_state.property_inputs = []
            st.success("✓ All inputs cleared")
            st.rerun()
        except Exception as e:
            log_app_error(e, user_action="Clear All")
            st.error(f"Error clearing inputs: {str(e)}")

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
            with st.expander(f"Source {idx + 1}: {sal['monthly_gross']:,.0f} GEL/month × {sal['months']} months", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    edit_monthly = st.number_input(
                        "Monthly Gross Salary (GEL)",
                        min_value=0.0,
                        value=sal['monthly_gross'],
                        step=100.0,
                        key=f"edit_salary_monthly_{idx}"
                    )
                with col2:
                    edit_months = st.number_input(
                        "Months Worked",
                        min_value=1,
                        max_value=12,
                        value=sal['months'],
                        key=f"edit_salary_months_{idx}"
                    )
                edit_pension = st.number_input(
                    "Employee Pension Rate",
                    min_value=0.0,
                    max_value=0.1,
                    value=sal.get('pension_rate', 0.02),
                    step=0.01,
                    format="%.2f",
                    key=f"edit_salary_pension_{idx}"
                )
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                with col_btn1:
                    if st.button("✓ Update", key=f"update_salary_{idx}", use_container_width=True):
                        try:
                            st.session_state.salary_inputs[idx] = {
                                'monthly_gross': edit_monthly,
                                'months': int(edit_months),
                                'pension_rate': edit_pension
                            }
                            st.success("✓ Updated")
                            st.rerun()
                        except Exception as e:
                            log_app_error(e, user_action="Update Salary Source", index=idx)
                            st.error(f"Error updating: {str(e)}")
                with col_btn2:
                    if st.button("🗑️ Remove", key=f"remove_salary_{idx}", use_container_width=True):
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
            with st.expander(f"Business {idx + 1}: {micro['turnover']:,.0f} GEL turnover", expanded=False):
                edit_turnover = st.number_input(
                    "Annual Turnover (GEL)",
                    min_value=0.0,
                    value=micro['turnover'],
                    step=1000.0,
                    key=f"edit_micro_turnover_{idx}"
                )
                edit_no_employees = st.checkbox("No employees", value=micro.get('no_employees', True), key=f"edit_micro_no_employees_{idx}")
                edit_activity = st.checkbox("Activity allowed for micro regime", value=micro.get('activity_allowed', True), key=f"edit_micro_activity_{idx}")
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("✓ Update", key=f"update_micro_{idx}", use_container_width=True):
                        try:
                            st.session_state.micro_inputs[idx] = {
                                'turnover': edit_turnover,
                                'no_employees': edit_no_employees,
                                'activity_allowed': edit_activity
                            }
                            st.success("✓ Updated")
                            st.rerun()
                        except Exception as e:
                            log_app_error(e, user_action="Update Micro Business", index=idx)
                            st.error(f"Error updating: {str(e)}")
                with col_btn2:
                    if st.button("🗑️ Remove", key=f"remove_micro_{idx}", use_container_width=True):
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
            with st.expander(f"Business {idx + 1}: {small['turnover']:,.0f} GEL turnover", expanded=False):
                edit_turnover = st.number_input(
                    "Annual Turnover (GEL)",
                    min_value=0.0,
                    value=small['turnover'],
                    step=1000.0,
                    key=f"edit_small_turnover_{idx}"
                )
                edit_registered = st.checkbox("Registered as small business", value=small.get('registered', False), key=f"edit_small_registered_{idx}")
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("✓ Update", key=f"update_small_{idx}", use_container_width=True):
                        try:
                            st.session_state.small_inputs[idx] = {
                                'turnover': edit_turnover,
                                'registered': edit_registered
                            }
                            st.success("✓ Updated")
                            st.rerun()
                        except Exception as e:
                            log_app_error(e, user_action="Update Small Business", index=idx)
                            st.error(f"Error updating: {str(e)}")
                with col_btn2:
                    if st.button("🗑️ Remove", key=f"remove_small_{idx}", use_container_width=True):
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
            with st.expander(f"Property {idx + 1}: {rental['monthly_rent']:,.0f} GEL/month × {rental['months']} months", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    edit_monthly_rent = st.number_input(
                        "Monthly Rent (GEL)",
                        min_value=0.0,
                        value=rental['monthly_rent'],
                        step=100.0,
                        key=f"edit_rental_monthly_{idx}"
                    )
                with col2:
                    edit_months = st.number_input(
                        "Months",
                        min_value=1,
                        max_value=12,
                        value=rental['months'],
                        key=f"edit_rental_months_{idx}"
                    )
                edit_special = st.checkbox("5% special regime", value=rental.get('special_5_percent', False), key=f"edit_rental_special_{idx}")
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("✓ Update", key=f"update_rental_{idx}", use_container_width=True):
                        try:
                            st.session_state.rental_inputs[idx] = {
                                'monthly_rent': edit_monthly_rent,
                                'months': int(edit_months),
                                'special_5_percent': edit_special
                            }
                            st.success("✓ Updated")
                            st.rerun()
                        except Exception as e:
                            log_app_error(e, user_action="Update Rental", index=idx)
                            st.error(f"Error updating: {str(e)}")
                with col_btn2:
                    if st.button("🗑️ Remove", key=f"remove_rental_{idx}", use_container_width=True):
                        try:
                            st.session_state.rental_inputs.pop(idx)
                            st.rerun()
                        except (IndexError, KeyError) as e:
                            log_app_error(e, user_action="Remove Rental", index=idx)
                            st.error(f"Error removing rental: {str(e)}")
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
            try:
                gain = cg.get('sale_price', 0) - cg.get('purchase_price', 0)
                residence_note = " (Primary Residence - Exempt)" if cg.get('is_primary_residence', False) else ""
                with st.expander(f"Transaction {idx + 1}: {gain:,.0f} GEL gain{residence_note}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_purchase = st.number_input(
                            "Purchase Price (GEL)",
                            min_value=0.0,
                            value=cg.get('purchase_price', 0),
                            step=1000.0,
                            key=f"edit_cg_purchase_{idx}"
                        )
                    with col2:
                        edit_sale = st.number_input(
                            "Sale Price (GEL)",
                            min_value=0.0,
                            value=cg.get('sale_price', 0),
                            step=1000.0,
                            key=f"edit_cg_sale_{idx}"
                        )
                    edit_primary = st.checkbox("Primary residence (exempt)", value=cg.get('is_primary_residence', False), key=f"edit_cg_primary_{idx}")
                    
                    col_btn1, col_btn2 = st.columns([1, 1])
                    with col_btn1:
                        if st.button("✓ Update", key=f"update_cg_{idx}", use_container_width=True):
                            try:
                                st.session_state.cg_inputs[idx] = {
                                    'purchase_price': edit_purchase,
                                    'sale_price': edit_sale,
                                    'is_primary_residence': edit_primary
                                }
                                st.success("✓ Updated")
                                st.rerun()
                            except Exception as e:
                                log_app_error(e, user_action="Update Capital Gains", index=idx)
                                st.error(f"Error updating: {str(e)}")
                    with col_btn2:
                        if st.button("🗑️ Remove", key=f"remove_cg_{idx}", use_container_width=True):
                            try:
                                st.session_state.cg_inputs.pop(idx)
                                st.rerun()
                            except (IndexError, KeyError) as e:
                                log_app_error(e, user_action="Remove Capital Gains", index=idx)
                                st.error(f"Error removing capital gains: {str(e)}")
                                st.rerun()
            except (KeyError, TypeError) as e:
                log_app_error(e, user_action="Display Capital Gain", index=idx, cg_data=cg)
                st.write(f"**Transaction {idx + 1}:** Error displaying gain")

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
            with st.expander(f"Dividends {idx + 1}: {div['amount']:,.0f} GEL", expanded=False):
                edit_amount = st.number_input(
                    "Dividends Amount (GEL)",
                    min_value=0.0,
                    value=div['amount'],
                    step=100.0,
                    key=f"edit_dividends_amount_{idx}"
                )
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("✓ Update", key=f"update_dividends_{idx}", use_container_width=True):
                        try:
                            st.session_state.dividends_inputs[idx] = {
                                'amount': edit_amount
                            }
                            st.success("✓ Updated")
                            st.rerun()
                        except Exception as e:
                            log_app_error(e, user_action="Update Dividends", index=idx)
                            st.error(f"Error updating: {str(e)}")
                with col_btn2:
                    if st.button("🗑️ Remove", key=f"remove_dividends_{idx}", use_container_width=True):
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
            with st.expander(f"Interest {idx + 1}: {interest['amount']:,.0f} GEL", expanded=False):
                edit_amount = st.number_input(
                    "Interest Amount (GEL)",
                    min_value=0.0,
                    value=interest['amount'],
                    step=100.0,
                    key=f"edit_interest_amount_{idx}"
                )
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("✓ Update", key=f"update_interest_{idx}", use_container_width=True):
                        try:
                            st.session_state.interest_inputs[idx] = {
                                'amount': edit_amount
                            }
                            st.success("✓ Updated")
                            st.rerun()
                        except Exception as e:
                            log_app_error(e, user_action="Update Interest", index=idx)
                            st.error(f"Error updating: {str(e)}")
                with col_btn2:
                    if st.button("🗑️ Remove", key=f"remove_interest_{idx}", use_container_width=True):
                        try:
                            st.session_state.interest_inputs.pop(idx)
                            st.rerun()
                        except (IndexError, KeyError) as e:
                            log_app_error(e, user_action="Remove Interest", index=idx)
                            st.error(f"Error removing interest: {str(e)}")
                            st.rerun()

# Helper function to calculate total income from all sources
def calculate_total_family_income():
    """Calculate total family income from all entered sources."""
    total = 0.0
    
    # Salary income
    for s in st.session_state.salary_inputs:
        total += s.get('monthly_gross', 0) * s.get('months', 0)
    
    # Micro business turnover
    for m in st.session_state.micro_inputs:
        total += m.get('turnover', 0)
    
    # Small business turnover
    for s in st.session_state.small_inputs:
        total += s.get('turnover', 0)
    
    # Rental income
    for r in st.session_state.rental_inputs:
        total += r.get('monthly_rent', 0) * r.get('months', 0)
    
    # Capital gains (only gains, not total sale price)
    for cg in st.session_state.cg_inputs:
        sale = cg.get('sale_price', 0)
        purchase = cg.get('purchase_price', 0)
        if sale > purchase:
            total += sale - purchase
    
    # Dividends
    for d in st.session_state.dividends_inputs:
        total += d.get('amount', 0)
    
    # Interest
    for i in st.session_state.interest_inputs:
        total += i.get('amount', 0)
    
    return total

# Property Tax tab
with tab8:
    st.subheader("Property Tax")
    st.caption("ℹ️ Property tax is calculated based on family income threshold (65,000 GEL)")
    
    # Auto-calculate total family income from all sources
    calculated_family_income = calculate_total_family_income()
    
    # Show calculated income summary
    if calculated_family_income > 0:
        st.info(f"💰 **Auto-calculated Family Income:** {calculated_family_income:,.2f} GEL (from all income sources)")
        threshold = 65000.0
        if calculated_family_income > threshold:
            st.success(f"✓ Your family income ({calculated_family_income:,.2f} GEL) exceeds the threshold ({threshold:,.0f} GEL). Property tax will apply.")
        else:
            st.warning(f"⚠️ Your family income ({calculated_family_income:,.2f} GEL) is below the threshold ({threshold:,.0f} GEL). You may be exempt from property tax.")
    
    with st.expander("Add Property Tax Info", expanded=True):
        st.caption("💡 **Note:** Family income is automatically calculated from all your income sources above. You can override it below if needed (e.g., if you have other family members' income not entered).")
        
        use_calculated = st.checkbox(
            "Use auto-calculated family income",
            value=True,
            key="use_calculated_income",
            help="Use the total income calculated from all entered sources"
        )
        
        if use_calculated:
            family_income = calculated_family_income
            st.caption(f"**Using calculated income:** {family_income:,.2f} GEL")
        else:
            family_income = st.number_input(
                "Manual Family Income Override (GEL)",
                min_value=0.0,
                value=calculated_family_income if calculated_family_income > 0 else 65000.0,
                step=1000.0,
                key="property_income_manual",
                help="Override the calculated income if you have additional family income sources not entered above"
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
                    'properties': int(properties),
                    'use_calculated': use_calculated
                })
                st.success(f"Added property tax info: {properties} properties")
                st.rerun()
            except Exception as e:
                log_app_error(e, user_action="Add Property Tax Info", family_income=family_income, properties=properties)
                st.error(f"Error adding property tax info: {str(e)}")
    
    if st.session_state.property_inputs:
        st.subheader("Current Property Tax Info")
        for idx, prop in enumerate(st.session_state.property_inputs):
            # Use calculated income if it's set to auto-update
            if prop.get('use_calculated', False):
                current_family_income = calculated_family_income
            else:
                current_family_income = prop.get('family_income', 0)
            
            properties = prop.get('properties', 0)
            threshold = 65000.0
            status = "⚠️ Exempt (below threshold)" if current_family_income <= threshold else "✓ Taxable (above threshold)"
            
            income_source_note = " (auto-calculated)" if prop.get('use_calculated', False) else " (manual)"
            with st.expander(f"Info {idx + 1}: {properties} properties, {current_family_income:,.0f} GEL family income{income_source_note} - {status}", expanded=False):
                use_calculated_edit = st.checkbox(
                    "Use auto-calculated family income",
                    value=prop.get('use_calculated', False),
                    key=f"edit_use_calculated_{idx}",
                    help="Automatically use total income from all sources"
                )
                
                if use_calculated_edit:
                    edit_family_income = calculated_family_income
                    st.caption(f"**Using calculated income:** {edit_family_income:,.2f} GEL")
                else:
                    edit_family_income = st.number_input(
                        "Manual Family Income Override (GEL)",
                        min_value=0.0,
                        value=prop.get('family_income', calculated_family_income),
                        step=1000.0,
                        key=f"edit_property_income_{idx}",
                        help="Override the calculated income if needed"
                    )
                
                edit_properties = st.number_input(
                    "Number of Properties",
                    min_value=0,
                    value=properties,
                    key=f"edit_property_count_{idx}"
                )
                
                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("✓ Update", key=f"update_property_{idx}", use_container_width=True):
                        try:
                            st.session_state.property_inputs[idx] = {
                                'family_income': edit_family_income,
                                'properties': int(edit_properties),
                                'use_calculated': use_calculated_edit
                            }
                            st.success("✓ Updated")
                            st.rerun()
                        except Exception as e:
                            log_app_error(e, user_action="Update Property Tax Info", index=idx)
                            st.error(f"Error updating: {str(e)}")
                with col_btn2:
                    if st.button("🗑️ Remove", key=f"remove_property_{idx}", use_container_width=True):
                        try:
                            st.session_state.property_inputs.pop(idx)
                            st.rerun()
                        except (IndexError, KeyError) as e:
                            log_app_error(e, user_action="Remove Property Tax Info", index=idx)
                            st.error(f"Error removing property tax info: {str(e)}")
                            st.rerun()
    else:
        if calculated_family_income > 0:
            st.info(f"💡 **Tip:** Your calculated family income is {calculated_family_income:,.2f} GEL. Add property information above to calculate property tax.")
        else:
            st.info("💡 **No property tax info added yet.** Add your income sources in other tabs, then add property information here to calculate property tax.")

# Summary Section - Show all entered data
st.divider()
st.header("📊 Income Summary")
st.caption("Overview of all entered income sources")

total_calculated_income = calculate_total_family_income()

if total_calculated_income > 0 or any([
    st.session_state.salary_inputs,
    st.session_state.micro_inputs,
    st.session_state.small_inputs,
    st.session_state.rental_inputs,
    st.session_state.cg_inputs,
    st.session_state.dividends_inputs,
    st.session_state.interest_inputs,
    st.session_state.property_inputs
]):
    summary_cols = st.columns(4)
    
    with summary_cols[0]:
        salary_total = sum(s.get('monthly_gross', 0) * s.get('months', 0) for s in st.session_state.salary_inputs)
        st.metric("Salary Income", f"{salary_total:,.2f} GEL", delta=f"{len(st.session_state.salary_inputs)} source(s)")
    
    with summary_cols[1]:
        business_total = (
            sum(m.get('turnover', 0) for m in st.session_state.micro_inputs) +
            sum(s.get('turnover', 0) for s in st.session_state.small_inputs)
        )
        business_count = len(st.session_state.micro_inputs) + len(st.session_state.small_inputs)
        st.metric("Business Income", f"{business_total:,.2f} GEL", delta=f"{business_count} business(es)")
    
    with summary_cols[2]:
        rental_total = sum(r.get('monthly_rent', 0) * r.get('months', 0) for r in st.session_state.rental_inputs)
        st.metric("Rental Income", f"{rental_total:,.2f} GEL", delta=f"{len(st.session_state.rental_inputs)} property(ies)")
    
    with summary_cols[3]:
        investment_total = (
            sum(d.get('amount', 0) for d in st.session_state.dividends_inputs) +
            sum(i.get('amount', 0) for i in st.session_state.interest_inputs) +
            sum(max(0, cg.get('sale_price', 0) - cg.get('purchase_price', 0)) for cg in st.session_state.cg_inputs)
        )
        investment_count = (
            len(st.session_state.dividends_inputs) +
            len(st.session_state.interest_inputs) +
            len([cg for cg in st.session_state.cg_inputs if cg.get('sale_price', 0) > cg.get('purchase_price', 0)])
        )
        st.metric("Investment Income", f"{investment_total:,.2f} GEL", delta=f"{investment_count} source(s)")
    
    st.divider()
    
    # Detailed breakdown
    with st.expander("📋 Detailed Income Breakdown", expanded=False):
        breakdown_data = []
        
        # Salary
        for idx, s in enumerate(st.session_state.salary_inputs):
            annual = s.get('monthly_gross', 0) * s.get('months', 0)
            breakdown_data.append({
                "Type": "Salary",
                "Description": f"Source {idx + 1}: {s.get('monthly_gross', 0):,.0f} GEL/month × {s.get('months', 0)} months",
                "Amount (GEL)": f"{annual:,.2f}"
            })
        
        # Micro Business
        for idx, m in enumerate(st.session_state.micro_inputs):
            breakdown_data.append({
                "Type": "Micro Business",
                "Description": f"Business {idx + 1}: {m.get('turnover', 0):,.0f} GEL turnover",
                "Amount (GEL)": f"{m.get('turnover', 0):,.2f}"
            })
        
        # Small Business
        for idx, s in enumerate(st.session_state.small_inputs):
            breakdown_data.append({
                "Type": "Small Business",
                "Description": f"Business {idx + 1}: {s.get('turnover', 0):,.0f} GEL turnover",
                "Amount (GEL)": f"{s.get('turnover', 0):,.2f}"
            })
        
        # Rental
        for idx, r in enumerate(st.session_state.rental_inputs):
            annual = r.get('monthly_rent', 0) * r.get('months', 0)
            breakdown_data.append({
                "Type": "Rental",
                "Description": f"Property {idx + 1}: {r.get('monthly_rent', 0):,.0f} GEL/month × {r.get('months', 0)} months",
                "Amount (GEL)": f"{annual:,.2f}"
            })
        
        # Capital Gains
        for idx, cg in enumerate(st.session_state.cg_inputs):
            gain = max(0, cg.get('sale_price', 0) - cg.get('purchase_price', 0))
            if gain > 0:
                breakdown_data.append({
                    "Type": "Capital Gains",
                    "Description": f"Transaction {idx + 1}: {gain:,.0f} GEL gain",
                    "Amount (GEL)": f"{gain:,.2f}"
                })
        
        # Dividends
        for idx, d in enumerate(st.session_state.dividends_inputs):
            breakdown_data.append({
                "Type": "Dividends",
                "Description": f"Dividends {idx + 1}",
                "Amount (GEL)": f"{d.get('amount', 0):,.2f}"
            })
        
        # Interest
        for idx, i in enumerate(st.session_state.interest_inputs):
            breakdown_data.append({
                "Type": "Interest",
                "Description": f"Interest {idx + 1}",
                "Amount (GEL)": f"{i.get('amount', 0):,.2f}"
            })
        
        if breakdown_data:
            # Create dataframe using Streamlit's built-in dataframe
            st.dataframe(breakdown_data, use_container_width=True, hide_index=True)
            
            st.caption(f"**Total Family Income:** {total_calculated_income:,.2f} GEL")
        else:
            st.caption("No income sources entered yet.")
    
    st.caption(f"💡 **Total Calculated Family Income:** {total_calculated_income:,.2f} GEL (used for property tax calculation)")
else:
    st.info("💡 Enter income sources in the tabs above to see your income summary here.")

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
            family_income=p.get('family_income', calculate_total_family_income()) if not p.get('use_calculated', False) else calculate_total_family_income(),
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

