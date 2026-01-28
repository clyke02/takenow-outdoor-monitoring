"""
Data Loader Module
Handle semua operasi loading data dengan caching
"""
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Tuple, Optional
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import (
    KATALOG_FILE, 
    RIWAYAT_PENYEWAAN_FILE, 
    RIWAYAT_MAINTENANCE_FILE, 
    INSIGHT_FILE,
    CACHE_TTL
)


@st.cache_data(ttl=CACHE_TTL)
def load_katalog() -> pd.DataFrame:
    """Load katalog barang dengan caching"""
    try:
        df = pd.read_excel(KATALOG_FILE)
        df['tanggal_pembelian'] = pd.to_datetime(df['tanggal_pembelian'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading katalog: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL)
def load_riwayat_penyewaan() -> pd.DataFrame:
    """Load riwayat penyewaan dengan caching"""
    try:
        df = pd.read_csv(RIWAYAT_PENYEWAAN_FILE)
        df['tanggal_sewa'] = pd.to_datetime(df['tanggal_sewa'], errors='coerce')
        # tanggal_kembali optional - jika ada, convert ke datetime
        if 'tanggal_kembali' in df.columns:
            df['tanggal_kembali'] = pd.to_datetime(df['tanggal_kembali'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading riwayat penyewaan: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL)
def load_riwayat_maintenance() -> pd.DataFrame:
    """Load riwayat maintenance dengan caching"""
    try:
        df = pd.read_csv(RIWAYAT_MAINTENANCE_FILE)
        df['tanggal_maintenance'] = pd.to_datetime(df['tanggal_maintenance'], errors='coerce')
        
        # Remove unwanted columns
        columns_to_drop = ['biaya_perbaikan', 'durasi_perbaikan_hari', 'teknisi']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
        
        return df
    except Exception as e:
        st.error(f"Error loading riwayat maintenance: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL)
def load_insight() -> pd.DataFrame:
    """Load insight kelayakan alat dengan caching"""
    try:
        df = pd.read_csv(INSIGHT_FILE)
        
        # Remove financial columns - focus only on equipment condition insights
        columns_to_drop = ['total_biaya_maintenance', 'estimated_revenue', 'cost_benefit_ratio']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
        
        return df
    except Exception as e:
        st.error(f"Error loading insight: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL)
def load_all_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load semua data sekaligus untuk performa optimal
    Returns: (katalog, penyewaan, maintenance, insight)
    
    Insight sekarang dihitung otomatis, bukan dari file CSV
    """
    from src.data.processor import calculate_equipment_feasibility
    
    katalog = load_katalog()
    penyewaan = load_riwayat_penyewaan()
    maintenance = load_riwayat_maintenance()
    
    # Generate insight secara otomatis dari data
    insight = calculate_equipment_feasibility(katalog, penyewaan, maintenance)
    
    return katalog, penyewaan, maintenance, insight


def refresh_cache():
    """Clear all cached data"""
    st.cache_data.clear()
    st.success("Cache berhasil di-refresh!")
