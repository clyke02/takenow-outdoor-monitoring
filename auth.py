"""
Authentication Module untuk Dashboard Kelayakan Alat
Simple single-user authentication
"""

import streamlit as st
from config import USERNAME, PASSWORD, USER_DISPLAY_NAME


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
        
        # Login button
        login_button = st.button("🔑 Login", use_container_width=True, type="primary")
        
        # Handle login
        if login_button:
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.display_name = USER_DISPLAY_NAME
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
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
        bool: True if credentials are valid, False otherwise
    """
    return username == USERNAME and password == PASSWORD


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
    st.rerun()


def get_current_user():
    """
    Get current logged-in user display name
    
    Returns:
        str: User display name or None
    """
    return st.session_state.get('display_name', None)
