"""
Authentication Module untuk Dashboard Kelayakan Alat
Simple single-user authentication
"""

import streamlit as st
from config import USERS, ROLE_PERMISSIONS


def show_login_page():
    """Display login page"""
    
    # Hide default streamlit elements for cleaner login page
    st.markdown("""
    <style>
        .main > div {
            padding-top: 3rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo/Header
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #1f77b4; margin-bottom: 0;">⛺ Performance Dashboard</h1>
            <p style="color: #7f8c8d; font-size: 1.1rem;">Equipment Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form with clean container
        st.markdown("### 🔐 Login")
        st.markdown("")  # Spacer
        
        # Use form to enable Enter key submit
        with st.form(key="login_form", clear_on_submit=False):
            # Username input
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )
            
            # Password input
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            st.markdown("")  # Spacer
            
            # Login button (form submit)
            login_button = st.form_submit_button("🔑 Login", use_container_width=True, type="primary")
        
        # Handle login (outside form to avoid rerun issues)
        if login_button:
            if username and password:  # Check if fields are not empty
                user_data = authenticate(username, password)
                if user_data:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.display_name = user_data["display_name"]
                    st.session_state.user_role = user_data["role"]
                    # Clear any previous active_page to prevent unauthorized access
                    if 'active_page' in st.session_state:
                        del st.session_state.active_page
                    st.success(f"✅ Login successful! Welcome {user_data['display_name']}")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.warning("⚠️ Please enter both username and password")
        
        # Footer
        st.markdown("")  # Spacer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; color: #95a5a6;">
            <p>Dashboard Kelayakan Alat Camping</p>
            <p style="font-size: 0.9rem;">© 2026 - Sistem Informasi Perusahaan</p>
        </div>
        """, unsafe_allow_html=True)


def authenticate(username, password):
    """
    Validate user credentials
    
    Args:
        username (str): Username input
        password (str): Password input
    
    Returns:
        dict or None: User data if valid, None otherwise
    """
    if username in USERS:
        if USERS[username]["password"] == password:
            return USERS[username]
    return None


def check_authentication():
    """
    Check if user is authenticated
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    return st.session_state.get('logged_in', False)


def logout():
    """Logout user by clearing session state"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.display_name = None
    st.session_state.user_role = None
    # Clear active page to prevent unauthorized access after logout
    if 'active_page' in st.session_state:
        del st.session_state.active_page
    st.rerun()


def get_current_user():
    """
    Get current logged-in user display name
    
    Returns:
        str: User display name or None
    """
    return st.session_state.get('display_name', None)


def get_user_role():
    """
    Get current user role
    
    Returns:
        str: User role or None
    """
    return st.session_state.get('user_role', None)


def has_access(section):
    """
    Check if current user has access to a section
    
    Args:
        section (str): Section name ('executive', 'operational', 'planning')
    
    Returns:
        bool: True if user has access, False otherwise
    """
    role = get_user_role()
    if not role:
        return False
    return ROLE_PERMISSIONS.get(role, {}).get(section, False)
