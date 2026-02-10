"""
Dashboard Kelayakan Alat Camping
Main Streamlit Application dengan Clean Architecture

Author: GitHub Copilot
Date: January 2026
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Setup path
sys.path.append(str(Path(__file__).parent))

# Import modules
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, MAX_ROWS_DISPLAY
from auth import show_login_page, check_authentication, logout, get_current_user, get_user_role, has_access
from src.data.loader import load_all_data, refresh_cache, load_katalog
from src.data.processor import (
    get_maintenance_summary,
    get_top_maintenance_items,
    get_recommendation_distribution,
    get_critical_items,
    get_rental_trends,
    get_utilization_rate,
    get_category_performance,
    get_strategic_insights,
    classify_lifecycle_stage
)
from src.visualization.charts import (
    create_recommendation_pie_chart,
    create_severity_bar_chart,
    create_condition_bar_chart,
    create_top_maintenance_chart,
    create_rental_trend_chart,
    create_maintenance_ratio_chart,
    create_utilization_chart,
    create_scatter_feasibility_utilization,
    create_box_feasibility_by_category,
    create_heatmap_maintenance_burden,
    create_quadrant_lifecycle,
    create_gauge_chart
)
from src.visualization.metrics import (
    display_summary_metrics,
    display_severity_metrics,
    display_recommendation_summary
)

# Page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
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
        padding: 1rem;
        background: linear-gradient(90deg, #e8f4f8 0%, #b8e0f0 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Check authentication
    if not check_authentication():
        show_login_page()
        return
    
    # Header
    st.markdown(f'<div class="main-header">{PAGE_ICON} {PAGE_TITLE}</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        
        # User info and logout
        current_user = get_current_user()
        user_role = get_user_role()
        
        # Display user info with role badge
        role_color = "#3498db" if user_role == "owner" else "#e67e22"
        role_label = "Owner" if user_role == "owner" else "Operational"
        
        st.markdown(f"""
        <div style="background-color: #e8f4f8; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="margin: 0; color: #2c3e50;"><strong>👤 {current_user}</strong></p>
            <p style="margin: 5px 0 0 0;">
                <span style="background-color: {role_color}; color: white; padding: 2px 8px; 
                             border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                    {role_label}
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()
        
        st.divider()
        
        st.title("🎯 Navigation")
        
        # Initialize session state with default page based on role
        # Also validate if current active_page is allowed for current role
        if 'active_page' not in st.session_state:
            # Set default page based on role
            if has_access('executive'):
                st.session_state.active_page = "📊 Overview"
            elif has_access('operational'):
                st.session_state.active_page = "📊 Tactical Dashboard"
            elif has_access('planning'):
                st.session_state.active_page = "📈 Strategic Dashboard"
        else:
            # Validate current active_page is allowed for current role
            current_page = st.session_state.active_page
            page_to_section = {
                "📊 Overview": "executive",
                "📊 Tactical Dashboard": "operational",
                "⚠️ Critical Items": "operational",
                "📈 Strategic Dashboard": "planning",
                "📋 Data Tables": "planning"
            }
            
            # If current page is not allowed for current role, reset to default
            if current_page in page_to_section:
                required_section = page_to_section[current_page]
                if not has_access(required_section):
                    # Reset to appropriate default page
                    if has_access('executive'):
                        st.session_state.active_page = "📊 Overview"
                    elif has_access('operational'):
                        st.session_state.active_page = "📊 Tactical Dashboard"
                    elif has_access('planning'):
                        st.session_state.active_page = "📈 Strategic Dashboard"
        
        # EXECUTIVE SECTION - Only show if user has access
        if has_access('executive'):
            st.markdown("### 📋 EXECUTIVE")
            
            # Use button for better stability in production
            if st.button(
                "📊 Overview",
                use_container_width=True,
                type="primary" if st.session_state.active_page == "📊 Overview" else "secondary",
                key="btn_overview"
            ):
                if st.session_state.active_page != "📊 Overview":
                    st.session_state.active_page = "📊 Overview"
                    st.rerun()
            
            st.divider()
        
        # OPERATIONAL SECTION - Only show if user has access
        if has_access('operational'):
            st.markdown("### ⚙️ OPERATIONAL")
            
            # Use buttons for better stability in production
            if st.button(
                "📊 Tactical Dashboard",
                use_container_width=True,
                type="primary" if st.session_state.active_page == "📊 Tactical Dashboard" else "secondary",
                key="btn_tactical"
            ):
                if st.session_state.active_page != "📊 Tactical Dashboard":
                    st.session_state.active_page = "📊 Tactical Dashboard"
                    st.rerun()
            
            if st.button(
                "⚠️ Critical Items",
                use_container_width=True,
                type="primary" if st.session_state.active_page == "⚠️ Critical Items" else "secondary",
                key="btn_critical"
            ):
                if st.session_state.active_page != "⚠️ Critical Items":
                    st.session_state.active_page = "⚠️ Critical Items"
                    st.rerun()
            
            st.divider()
        
        # PLANNING SECTION - Only show if user has access
        if has_access('planning'):
            st.markdown("### 📈 PLANNING")
            
            # Use buttons for better stability in production
            if st.button(
                "📈 Strategic Dashboard",
                use_container_width=True,
                type="primary" if st.session_state.active_page == "📈 Strategic Dashboard" else "secondary",
                key="btn_strategic"
            ):
                if st.session_state.active_page != "📈 Strategic Dashboard":
                    st.session_state.active_page = "📈 Strategic Dashboard"
                    st.rerun()
            
            if st.button(
                "📋 Data Tables",
                use_container_width=True,
                type="primary" if st.session_state.active_page == "📋 Data Tables" else "secondary",
                key="btn_data_tables"
            ):
                if st.session_state.active_page != "📋 Data Tables":
                    st.session_state.active_page = "📋 Data Tables"
                    st.rerun()
            
            st.divider()
        
        # Use active page from session state
        page = st.session_state.active_page
        
        st.divider()
        
        st.subheader("⚙️ Settings")
        if st.button("🔄 Refresh Data", use_container_width=True):
            refresh_cache()
        
        st.divider()
        
        st.caption("Dashboard Kelayakan Alat")
        st.caption("© 2026 - Sistem Informasi Perusahaan")
    
    # Load data
    with st.spinner("Loading data..."):
        katalog_df, penyewaan_df, maintenance_df, insight_df = load_all_data()
    
    if katalog_df.empty or insight_df.empty:
        st.error("❌ Data tidak dapat dimuat. Pastikan semua file dataset tersedia.")
        return
    
    # Route ke halaman yang dipilih dengan access control
    if page == "📊 Overview":
        if has_access('executive'):
            show_overview_page(katalog_df, penyewaan_df, maintenance_df, insight_df)
        else:
            st.error("🚫 Access Denied: You don't have permission to access Executive Dashboard")
    
    elif page == "📊 Tactical Dashboard":
        if has_access('operational'):
            show_tactical_dashboard(insight_df, maintenance_df)
        else:
            st.error("🚫 Access Denied: You don't have permission to access Tactical Dashboard")
    
    elif page == "⚠️ Critical Items":
        if has_access('operational'):
            show_critical_items_page(insight_df, maintenance_df)
        else:
            st.error("🚫 Access Denied: You don't have permission to access Critical Items")
    
    elif page == "📈 Strategic Dashboard":
        if has_access('planning'):
            show_strategic_dashboard(insight_df)
        else:
            st.error("🚫 Access Denied: You don't have permission to access Strategic Dashboard")
    
    elif page == "📋 Data Tables":
        if has_access('planning'):
            show_data_tables_page(katalog_df, penyewaan_df, maintenance_df, insight_df)
        else:
            st.error("🚫 Access Denied: You don't have permission to access Data Tables")


