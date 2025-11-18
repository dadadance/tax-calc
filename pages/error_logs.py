"""Error logs page for the tax calculator."""
import streamlit as st
from tax_core.error_logger import logger
import json
from datetime import datetime


st.set_page_config(
    page_title="Error Logs - Tax Calculator",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Error Logs")
st.caption("View and manage application error logs")

# Get stats
stats = logger.get_log_stats()

# Stats cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Errors", stats["total_errors"])

with col2:
    error_types_count = len(stats["errors_by_type"])
    st.metric("Error Types", error_types_count)

with col3:
    actions_count = len(stats["errors_by_action"])
    st.metric("User Actions", actions_count)

with col4:
    if stats["latest_error"]:
        latest_time = stats["latest_error"].get("timestamp", "N/A")
        if latest_time != "N/A":
            try:
                dt = datetime.fromisoformat(latest_time)
                latest_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass
        st.caption(f"Latest: {latest_time}")
    else:
        st.caption("Latest: None")

st.divider()

# Error breakdown
if stats["total_errors"] > 0:
    tab1, tab2, tab3 = st.tabs(["Recent Errors", "By Type", "By Action"])
    
    with tab1:
        st.subheader("Recent Errors")
        
        num_errors = st.slider("Number of errors to show", 1, 100, 10, key="num_errors")
        errors = logger.get_recent_errors(limit=num_errors)
        
        if errors:
            for i, error_data in enumerate(errors, 1):
                with st.expander(
                    f"[{i}] {error_data.get('error_type', 'Unknown')}: {error_data.get('error_message', 'No message')[:100]}",
                    expanded=False
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Error ID:** `{error_data.get('error_id', 'N/A')}`")
                        st.write(f"**Timestamp:** {error_data.get('timestamp', 'N/A')}")
                        st.write(f"**Type:** `{error_data.get('error_type', 'N/A')}`")
                        st.write(f"**Message:** {error_data.get('error_message', 'N/A')}")
                        st.write(f"**User Action:** {error_data.get('user_action', 'N/A')}")
                        
                        context = error_data.get('context', {})
                        if context:
                            st.write("**Context:**")
                            st.json(context)
                        
                        traceback = error_data.get('traceback', '')
                        if traceback:
                            st.write("**Traceback:**")
                            st.code(traceback, language='python')
                    
                    with col2:
                        if st.button("Copy Error ID", key=f"copy_{error_data.get('error_id')}"):
                            st.code(error_data.get('error_id', ''), language=None)
        else:
            st.info("No errors found.")
    
    with tab2:
        st.subheader("Errors by Type")
        
        if stats["errors_by_type"]:
            error_types_data = {
                "Error Type": list(stats["errors_by_type"].keys()),
                "Count": list(stats["errors_by_type"].values())
            }
            st.dataframe(error_types_data, use_container_width=True, hide_index=True)
            
            # Show errors for selected type
            selected_type = st.selectbox(
                "View errors of type:",
                list(stats["errors_by_type"].keys())
            )
            
            if selected_type:
                all_errors = logger.get_recent_errors(limit=10000)
                type_errors = [e for e in all_errors if e.get('error_type') == selected_type]
                
                st.write(f"Found {len(type_errors)} error(s) of type `{selected_type}`:")
                for error_data in type_errors[:10]:  # Show first 10
                    with st.expander(f"{error_data.get('timestamp', 'N/A')}: {error_data.get('error_message', 'N/A')[:80]}"):
                        st.json(error_data)
        else:
            st.info("No errors by type.")
    
    with tab3:
        st.subheader("Errors by User Action")
        
        if stats["errors_by_action"]:
            actions_data = {
                "User Action": list(stats["errors_by_action"].keys()),
                "Count": list(stats["errors_by_action"].values())
            }
            st.dataframe(actions_data, use_container_width=True, hide_index=True)
            
            # Show errors for selected action
            selected_action = st.selectbox(
                "View errors for action:",
                list(stats["errors_by_action"].keys())
            )
            
            if selected_action:
                all_errors = logger.get_recent_errors(limit=10000)
                action_errors = [e for e in all_errors if e.get('user_action') == selected_action]
                
                st.write(f"Found {len(action_errors)} error(s) for action `{selected_action}`:")
                for error_data in action_errors[:10]:  # Show first 10
                    with st.expander(f"{error_data.get('timestamp', 'N/A')}: {error_data.get('error_message', 'N/A')[:80]}"):
                        st.json(error_data)
        else:
            st.info("No errors by action.")
    
    st.divider()
    
    # Clear logs button
    st.subheader("Manage Logs")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Logs", type="primary", use_container_width=True):
            if logger.clear_logs():
                st.success("✓ Logs cleared successfully!")
                st.rerun()
            else:
                st.error("✗ Failed to clear logs.")
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Export logs
    st.subheader("Export Logs")
    all_errors = logger.get_recent_errors(limit=10000)
    
    if all_errors:
        json_str = json.dumps(all_errors, indent=2, default=str)
        st.download_button(
            label="📥 Download Logs as JSON",
            data=json_str,
            file_name=f"error_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
else:
    st.success("🎉 No errors logged! The application is running smoothly.")
    
    if st.button("🔄 Refresh"):
        st.rerun()

