"""
Data Processor Module
Handle transformasi dan agregasi data
"""
import pandas as pd
import streamlit as st
from typing import Dict, List, Tuple


@st.cache_data
def get_maintenance_summary(maintenance_df: pd.DataFrame) -> Dict:
    """Aggregasi summary maintenance"""
    if maintenance_df.empty:
        return {}
    
    summary = {
        'total_events': len(maintenance_df),
        'severity_dist': maintenance_df['severity'].value_counts().to_dict() if 'severity' in maintenance_df else {},
        'condition_dist': maintenance_df['kondisi_setelah_perbaikan'].value_counts().to_dict() if 'kondisi_setelah_perbaikan' in maintenance_df else {}
    }
    
    return summary


@st.cache_data
def get_top_maintenance_items(maintenance_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Get top N items dengan maintenance terbanyak"""
    if maintenance_df.empty:
        return pd.DataFrame()
    
    top_items = maintenance_df.groupby('kode_barang').agg({
        'id_maintenance': 'count'
    }).rename(columns={'id_maintenance': 'jumlah_maintenance'})
    
    top_items = top_items.sort_values('jumlah_maintenance', ascending=False).head(n)
    return top_items.reset_index()


@st.cache_data
def get_recommendation_distribution(insight_df: pd.DataFrame) -> pd.DataFrame:
    """Distribusi rekomendasi alat"""
    if insight_df.empty or 'rekomendasi' not in insight_df:
        return pd.DataFrame()
    
    dist = insight_df['rekomendasi'].value_counts().reset_index()
    dist.columns = ['Rekomendasi', 'Jumlah']
    return dist


@st.cache_data
def get_critical_items(insight_df: pd.DataFrame, threshold: float = 0.3) -> pd.DataFrame:
    """Get alat dengan maintenance ratio tinggi (kritis) atau kelayakan rendah"""
    if insight_df.empty:
        return pd.DataFrame()
    
    # Filter berdasarkan maintenance ratio ATAU kelayakan rendah
    critical = insight_df[
        (insight_df['maintenance_ratio'] > threshold) | 
        (insight_df.get('kelayakan', 100) < 70)
    ].copy()
    
    # No default sorting - maintain natural order
    # Users can sort via UI if needed
    
    # Pilih kolom yang relevan
    columns = ['kode_barang', 'nama_barang', 'freq_sewa', 'jumlah_maintenance', 'maintenance_ratio']
    if 'kelayakan' in critical.columns:
        columns.append('kelayakan')
    columns.append('rekomendasi')
    
    return critical[columns]


@st.cache_data
def get_rental_trends(penyewaan_df: pd.DataFrame) -> pd.DataFrame:
    """Trend penyewaan per bulan"""
    if penyewaan_df.empty or 'tanggal_sewa' not in penyewaan_df:
        return pd.DataFrame()
    
    # Filter hanya transaksi utama (yang punya nomor)
    main_df = penyewaan_df[penyewaan_df['no'].notna()].copy()
    
    if main_df.empty:
        return pd.DataFrame()
    
    main_df['bulan'] = main_df['tanggal_sewa'].dt.to_period('M')
    trends = main_df.groupby('bulan').size().reset_index()
    trends.columns = ['Bulan', 'Jumlah Transaksi']
    trends['Bulan'] = trends['Bulan'].astype(str)
    
    return trends


@st.cache_data
def get_revenue_by_category(penyewaan_df: pd.DataFrame, katalog_df: pd.DataFrame) -> pd.DataFrame:
    """Revenue per kategori"""
    if penyewaan_df.empty or katalog_df.empty:
        return pd.DataFrame()
    
    # Merge dengan katalog
    merged = penyewaan_df.merge(
        katalog_df[['kode_barang', 'kategori']], 
        on='kode_barang', 
        how='left'
    )
    
    # Clean harga satuan
    merged['harga_clean'] = merged['harga_satuan'].apply(clean_rupiah)
    merged['revenue'] = merged['harga_clean'] * merged['jumlah']
    
    # Aggregate per kategori
    revenue = merged.groupby('kategori')['revenue'].sum().reset_index()
    revenue.columns = ['Kategori', 'Total Revenue']
    revenue = revenue.sort_values('Total Revenue', ascending=False)
    
    return revenue


@st.cache_data
def get_utilization_rate(insight_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate utilization rate untuk top items"""
    if insight_df.empty:
        return pd.DataFrame()
    
    top_items = insight_df.nlargest(20, 'freq_sewa')[
        ['kode_barang', 'nama_barang', 'freq_sewa', 'total_hari_sewa', 'kategori']
    ].copy()
    
    return top_items


def clean_rupiah(val) -> float:
    """Convert Rupiah string ke float"""
    if pd.isna(val):
        return 0
    val_str = str(val).replace('Rp.', '').replace('RP.', '').replace('.', '').replace(',', '').strip()
    try:
        return float(val_str)
    except:
        return 0


def format_rupiah(value: float) -> str:
    """Format float ke Rupiah string"""
    try:
        return f"Rp. {value:,.0f}".replace(',', '.')
    except:
        return "Rp. 0"


def calculate_age_days(purchase_date: pd.Series, reference_date: pd.Timestamp = None) -> pd.Series:
    """Calculate umur alat dalam hari"""
    if reference_date is None:
        reference_date = pd.Timestamp.now()
    
    return (reference_date - purchase_date).dt.days


@st.cache_data
def calculate_equipment_feasibility(katalog_df: pd.DataFrame, penyewaan_df: pd.DataFrame, 
                                   maintenance_df: pd.DataFrame, reference_date: pd.Timestamp = None) -> pd.DataFrame:
    """
    Menghitung kelayakan alat secara otomatis berdasarkan:
    - Umur barang (sejak pembelian)
    - Frekuensi penyewaan
    - Total hari sewa
    - Riwayat maintenance dan severity
    - Recovery dari maintenance
    
    Kelayakan dimulai dari 100% dan berkurang seiring penggunaan
    """
    if katalog_df.empty:
        return pd.DataFrame()
    
    if reference_date is None:
        reference_date = pd.Timestamp.now()
    
    # Inisialisasi dataframe insight
    insight = katalog_df[['kode_barang', 'nama_barang', 'kategori', 'tanggal_pembelian']].copy()
    
    # Hitung umur barang dalam hari
    insight['umur_hari'] = (reference_date - insight['tanggal_pembelian']).dt.days
    
    # Agregasi data penyewaan per barang
    if not penyewaan_df.empty and 'kode_barang' in penyewaan_df.columns:
        # Cari kolom ID yang tersedia untuk counting
        id_col = None
        for col in ['id_penyewaan', 'no', 'id']:
            if col in penyewaan_df.columns:
                id_col = col
                break
        
        if id_col:
            rental_agg = penyewaan_df.groupby('kode_barang').agg({
                id_col: 'count',  # frekuensi sewa
                'durasi_sewa': 'sum'  # total hari sewa
            }).reset_index()
            rental_agg.columns = ['kode_barang', 'freq_sewa', 'total_hari_sewa']
        else:
            # Fallback: hitung dengan size()
            rental_agg = penyewaan_df.groupby('kode_barang').agg({
                'durasi_sewa': ['count', 'sum']
            }).reset_index()
            rental_agg.columns = ['kode_barang', 'freq_sewa', 'total_hari_sewa']
        
        insight = insight.merge(rental_agg, on='kode_barang', how='left')
    else:
        insight['freq_sewa'] = 0
        insight['total_hari_sewa'] = 0
    
    # Fill NaN dengan 0
    insight['freq_sewa'] = insight['freq_sewa'].fillna(0)
    insight['total_hari_sewa'] = insight['total_hari_sewa'].fillna(0)
    
    # Agregasi data maintenance per barang
    if not maintenance_df.empty and 'kode_barang' in maintenance_df.columns:
        maintenance_agg = maintenance_df.groupby('kode_barang').agg({
            'id_maintenance': 'count'
        }).reset_index()
        maintenance_agg.columns = ['kode_barang', 'jumlah_maintenance']
        
        insight = insight.merge(maintenance_agg, on='kode_barang', how='left')
        
        # Hitung impact dari maintenance (setiap maintenance = -0.2%)
        insight['maintenance_impact'] = insight['jumlah_maintenance'] * -0.2
    else:
        insight['jumlah_maintenance'] = 0
        insight['maintenance_impact'] = 0
    
    # Fill NaN
    insight['jumlah_maintenance'] = insight['jumlah_maintenance'].fillna(0)
    insight['maintenance_impact'] = insight['maintenance_impact'].fillna(0)
    
    # PERHITUNGAN KELAYAKAN
    # Mulai dari 100%
    insight['kelayakan'] = 100.0
    
    # Degradasi dari umur (0.01% per hari, max 20%)
    insight['kelayakan'] -= (insight['umur_hari'] * 0.01).clip(upper=20)
    
    # Degradasi dari frekuensi sewa (0.5% per sewa, max 30%)
    insight['kelayakan'] -= (insight['freq_sewa'] * 0.5).clip(upper=30)
    
    # Degradasi dari total hari sewa (0.05% per hari, max 20%)
    insight['kelayakan'] -= (insight['total_hari_sewa'] * 0.05).clip(upper=20)
    
    # Degradasi dari maintenance (0.2% per event, max 15%)
    impact_clipped = insight['maintenance_impact'].clip(lower=-15)
    insight['kelayakan'] += impact_clipped
    
    # Pastikan kelayakan dalam range 0-100
    insight['kelayakan'] = insight['kelayakan'].clip(lower=0, upper=100)
    
    # Hitung maintenance ratio
    insight['maintenance_ratio'] = 0.0
    mask = insight['freq_sewa'] > 0
    insight.loc[mask, 'maintenance_ratio'] = insight.loc[mask, 'jumlah_maintenance'] / insight.loc[mask, 'freq_sewa']
    
    # Tentukan rekomendasi berdasarkan kelayakan
    insight['rekomendasi'] = insight.apply(determine_recommendation, axis=1)
    
    # Pilih kolom yang akan ditampilkan
    result = insight[[
        'kode_barang', 'nama_barang', 'kategori', 
        'freq_sewa', 'total_hari_sewa', 'jumlah_maintenance', 
        'maintenance_ratio',
        'kelayakan', 'rekomendasi'
    ]].copy()
    
    # No default sorting - maintain natural order based on kode_barang
    # Users can sort via UI if needed
    
    return result


def calculate_maintenance_impact(maintenance_group: pd.DataFrame) -> float:
    """
    Hitung impact dari maintenance
    Semakin banyak maintenance = barang sering bermasalah = kelayakan turun
    Setiap maintenance event mengurangi 0.2% kelayakan
    """
    # Hitung jumlah maintenance events
    maintenance_count = len(maintenance_group)
    
    # Setiap maintenance = -0.2% (menunjukkan barang sering bermasalah)
    impact = maintenance_count * -0.2
    
    return impact


def determine_recommendation(row: pd.Series) -> str:
    """
    Tentukan rekomendasi berdasarkan persentase kelayakan saja
    Lebih simpel dan konsisten
    """
    kelayakan = row['kelayakan']
    
    # Kategori berdasarkan threshold kelayakan
    if kelayakan >= 85:
        return 'KONDISI SANGAT BAIK'
    elif kelayakan >= 70:
        return 'LAYAK OPERASIONAL'
    elif kelayakan >= 40:
        return 'TINGKATKAN PEMELIHARAAN'
    else:
        return 'PERLU PERHATIAN KHUSUS'


@st.cache_data
def get_category_performance(insight_df: pd.DataFrame) -> pd.DataFrame:
    """Get performance metrics per category"""
    if insight_df.empty:
        return pd.DataFrame()
    
    category_stats = insight_df.groupby('kategori').agg({
        'kelayakan': ['mean', 'min', 'max', 'count'],
        'freq_sewa': 'sum',
        'jumlah_maintenance': 'sum',
        'maintenance_ratio': 'mean'
    }).reset_index()
    
    category_stats.columns = [
        'kategori', 'avg_kelayakan', 'min_kelayakan', 'max_kelayakan', 
        'jumlah_items', 'total_sewa', 'total_maintenance', 'avg_maintenance_ratio'
    ]
    
    # Calculate ROI indicator (freq_sewa / jumlah_maintenance)
    category_stats['roi_indicator'] = 0.0
    mask = category_stats['total_maintenance'] > 0
    category_stats.loc[mask, 'roi_indicator'] = (
        category_stats.loc[mask, 'total_sewa'] / category_stats.loc[mask, 'total_maintenance']
    )
    
    # Sort by avg_kelayakan descending
    category_stats = category_stats.sort_values('avg_kelayakan', ascending=False)
    
    return category_stats


@st.cache_data
def get_strategic_insights(insight_df: pd.DataFrame) -> dict:
    """Generate strategic insights and recommendations"""
    if insight_df.empty:
        return {}
    
    insights = {}
    
    # Overall metrics
    insights['total_items'] = len(insight_df)
    insights['avg_kelayakan'] = insight_df['kelayakan'].mean()
    insights['total_sewa'] = insight_df['freq_sewa'].sum()
    insights['avg_utilization'] = insight_df['freq_sewa'].mean()
    insights['total_maintenance'] = insight_df['jumlah_maintenance'].sum()
    
    # Status distribution
    insights['status_dist'] = insight_df['rekomendasi'].value_counts().to_dict()
    
    # Critical items count
    insights['critical_count'] = len(insight_df[insight_df['kelayakan'] < 40])
    insights['warning_count'] = len(insight_df[(insight_df['kelayakan'] >= 40) & (insight_df['kelayakan'] < 70)])
    
    # Top performers
    insights['top_performers'] = insight_df.nlargest(5, 'freq_sewa')[['kode_barang', 'nama_barang', 'freq_sewa', 'kelayakan']].to_dict('records')
    
    # High maintenance burden
    insights['high_maintenance'] = insight_df.nlargest(5, 'maintenance_ratio')[['kode_barang', 'nama_barang', 'maintenance_ratio', 'jumlah_maintenance']].to_dict('records')
    
    # Investment priorities (high freq_sewa but declining kelayakan)
    investment_priority = insight_df[
        (insight_df['freq_sewa'] > insight_df['freq_sewa'].median()) & 
        (insight_df['kelayakan'] < 70)
    ].nlargest(10, 'freq_sewa')
    insights['investment_priority'] = investment_priority[['kode_barang', 'nama_barang', 'freq_sewa', 'kelayakan']].to_dict('records')
    
    return insights


@st.cache_data  
def classify_lifecycle_stage(insight_df: pd.DataFrame) -> pd.DataFrame:
    """Classify each item into lifecycle stage"""
    if insight_df.empty:
        return pd.DataFrame()
    
    result = insight_df.copy()
    
    def determine_stage(row):
        kelayakan = row['kelayakan']
        freq = row['freq_sewa']
        ratio = row['maintenance_ratio']
        
        # Stage classification
        if kelayakan >= 85 and freq > 0:
            return 'PRIME - Kondisi Optimal'
        elif kelayakan >= 70 and freq >= insight_df['freq_sewa'].median():
            return 'ACTIVE - Produktif'
        elif kelayakan >= 70 and freq < insight_df['freq_sewa'].median():
            return 'UNDERUTILIZED - Kurang Digunakan'
        elif kelayakan >= 40 and ratio < 0.5:
            return 'AGING - Perlu Perhatian'
        elif kelayakan >= 40 and ratio >= 0.5:
            return 'MAINTENANCE HEAVY - Beban Tinggi'
        else:
            return 'END OF LIFE - Pertimbangkan Penggantian'
    
    result['lifecycle_stage'] = result.apply(determine_stage, axis=1)
    
    return result