def show_overview_page(katalog_df, penyewaan_df, maintenance_df, insight_df):
    """Executive Summary - Overview page dengan high-level KPIs"""
    
    st.markdown('<div class="section-header">📊 Executive Dashboard</div>', 
                unsafe_allow_html=True)
    
    # Get strategic insights
    insights = get_strategic_insights(insight_df)
    
    # Key Performance Indicators
    st.subheader("🎯 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Alat",
            f"{insights['total_items']}",
            help="Total jumlah alat dalam katalog"
        )
    
    with col2:
        avg_kelayakan = insights['avg_kelayakan']
        delta_color = "normal" if avg_kelayakan >= 70 else "inverse"
        st.metric(
            "Avg Kelayakan",
            f"{avg_kelayakan:.1f}%",
            delta=f"{avg_kelayakan - 70:.1f}% dari target",
            delta_color=delta_color,
            help="Rata-rata kelayakan seluruh alat"
        )
    
    with col3:
        st.metric(
            "Total Penyewaan",
            f"{int(insights['total_sewa'])}x",
            help="Total frekuensi penyewaan"
        )
    
    with col4:
        utilization_rate = insights['avg_utilization']
        st.metric(
            "Avg Utilisasi",
            f"{utilization_rate:.1f}x",
            help="Rata-rata frekuensi sewa per alat"
        )
    
    st.divider()
    
    # Gauge Charts Row - Collapsed by default untuk performa
    with st.expander("📊 Health Indicators (Gauge Charts)", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig_gauge1 = create_gauge_chart(
                value=insights['avg_kelayakan'],
                title="Overall Kelayakan",
                max_value=100,
                thresholds={'low': 40, 'medium': 70, 'high': 85}
            )
            st.plotly_chart(fig_gauge1, use_container_width=True)
        
        with col2:
            # Utilization rate as percentage of median
            util_pct = min((insights['avg_utilization'] / 10) * 100, 100)  # Scale to 100
            fig_gauge2 = create_gauge_chart(
                value=util_pct,
                title="Utilization Rate",
                max_value=100,
                thresholds={'low': 30, 'medium': 60, 'high': 80}
            )
            st.plotly_chart(fig_gauge2, use_container_width=True)
        
        with col3:
            # Health score (inverse of maintenance burden)
            if insights['total_sewa'] > 0:
                health_score = max(0, 100 - (insights['total_maintenance'] / insights['total_sewa'] * 100))
            else:
                health_score = 100
            fig_gauge3 = create_gauge_chart(
                value=health_score,
                title="Equipment Health",
                max_value=100,
                thresholds={'low': 50, 'medium': 70, 'high': 85}
            )
            st.plotly_chart(fig_gauge3, use_container_width=True)
    
    st.divider()
    
    # Status Distribution
    st.subheader("🎯 Status Distribution")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart
        rec_dist = get_recommendation_distribution(insight_df)
        if not rec_dist.empty:
            fig = create_recommendation_pie_chart(rec_dist)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Status summary cards
        st.markdown("#### 📋 Status Summary")
        
        critical = insights['critical_count']
        warning = insights['warning_count']
        total = insights['total_items']
        healthy = total - critical - warning
        
        st.markdown(f"""
        <div style="background-color: #e8f8f5; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: #1e8449; margin: 0;">✅ Healthy: {healthy}</h3>
            <p style="color: #145a32; margin: 5px 0 0 0; font-weight: 500;">Kelayakan ≥ 70%</p>
        </div>
        
        <div style="background-color: #fef5e7; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: #d68910; margin: 0;">⚠️ Warning: {warning}</h3>
            <p style="color: #9c640c; margin: 5px 0 0 0; font-weight: 500;">Kelayakan 40-70%</p>
        </div>
        
        <div style="background-color: #fadbd8; padding: 15px; border-radius: 10px;">
            <h3 style="color: #c0392b; margin: 0;">🔴 Critical: {critical}</h3>
            <p style="color: #922b21; margin: 5px 0 0 0; font-weight: 500;">Kelayakan < 40%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Navigation Cards
    st.subheader("🧭 Quick Navigation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 15px; color: white; text-align: center;">
            <h3>📊 Tactical Dashboard</h3>
            <p>Monitoring operasional harian</p>
            <p style="font-size: 0.9em; opacity: 0.9;">• Critical items<br>• Performance metrics<br>• Real-time alerts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 15px; color: white; text-align: center;">
            <h3>📈 Strategic Dashboard</h3>
            <p>Analisis jangka panjang</p>
            <p style="font-size: 0.9em; opacity: 0.9;">• Investment analysis<br>• Portfolio evaluation<br>• Lifecycle planning</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 15px; color: white; text-align: center;">
            <h3>📋 Data Tables</h3>
            <p>Eksplorasi data detail</p>
            <p style="font-size: 0.9em; opacity: 0.9;">• Raw data access<br>• Custom filtering<br>• Export options</p>
        </div>
        """, unsafe_allow_html=True)


def show_tactical_dashboard(insight_df, maintenance_df):
    """Tactical Dashboard - Operational monitoring untuk daily decisions"""
    
    st.markdown('<div class="section-header">📊 Tactical Dashboard</div>', 
                unsafe_allow_html=True)
    st.caption("Real-time operational monitoring untuk decision making harian")
    
    # Interactive Filters
    st.subheader("🔧 Filters")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        kelayakan_threshold = st.slider(
            "Kelayakan Threshold (%)",
            min_value=40,
            max_value=90,
            value=70,
            step=5,
            help="Filter alat dengan kelayakan di bawah threshold"
        )
    
    with col2:
        # Get unique categories - cached
        all_categories = sorted(insight_df['kategori'].unique().tolist())
        selected_categories = st.multiselect(
            "Filter Kategori",
            options=all_categories,
            default=all_categories[:3] if len(all_categories) > 3 else all_categories,  # Default hanya 3 kategori pertama
            help="Pilih kategori yang ingin ditampilkan"
        )
    
    # Apply filters only if categories selected
    if not selected_categories:
        st.warning("⚠️ Pilih minimal 1 kategori untuk menampilkan data")
        return
    
    filtered_df = insight_df[insight_df['kategori'].isin(selected_categories)].copy()
    
    st.divider()
    
    # Critical Items Alert
    critical_items = filtered_df[filtered_df['kelayakan'] < kelayakan_threshold].copy()
    critical_items = critical_items.sort_values('kelayakan', ascending=True)
    
    if len(critical_items) > 0:
        st.error(f"⚠️ **ALERT:** {len(critical_items)} alat memerlukan perhatian (kelayakan < {kelayakan_threshold}%)")
    else:
        st.success(f"✅ Semua alat dalam kondisi baik (kelayakan ≥ {kelayakan_threshold}%)")
    
    # Key Tactical Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Critical Items",
            len(critical_items),
            delta=f"-{len(critical_items)} items" if len(critical_items) > 0 else "All clear",
            delta_color="inverse"
        )
    
    with col2:
        avg_kelayakan = filtered_df['kelayakan'].mean()
        st.metric(
            "Avg Kelayakan",
            f"{avg_kelayakan:.1f}%",
            delta=f"{avg_kelayakan - kelayakan_threshold:.1f}%"
        )
    
    with col3:
        high_maintenance = len(filtered_df[filtered_df['maintenance_ratio'] > 0.3])
        st.metric(
            "High Maintenance",
            high_maintenance,
            help="Alat dengan maintenance ratio > 30%"
        )
    
    with col4:
        underutilized = len(filtered_df[filtered_df['freq_sewa'] < filtered_df['freq_sewa'].median()])
        st.metric(
            "Underutilized",
            underutilized,
            help="Alat dengan utilisasi di bawah median"
        )
    
    st.divider()
    
    # Category Performance Cards - Lazy render dengan expander
    with st.expander("📊 Category Performance", expanded=False):
        category_perf = get_category_performance(filtered_df)
        
        # Display as cards - limit to 3 for performance
        cols = st.columns(3)
        for idx, row in category_perf.head(3).iterrows():
            col_idx = idx % 3
            with cols[col_idx]:
                avg_kel = row['avg_kelayakan']
                if avg_kel >= 85:
                    bg_color = "#d4edda"
                    icon = "🟢"
                elif avg_kel >= 70:
                    bg_color = "#fff3cd"
                    icon = "🟡"
                else:
                    bg_color = "#f8d7da"
                    icon = "🔴"
                
                st.markdown(f"""
                <div style="background-color: {bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <h4 style="margin: 0;">{icon} {row['kategori']}</h4>
                    <p style="margin: 5px 0;"><strong>Kelayakan:</strong> {avg_kel:.1f}%</p>
                    <p style="margin: 5px 0;"><strong>Items:</strong> {int(row['jumlah_items'])} | <strong>Sewa:</strong> {int(row['total_sewa'])}x</p>
                    <p style="margin: 5px 0;"><strong>Maintenance:</strong> {int(row['total_maintenance'])}x | <strong>Ratio:</strong> {row['avg_maintenance_ratio']*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Visualizations - Only show critical items chart by default
    st.subheader("🔝 Top Maintenance Burden")
    if len(critical_items) > 0:
        fig = create_maintenance_ratio_chart(critical_items, top_n=10)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("✅ Tidak ada alat yang memerlukan perhatian khusus")
    
    # Utilization chart in expander for lazy loading
    with st.expander("📈 View Top Utilization Chart", expanded=False):
        util_data = get_utilization_rate(filtered_df)
        if not util_data.empty:
            fig = create_utilization_chart(util_data, top_n=10)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Data utilisasi tidak tersedia")
    
    st.divider()
    
    # Critical Items Table
    if len(critical_items) > 0:
        st.subheader("⚠️ Critical Items Detail")
        
        with st.expander("📋 Lihat Detail Critical Items", expanded=True):
            # Format untuk display
            display_critical = critical_items.head(20).copy()
            display_critical['kelayakan'] = display_critical['kelayakan'].apply(lambda x: f"{x:.1f}%")
            display_critical['maintenance_ratio'] = display_critical['maintenance_ratio'].apply(lambda x: f"{x*100:.1f}%")
            
            st.dataframe(
                display_critical[['kode_barang', 'nama_barang', 'kategori', 'freq_sewa', 
                                 'jumlah_maintenance', 'maintenance_ratio', 'kelayakan', 'rekomendasi']],
                use_container_width=True,
                hide_index=True
            )


def show_strategic_dashboard(insight_df):
    """Strategic Dashboard - Long-term analysis untuk planning"""
    
    st.markdown('<div class="section-header">📈 Strategic Dashboard</div>', 
                unsafe_allow_html=True)
    st.caption("Analisis strategis untuk perencanaan jangka panjang dan investment decisions")
    
    # Add loading indicator
    with st.spinner("Loading strategic insights..."):
        # Strategic Insights
        insights = get_strategic_insights(insight_df)
    
    # Executive Summary
    st.subheader("📊 Strategic Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px;">
            <h4 style="color: #0d47a1; margin: 0 0 10px 0;">📦 Portfolio Size</h4>
            <h2 style="color: #1f77b4; margin: 10px 0;">{}</h2>
            <p style="color: #37474f; margin: 5px 0 0 0;">Total Equipment Items</p>
        </div>
        """.format(insights['total_items']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px;">
            <h4 style="color: #1b5e20; margin: 0 0 10px 0;">📈 Total Utilization</h4>
            <h2 style="color: #4caf50; margin: 10px 0;">{:,}x</h2>
            <p style="color: #37474f; margin: 5px 0 0 0;">Total Rental Frequency</p>
        </div>
        """.format(int(insights['total_sewa'])), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #fff3e0; padding: 20px; border-radius: 10px;">
            <h4 style="color: #e65100; margin: 0 0 10px 0;">🔧 Maintenance Events</h4>
            <h2 style="color: #ff9800; margin: 10px 0;">{:,}x</h2>
            <p style="color: #37474f; margin: 5px 0 0 0;">Total Maintenance Count</p>
        </div>
        """.format(int(insights['total_maintenance'])), unsafe_allow_html=True)
    
    st.divider()
    
    # Category Ranking Table
    st.subheader("🏆 Category Ranking by Performance")
    
    category_perf = get_category_performance(insight_df)
    
    # Format for display
    display_cat = category_perf.copy()
    display_cat['avg_kelayakan'] = display_cat['avg_kelayakan'].apply(lambda x: f"{x:.1f}%")
    display_cat['avg_maintenance_ratio'] = display_cat['avg_maintenance_ratio'].apply(lambda x: f"{x*100:.1f}%")
    display_cat['roi_indicator'] = display_cat['roi_indicator'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(
        display_cat[['kategori', 'jumlah_items', 'avg_kelayakan', 'total_sewa', 
                     'total_maintenance', 'avg_maintenance_ratio', 'roi_indicator']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "kategori": "Kategori",
            "jumlah_items": "Items",
            "avg_kelayakan": "Avg Kelayakan",
            "total_sewa": "Total Sewa",
            "total_maintenance": "Total Maint",
            "avg_maintenance_ratio": "Avg Ratio",
            "roi_indicator": "ROI"
        }
    )
    
    st.divider()
    
    # Strategic Visualizations - Lazy loading per tab
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Correlation Analysis", 
        "📦 Portfolio Distribution", 
        "🔥 Maintenance Burden",
        "🎯 Lifecycle Matrix"
    ])
    
    with tab1:
        st.subheader("Correlation: Utilization vs Kelayakan")
        st.caption("Identifikasi pola: apakah utilisasi tinggi menurunkan kelayakan?")
        
        with st.spinner("Generating correlation chart..."):
            fig = create_scatter_feasibility_utilization(insight_df)
            st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation
        correlation = insight_df[['freq_sewa', 'kelayakan']].corr().iloc[0, 1]
        if correlation < -0.3:
            st.warning(f"⚠️ Korelasi negatif kuat ({correlation:.2f}): Utilisasi tinggi cenderung menurunkan kelayakan. Pertimbangkan penambahan inventory.")
        elif correlation > 0.3:
            st.success(f"✅ Korelasi positif ({correlation:.2f}): Alat dengan utilisasi tinggi tetap terjaga kelayakannya.")
        else:
            st.info(f"ℹ️ Korelasi lemah ({correlation:.2f}): Tidak ada pola kuat antara utilisasi dan kelayakan.")
    
    with tab2:
        st.subheader("Distribusi Kelayakan per Kategori")
        st.caption("Evaluasi performa portfolio berdasarkan kategori")
        
        with st.spinner("Generating box plot..."):
            fig = create_box_feasibility_by_category(insight_df)
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.markdown("**📋 Key Insights:**")
        best_category = category_perf.iloc[0]
        worst_category = category_perf.iloc[-1]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🏆 **Best Performer:** {best_category['kategori']} (Avg: {best_category['avg_kelayakan']:.1f}%)")
        with col2:
            st.error(f"⚠️ **Needs Attention:** {worst_category['kategori']} (Avg: {worst_category['avg_kelayakan']:.1f}%)")
    
    with tab3:
        st.subheader("Beban Maintenance per Kategori")
        st.caption("Identifikasi kategori dengan maintenance burden tertinggi")
        
        with st.spinner("Generating heatmap..."):
            fig = create_heatmap_maintenance_burden(insight_df)
            st.plotly_chart(fig, use_container_width=True)
        
        # High burden categories
        high_burden = category_perf[category_perf['avg_maintenance_ratio'] > 0.3]
        if not high_burden.empty:
            st.warning(f"⚠️ {len(high_burden)} kategori memiliki maintenance ratio > 30%: {', '.join(high_burden['kategori'].tolist())}")
    
    with tab4:
        st.subheader("Asset Lifecycle Matrix")
        st.caption("Matriks strategis: Nilai Utilisasi vs Beban Maintenance")
        
        with st.spinner("Generating lifecycle matrix..."):
            fig = create_quadrant_lifecycle(insight_df)
            st.plotly_chart(fig, use_container_width=True)
        
        # Quadrant insights
        st.markdown("**🎯 Strategic Recommendations:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🟢 High Value / Low Maintenance** (IDEAL)
            - Maintain current strategy
            - Use as benchmark
            - Maximize utilization
            
            **🟡 High Value / High Maintenance** (PERHATIAN)
            - Investasi maintenance preventif
            - Monitor closely
            - Plan replacement timeline
            """)
        
        with col2:
            st.markdown("""
            **🔵 Low Value / Low Maintenance** (RENDAH)
            - Tingkatkan marketing
            - Evaluate pricing
            - Consider bundling
            
            **🔴 Low Value / High Maintenance** (KRITIS)
            - Prioritas penggantian
            - Stop procurement
            - Phase out strategy
            """)
    
    st.divider()
    
    # Investment Priority
    st.subheader("💡 Investment Priority Recommendations")
    
    if len(insights['investment_priority']) > 0:
        st.warning(f"⚠️ {len(insights['investment_priority'])} alat dengan utilisasi tinggi namun kelayakan menurun")
        
        investment_df = pd.DataFrame(insights['investment_priority'])
        st.dataframe(
            investment_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "kode_barang": "Kode",
                "nama_barang": "Nama Alat",
                "freq_sewa": "Freq Sewa",
                "kelayakan": st.column_config.NumberColumn("Kelayakan", format="%.1f%%")
            }
        )
        
        st.info("💡 **Rekomendasi:** Prioritaskan investment pada alat-alat di atas untuk memaksimalkan ROI dan mempertahankan utilisasi tinggi.")
    else:
        st.success("✅ Tidak ada alat dengan utilisasi tinggi yang memerlukan investment prioritas")
    
    st.divider()
    
    # Lifecycle Classification - Collapsed by default
    with st.expander("🔄 Equipment Lifecycle Distribution", expanded=False):
        lifecycle_df = classify_lifecycle_stage(insight_df)
        lifecycle_dist = lifecycle_df['lifecycle_stage'].value_counts().reset_index()
        lifecycle_dist.columns = ['Stage', 'Count']
        
        # Display as metrics
        stages = lifecycle_dist.to_dict('records')
        cols = st.columns(min(len(stages), 3))
        
        for idx, stage in enumerate(stages):
            col_idx = idx % 3
            with cols[col_idx]:
                st.metric(stage['Stage'], stage['Count'])


def show_critical_items_page(insight_df, maintenance_df):
    """Critical items page"""
    
    st.markdown('<div class="section-header">⚠️ Alat yang Memerlukan Perhatian</div>', 
                unsafe_allow_html=True)
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    with col1:
        threshold = st.slider(
            "Kelayakan Threshold (%)",
            min_value=40,
            max_value=90,
            value=70,
            step=5
        )
    
    # Critical items - filter by kelayakan
    if 'kelayakan' in insight_df.columns:
        critical_df = insight_df[insight_df['kelayakan'] < threshold].copy()
        critical_df = critical_df.sort_values('kelayakan', ascending=True)
    else:
        # Fallback ke maintenance ratio jika tidak ada kolom kelayakan
        critical_df = get_critical_items(insight_df, threshold=0.3)
    
    if critical_df.empty:
        st.success(f"✅ Semua alat memiliki kelayakan ≥ {threshold}%")
        return
    
    st.error(f"⚠️ Ditemukan **{len(critical_df)}** alat dengan kelayakan < {threshold}%")
    
    # Display critical items
    for idx, row in critical_df.head(10).iterrows():
        with st.container():
            if 'kelayakan' in row:
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
            else:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
            
            with col1:
                st.markdown(f"**{row['nama_barang']}**")
                st.caption(f"Kode: {row['kode_barang']}")
            
            with col2:
                if 'kelayakan' in row:
                    kelayakan = row['kelayakan']
                    if kelayakan < 40:
                        color = "🔴"
                    elif kelayakan < 70:
                        color = "🟡"
                    else:
                        color = "🟢"
                    st.metric("Kelayakan", f"{color} {kelayakan:.1f}%")
                else:
                    ratio = row['maintenance_ratio'] * 100
                    color = "🔴" if ratio > 50 else "🟡"
                    st.metric("Ratio", f"{color} {ratio:.1f}%")
            
            with col3:
                st.metric("Freq", f"{row['freq_sewa']:.0f}x")
            
            with col4:
                st.metric("Maint", f"{row['jumlah_maintenance']:.0f}x")
            
            if 'kelayakan' in row:
                with col5:
                    st.markdown(f"**{row['rekomendasi']}**")
            else:
                st.markdown(f"**{row['rekomendasi']}**")
            
            st.divider()
    
    # Full table
    with st.expander("📋 Lihat Semua Data"):
        display_df = critical_df.copy()
        display_df['maintenance_ratio'] = display_df['maintenance_ratio'].apply(
            lambda x: f"{x*100:.1f}%"
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)


def show_data_tables_page(katalog_df, penyewaan_df, maintenance_df, insight_df):
    """Data tables page"""
    
    st.markdown('<div class="section-header">📋 Data Tables</div>', 
                unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📦 Katalog", "🛒 Penyewaan", "🔧 Maintenance", "💡 Insight"
    ])
    
    with tab1:
        st.subheader("Katalog Barang")
        st.info(f"Total: {len(katalog_df)} items")
        
        # Pagination for Katalog - Reduced rows for better performance
        if 'katalog_page' not in st.session_state:
            st.session_state.katalog_page = 0
        
        rows_per_page = 10  # Reduced from MAX_ROWS_DISPLAY
        total_pages = max(1, (len(katalog_df) - 1) // rows_per_page + 1)
        start_idx = st.session_state.katalog_page * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(katalog_df))
        
        # Format tanggal_pembelian untuk display with error handling
        display_df = katalog_df.iloc[start_idx:end_idx].copy()
        if 'tanggal_pembelian' in display_df.columns:
            try:
                # Convert to string safely, handling NaT/None
                display_df['tanggal_pembelian'] = display_df['tanggal_pembelian'].apply(
                    lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else '-'
                )
            except Exception as e:
                # Fallback: convert to string directly
                display_df['tanggal_pembelian'] = display_df['tanggal_pembelian'].astype(str)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Pagination controls
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        with col1:
            if st.button("⏮️ First", key="katalog_first"):
                st.session_state.katalog_page = 0
                st.rerun()
        with col2:
            if st.button("◀️ Prev", key="katalog_prev"):
                if st.session_state.katalog_page > 0:
                    st.session_state.katalog_page -= 1
                    st.rerun()
        with col3:
            st.write(f"Page {st.session_state.katalog_page + 1} of {total_pages}")
        with col4:
            if st.button("Next ▶️", key="katalog_next"):
                if st.session_state.katalog_page < total_pages - 1:
                    st.session_state.katalog_page += 1
                    st.rerun()
        with col5:
            if st.button("Last ⏭️", key="katalog_last"):
                st.session_state.katalog_page = total_pages - 1
                st.rerun()
        
        st.caption(f"Showing rows {start_idx + 1} to {end_idx} of {len(katalog_df)}")
    
    with tab2:
        st.subheader("Riwayat Penyewaan")
        st.info(f"Total: {len(penyewaan_df)} rows")
        
        # Pagination for Penyewaan - Reduced rows
        if 'penyewaan_page' not in st.session_state:
            st.session_state.penyewaan_page = 0
        
        rows_per_page = 10  # Reduced for better performance
        total_pages = max(1, (len(penyewaan_df) - 1) // rows_per_page + 1)
        start_idx = st.session_state.penyewaan_page * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(penyewaan_df))
        
        # Format tanggal untuk display with error handling
        display_df = penyewaan_df.iloc[start_idx:end_idx].copy()
        if 'tanggal_sewa' in display_df.columns:
            try:
                display_df['tanggal_sewa'] = display_df['tanggal_sewa'].apply(
                    lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else '-'
                )
            except:
                display_df['tanggal_sewa'] = display_df['tanggal_sewa'].astype(str)
        if 'tanggal_kembali' in display_df.columns:
            try:
                display_df['tanggal_kembali'] = display_df['tanggal_kembali'].apply(
                    lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else '-'
                )
            except:
                display_df['tanggal_kembali'] = display_df['tanggal_kembali'].astype(str)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Pagination controls
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        with col1:
            if st.button("⏮️ First", key="penyewaan_first"):
                st.session_state.penyewaan_page = 0
                st.rerun()
        with col2:
            if st.button("◀️ Prev", key="penyewaan_prev"):
                if st.session_state.penyewaan_page > 0:
                    st.session_state.penyewaan_page -= 1
                    st.rerun()
        with col3:
            st.write(f"Page {st.session_state.penyewaan_page + 1} of {total_pages}")
        with col4:
            if st.button("Next ▶️", key="penyewaan_next"):
                if st.session_state.penyewaan_page < total_pages - 1:
                    st.session_state.penyewaan_page += 1
                    st.rerun()
        with col5:
            if st.button("Last ⏭️", key="penyewaan_last"):
                st.session_state.penyewaan_page = total_pages - 1
                st.rerun()
        
        st.caption(f"Showing rows {start_idx + 1} to {end_idx} of {len(penyewaan_df)}")
    
    with tab3:
        st.subheader("Riwayat Maintenance")
        st.info(f"Total: {len(maintenance_df)} events")
        
        # Pagination for Maintenance - Reduced rows
        if 'maintenance_page' not in st.session_state:
            st.session_state.maintenance_page = 0
        
        rows_per_page = 10  # Reduced for better performance
        total_pages = max(1, (len(maintenance_df) - 1) // rows_per_page + 1)
        start_idx = st.session_state.maintenance_page * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(maintenance_df))
        
        # Format tanggal_maintenance untuk display with error handling
        display_df = maintenance_df.iloc[start_idx:end_idx].copy()
        if 'tanggal_maintenance' in display_df.columns:
            try:
                display_df['tanggal_maintenance'] = display_df['tanggal_maintenance'].apply(
                    lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else '-'
                )
            except:
                display_df['tanggal_maintenance'] = display_df['tanggal_maintenance'].astype(str)
        
        # Remove biaya column if exists
        if 'biaya' in display_df.columns:
            display_df = display_df.drop(columns=['biaya'])
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Pagination controls
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        with col1:
            if st.button("⏮️ First", key="maintenance_first"):
                st.session_state.maintenance_page = 0
                st.rerun()
        with col2:
            if st.button("◀️ Prev", key="maintenance_prev"):
                if st.session_state.maintenance_page > 0:
                    st.session_state.maintenance_page -= 1
                    st.rerun()
        with col3:
            st.write(f"Page {st.session_state.maintenance_page + 1} of {total_pages}")
        with col4:
            if st.button("Next ▶️", key="maintenance_next"):
                if st.session_state.maintenance_page < total_pages - 1:
                    st.session_state.maintenance_page += 1
                    st.rerun()
        with col5:
            if st.button("Last ⏭️", key="maintenance_last"):
                st.session_state.maintenance_page = total_pages - 1
                st.rerun()
        
        st.caption(f"Showing rows {start_idx + 1} to {end_idx} of {len(maintenance_df)}")
    
    with tab4:
        st.subheader("Insight Kelayakan Alat")
        st.info(f"Total: {len(insight_df)} items")
        
        # Sorting options (applied globally before pagination)
        col_sort1, col_sort2 = st.columns([2, 1])
        with col_sort1:
            sort_column = st.selectbox(
                "Urutkan berdasarkan:",
                options=["Default (Kode Barang)", "Kelayakan", "Frekuensi Sewa", "Total Hari Sewa", "Jumlah Maintenance"],
                key="insight_sort_column"
            )
        with col_sort2:
            sort_order = st.radio(
                "Urutan:",
                options=["Ascending ⬆️", "Descending ⬇️"],
                key="insight_sort_order",
                horizontal=True
            )
        
        # Apply sorting globally - only compute when needed
        with st.spinner("Sorting data..."):
            sorted_df = insight_df.copy()
            if sort_column == "Kelayakan":
                sorted_df = sorted_df.sort_values('kelayakan', ascending=(sort_order == "Ascending ⬆️"))
            elif sort_column == "Frekuensi Sewa":
                sorted_df = sorted_df.sort_values('freq_sewa', ascending=(sort_order == "Ascending ⬆️"))
            elif sort_column == "Total Hari Sewa":
                sorted_df = sorted_df.sort_values('total_hari_sewa', ascending=(sort_order == "Ascending ⬆️"))
            elif sort_column == "Jumlah Maintenance":
                sorted_df = sorted_df.sort_values('jumlah_maintenance', ascending=(sort_order == "Ascending ⬆️"))
            # else: Default order (no sorting)
        
        # Pagination for Insight - reduced rows per page
        if 'insight_page' not in st.session_state:
            st.session_state.insight_page = 0
        
        rows_per_page = 10  # Reduced from MAX_ROWS_DISPLAY for better performance
        total_pages = max(1, (len(sorted_df) - 1) // rows_per_page + 1)
        start_idx = st.session_state.insight_page * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(sorted_df))
        
        # Format display
        display_df = sorted_df.copy()
        if 'maintenance_ratio' in display_df.columns:
            display_df['maintenance_ratio'] = display_df['maintenance_ratio'].apply(
                lambda x: f"{x*100:.1f}%" if pd.notna(x) else "0%"
            )
        if 'kelayakan' in display_df.columns:
            display_df['kelayakan'] = display_df['kelayakan'].apply(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "0%"
            )
        
        st.dataframe(display_df.iloc[start_idx:end_idx], use_container_width=True, hide_index=True)
        
        # Pagination controls
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        with col1:
            if st.button("⏮️ First", key="insight_first"):
                st.session_state.insight_page = 0
                st.rerun()
        with col2:
            if st.button("◀️ Prev", key="insight_prev"):
                if st.session_state.insight_page > 0:
                    st.session_state.insight_page -= 1
                    st.rerun()
        with col3:
            st.write(f"Page {st.session_state.insight_page + 1} of {total_pages}")
        with col4:
            if st.button("Next ▶️", key="insight_next"):
                if st.session_state.insight_page < total_pages - 1:
                    st.session_state.insight_page += 1
                    st.rerun()
        with col5:
            if st.button("Last ⏭️", key="insight_last"):
                st.session_state.insight_page = total_pages - 1
                st.rerun()
        
        st.caption(f"Showing rows {start_idx + 1} to {end_idx} of {len(sorted_df)}")


if __name__ == "__main__":
    main()
