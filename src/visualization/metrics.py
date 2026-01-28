"""
Metrics Display Module
Komponen untuk menampilkan metric cards
"""
import streamlit as st
from typing import Dict, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.data.processor import format_rupiah


def display_metric_card(label: str, value: str, delta: Optional[str] = None, 
                       delta_color: str = "normal", help_text: str = None):
    """Display metric card dengan styling"""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color, help=help_text)


def display_summary_metrics(maintenance_summary: Dict, total_items: int):
    """Display summary metrics dalam columns"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="📦 Total Alat",
            value=f"{total_items:,}",
            help="Total alat dalam katalog"
        )
    
    with col2:
        total_events = maintenance_summary.get('total_events', 0)
        st.metric(
            label="🔧 Maintenance Events",
            value=f"{total_events:,}",
            help="Total kejadian maintenance"
        )


def display_severity_metrics(severity_dist: Dict):
    """Display severity distribution metrics"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ringan = severity_dist.get('Ringan', 0)
        st.metric(
            label="✅ Ringan",
            value=ringan,
            help="Kerusakan ringan"
        )
    
    with col2:
        sedang = severity_dist.get('Sedang', 0)
        st.metric(
            label="⚠️ Sedang",
            value=sedang,
            help="Kerusakan sedang"
        )
    
    with col3:
        berat = severity_dist.get('Berat', 0)
        st.metric(
            label="❌ Berat",
            value=berat,
            help="Kerusakan berat"
        )


def display_recommendation_summary(insight_df):
    """Display recommendation summary metrics"""
    if insight_df.empty or 'rekomendasi' not in insight_df.columns:
        st.warning("Data rekomendasi tidak tersedia")
        return
    
    rec_counts = insight_df['rekomendasi'].value_counts()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sangat_baik = rec_counts.get('KONDISI SANGAT BAIK', 0)
        st.metric(
            label="💚 Sangat Baik",
            value=sangat_baik,
            delta="Excellent",
            delta_color="normal",
            help="Alat dalam kondisi sangat baik"
        )
    
    with col2:
        layak = rec_counts.get('LAYAK OPERASIONAL', 0)
        st.metric(
            label="💙 Layak Operasional",
            value=layak,
            delta="Good",
            delta_color="normal",
            help="Alat layak untuk operasional"
        )
    
    with col3:
        tingkatkan = rec_counts.get('TINGKATKAN PEMELIHARAAN', 0)
        st.metric(
            label="🟡 Tingkatkan Pemeliharaan",
            value=tingkatkan,
            delta="Warning",
            delta_color="normal",
            help="Perlu peningkatan pemeliharaan"
        )
    
    with col4:
        perlu_perhatian = rec_counts.get('PERLU PERHATIAN KHUSUS', 0)
        st.metric(
            label="🔴 Perlu Perhatian",
            value=perlu_perhatian,
            delta="Critical" if perlu_perhatian > 0 else "None",
            delta_color="inverse" if perlu_perhatian > 0 else "normal",
            help="Perlu perhatian khusus segera"
        )


def display_item_detail_metrics(item_data: Dict):
    """Display metrics untuk detail item spesifik"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Frekuensi Sewa",
            value=f"{item_data.get('freq_sewa', 0):,}x",
            help="Total kali disewa"
        )
    
    with col2:
        st.metric(
            label="Total Hari Sewa",
            value=f"{item_data.get('total_hari_sewa', 0):,} hari",
            help="Total durasi sewa"
        )
    
    with col3:
        st.metric(
            label="Jumlah Maintenance",
            value=f"{item_data.get('jumlah_maintenance', 0):,}x",
            help="Total maintenance dilakukan"
        )
    
    with col4:
        ratio = item_data.get('maintenance_ratio', 0) * 100
        delta_color = "inverse" if ratio > 30 else "normal"
        st.metric(
            label="Maintenance Ratio",
            value=f"{ratio:.1f}%",
            delta="High" if ratio > 30 else "Normal",
            delta_color=delta_color,
            help="Perbandingan maintenance vs sewa"
        )
