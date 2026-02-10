import streamlit as st

# Page config
st.set_page_config(
    page_title="Deteksi Buzzer MBG",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Import modules
from utils.data_loader import load_data, preprocess_data
from utils.feature_engineering import engineer_features
from utils.detection import detect_buzzers_rule_based, detect_buzzers_ml
from views import dashboard, analysis, network, user_explorer, settings

def main():
    st.markdown('<p class="main-header">🔍 Sistem Deteksi Buzzer MBG</p>', unsafe_allow_html=True)
    st.markdown("### Deteksi Buzzer pada Komentar YouTube tentang Program Makan Bergizi Gratis")
    
    # Sidebar
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Pilih Halaman:",
        ["🏠 Dashboard", "📈 Analisis Detail", "🕸️ Network Analysis", 
         "👤 User Explorer", "⚙️ Settings"]
    )
    
    # Load data with caching (akan diload sekali saja)
    with st.spinner("Loading data..."):
        df = load_data()
        
    if df is None:
        st.error("Failed to load data. Please check if dataset files exist.")
        return
    
    # Process data (cached)
    df = preprocess_data(df)
    
    # Engineer features (cached)
    with st.spinner("Engineering features..."):
        user_activity = engineer_features(df)
    
    # Detect buzzers (cached)
    with st.spinner("Detecting buzzers..."):
        user_activity = detect_buzzers_rule_based(user_activity)
        user_activity = detect_buzzers_ml(user_activity)
    
    # Route to pages - setiap page akan render secara modular
    if page == "🏠 Dashboard":
        dashboard.show_dashboard(df, user_activity)
    elif page == "📈 Analisis Detail":
        analysis.show_analysis(df, user_activity)
    elif page == "🕸️ Network Analysis":
        network.show_network(df, user_activity)
    elif page == "👤 User Explorer":
        user_explorer.show_user_explorer(df, user_activity)
    elif page == "⚙️ Settings":
        settings.show_settings()

if __name__ == "__main__":
    main()
