"""
Visualization Charts Module
Komponen chart reusable untuk dashboard
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from typing import Dict, List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from config import STATUS_COLORS, SEVERITY_COLORS, CONDITION_COLORS, COLORS


def create_recommendation_pie_chart(dist_df: pd.DataFrame) -> go.Figure:
    """Pie chart distribusi rekomendasi"""
    if dist_df.empty:
        return go.Figure()
    
    colors = [STATUS_COLORS.get(rec, COLORS['secondary']) for rec in dist_df['Rekomendasi']]
    
    fig = go.Figure(data=[go.Pie(
        labels=dist_df['Rekomendasi'],
        values=dist_df['Jumlah'],
        marker=dict(colors=colors),
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>',
        textposition='inside'
    )])
    
    fig.update_layout(
        title={
            'text': "Distribusi Rekomendasi Kelayakan Alat",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=400,
        margin=dict(t=60, b=80, l=20, r=20)
    )
    
    return fig


def create_severity_bar_chart(severity_dist: Dict) -> go.Figure:
    """Bar chart distribusi severity maintenance"""
    if not severity_dist:
        return go.Figure()
    
    df = pd.DataFrame(list(severity_dist.items()), columns=['Severity', 'Jumlah'])
    colors = [SEVERITY_COLORS.get(sev, COLORS['secondary']) for sev in df['Severity']]
    
    fig = go.Figure(data=[go.Bar(
        x=df['Severity'],
        y=df['Jumlah'],
        marker_color=colors,
        text=df['Jumlah'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Distribusi Tingkat Kerusakan",
        xaxis_title="Severity",
        yaxis_title="Jumlah Event",
        height=320  # Reduced from 350
    )
    
    return fig


def create_condition_bar_chart(condition_dist: Dict) -> go.Figure:
    """Bar chart distribusi kondisi setelah perbaikan"""
    if not condition_dist:
        return go.Figure()
    
    df = pd.DataFrame(list(condition_dist.items()), columns=['Kondisi', 'Jumlah'])
    colors = [CONDITION_COLORS.get(cond, COLORS['secondary']) for cond in df['Kondisi']]
    
    fig = go.Figure(data=[go.Bar(
        x=df['Kondisi'],
        y=df['Jumlah'],
        marker_color=colors,
        text=df['Jumlah'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Kondisi Alat Setelah Perbaikan",
        xaxis_title="Kondisi",
        yaxis_title="Jumlah Alat",
        height=350
    )
    
    return fig


def create_top_maintenance_chart(top_items_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart top items maintenance"""
    if top_items_df.empty:
        return go.Figure()
    
    fig = go.Figure(data=[go.Bar(
        y=top_items_df['nama_barang'],
        x=top_items_df['jumlah_maintenance'],
        orientation='h',
        marker_color=COLORS['danger'],
        text=top_items_df['jumlah_maintenance'],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Kode: ' + top_items_df['kode_barang'] + 
                      '<br>Maintenance: %{x}x<extra></extra>'
    )])
    
    fig.update_layout(
        title="Top 10 Alat dengan Maintenance Terbanyak",
        xaxis_title="Jumlah Maintenance",
        yaxis_title="",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def create_rental_trend_chart(trends_df: pd.DataFrame) -> go.Figure:
    """Line chart trend penyewaan"""
    if trends_df.empty:
        return go.Figure()
    
    fig = go.Figure(data=[go.Scatter(
        x=trends_df['Bulan'],
        y=trends_df['Jumlah Transaksi'],
        mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Transaksi: %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Trend Penyewaan Bulanan",
        xaxis_title="Bulan",
        yaxis_title="Jumlah Transaksi",
        height=350
    )
    
    return fig


def create_maintenance_ratio_chart(critical_df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Bar chart maintenance ratio untuk critical items"""
    if critical_df.empty:
        return go.Figure()
    
    data = critical_df.head(top_n).copy()
    
    # Color berdasarkan severity
    colors = []
    for ratio in data['maintenance_ratio']:
        if ratio > 0.5:
            colors.append(COLORS['danger'])
        elif ratio > 0.3:
            colors.append(COLORS['warning'])
        else:
            colors.append(COLORS['info'])
    
    fig = go.Figure(data=[go.Bar(
        y=data['nama_barang'],
        x=data['maintenance_ratio'] * 100,
        orientation='h',
        marker_color=colors,
        text=[f"{val:.1f}%" for val in data['maintenance_ratio'] * 100],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Ratio: %{x:.1f}%<br>' +
                      'Freq: ' + data['freq_sewa'].astype(str) + 
                      '<br>Maintenance: ' + data['jumlah_maintenance'].astype(str) +
                      '<extra></extra>'
    )])
    
    fig.update_layout(
        title=f"Top {top_n} Alat dengan Maintenance Ratio Tertinggi",
        xaxis_title="Maintenance Ratio (%)",
        yaxis_title="",
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def create_revenue_by_category_chart(revenue_df: pd.DataFrame) -> go.Figure:
    """Bar chart revenue per kategori"""
    if revenue_df.empty:
        return go.Figure()
    
    fig = go.Figure(data=[go.Bar(
        x=revenue_df['Kategori'],
        y=revenue_df['Total Revenue'],
        marker_color=COLORS['success'],
        text=[f"Rp. {val/1e6:.1f}M" for val in revenue_df['Total Revenue']],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Revenue: Rp. %{y:,.0f}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Revenue per Kategori Alat",
        xaxis_title="Kategori",
        yaxis_title="Total Revenue (Rp)",
        height=400,
        xaxis={'tickangle': -45}
    )
    
    return fig


def create_utilization_chart(util_df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Bar chart utilisasi alat"""
    if util_df.empty:
        return go.Figure()
    
    data = util_df.head(top_n)
    
    fig = go.Figure(data=[go.Bar(
        y=data['nama_barang'],
        x=data['freq_sewa'],
        orientation='h',
        marker_color=COLORS['info'],
        text=data['freq_sewa'],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Freq: %{x}x<br>' +
                      'Total Hari: ' + data['total_hari_sewa'].astype(str) +
                      '<extra></extra>'
    )])
    
    fig.update_layout(
        title=f"Top {top_n} Alat Paling Sering Disewa",
        xaxis_title="Frekuensi Sewa",
        yaxis_title="",
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def create_scatter_feasibility_utilization(insight_df: pd.DataFrame) -> go.Figure:
    """Scatter plot freq_sewa vs kelayakan colored by kategori"""
    if insight_df.empty:
        return go.Figure()
    
    # Sample data if too large
    if len(insight_df) > 200:
        plot_df = insight_df.sample(n=200, random_state=42)
    else:
        plot_df = insight_df
    
    fig = px.scatter(
        plot_df,
        x='freq_sewa',
        y='kelayakan',
        color='kategori',
        size='total_hari_sewa',
        hover_data=['kode_barang', 'nama_barang'],
        title="Analisis Pola: Utilisasi vs Kelayakan Alat",
        labels={
            'freq_sewa': 'Frekuensi Sewa',
            'kelayakan': 'Kelayakan (%)',
            'kategori': 'Kategori'
        }
    )
    
    fig.update_layout(
        height=450,  # Reduced from 500
        xaxis_title="Frekuensi Sewa (x)",
        yaxis_title="Kelayakan (%)"
    )
    
    # Disable animation for better performance
    fig.layout.transition = {'duration': 0}
    
    return fig


def create_box_feasibility_by_category(insight_df: pd.DataFrame) -> go.Figure:
    """Box plot distribusi kelayakan per kategori"""
    if insight_df.empty:
        return go.Figure()
    
    fig = px.box(
        insight_df,
        x='kategori',
        y='kelayakan',
        color='kategori',
        title="Distribusi Kelayakan per Kategori",
        labels={
            'kategori': 'Kategori',
            'kelayakan': 'Kelayakan (%)'
        },
        points='outliers'
    )
    
    fig.update_layout(
        height=400,  # Reduced from 450
        xaxis_title="Kategori",
        yaxis_title="Kelayakan (%)",
        showlegend=False,
        xaxis={'tickangle': -45}
    )
    
    return fig


def create_heatmap_maintenance_burden(insight_df: pd.DataFrame) -> go.Figure:
    """Heatmap maintenance_ratio per kategori"""
    if insight_df.empty:
        return go.Figure()
    
    # Aggregate by category
    heatmap_data = insight_df.groupby('kategori').agg({
        'maintenance_ratio': 'mean',
        'jumlah_maintenance': 'sum',
        'freq_sewa': 'sum'
    }).reset_index()
    
    # Create pivot for heatmap
    heatmap_data['avg_ratio_pct'] = heatmap_data['maintenance_ratio'] * 100
    
    fig = go.Figure(data=go.Bar(
        x=heatmap_data['kategori'],
        y=heatmap_data['avg_ratio_pct'],
        marker=dict(
            color=heatmap_data['avg_ratio_pct'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="Ratio (%)")
        ),
        text=[f"{val:.1f}%" for val in heatmap_data['avg_ratio_pct']],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Avg Ratio: %{y:.1f}%<br>' +
                      'Total Maintenance: ' + heatmap_data['jumlah_maintenance'].astype(str) +
                      '<extra></extra>'
    ))
    
    fig.update_layout(
        title="Beban Maintenance per Kategori",
        xaxis_title="Kategori",
        yaxis_title="Rata-rata Maintenance Ratio (%)",
        height=350,  # Reduced from 400
        xaxis={'tickangle': -45}
    )
    
    return fig


def create_quadrant_lifecycle(insight_df: pd.DataFrame) -> go.Figure:
    """Quadrant chart: freq_sewa vs maintenance_ratio"""
    if insight_df.empty:
        return go.Figure()
    
    # Sample data if too large for performance
    if len(insight_df) > 150:
        plot_df = insight_df.sample(n=150, random_state=42)
    else:
        plot_df = insight_df.copy()
    
    # Calculate medians for quadrant lines
    median_freq = plot_df['freq_sewa'].median()
    median_ratio = plot_df['maintenance_ratio'].median()
    
    # Determine quadrant for each item
    def get_quadrant(row):
        if row['freq_sewa'] >= median_freq and row['maintenance_ratio'] < median_ratio:
            return 'High Value / Low Maintenance'
        elif row['freq_sewa'] >= median_freq and row['maintenance_ratio'] >= median_ratio:
            return 'High Value / High Maintenance'
        elif row['freq_sewa'] < median_freq and row['maintenance_ratio'] < median_ratio:
            return 'Low Value / Low Maintenance'
        else:
            return 'Low Value / High Maintenance'
    
    plot_df['quadrant'] = plot_df.apply(get_quadrant, axis=1)
    
    fig = px.scatter(
        plot_df,
        x='freq_sewa',
        y='maintenance_ratio',
        color='quadrant',
        size='kelayakan',
        hover_data=['kode_barang', 'nama_barang', 'kategori'],
        title="Matriks Lifecycle Aset: Nilai vs Beban Maintenance",
        labels={
            'freq_sewa': 'Frekuensi Sewa (Nilai)',
            'maintenance_ratio': 'Maintenance Ratio (Beban)',
            'quadrant': 'Kategori Lifecycle'
        },
        color_discrete_map={
            'High Value / Low Maintenance': '#2ecc71',
            'High Value / High Maintenance': '#f39c12',
            'Low Value / Low Maintenance': '#3498db',
            'Low Value / High Maintenance': '#e74c3c'
        }
    )
    
    # Add quadrant lines
    fig.add_hline(y=median_ratio, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=median_freq, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add annotations for quadrants
    max_freq = plot_df['freq_sewa'].max()
    max_ratio = plot_df['maintenance_ratio'].max()
    
    fig.add_annotation(x=max_freq*0.75, y=max_ratio*0.25, text="IDEAL", showarrow=False, 
                      font=dict(size=14, color="green"), opacity=0.3)
    fig.add_annotation(x=max_freq*0.75, y=max_ratio*0.75, text="PERHATIAN", showarrow=False,
                      font=dict(size=14, color="orange"), opacity=0.3)
    fig.add_annotation(x=max_freq*0.25, y=max_ratio*0.25, text="RENDAH", showarrow=False,
                      font=dict(size=14, color="blue"), opacity=0.3)
    fig.add_annotation(x=max_freq*0.25, y=max_ratio*0.75, text="KRITIS", showarrow=False,
                      font=dict(size=14, color="red"), opacity=0.3)
    
    fig.update_layout(
        height=480,  # Reduced from 550
        xaxis_title="Frekuensi Sewa (Nilai Utilisasi)",
        yaxis_title="Maintenance Ratio (Beban Pemeliharaan)"
    )
    
    return fig


def create_gauge_chart(value: float, title: str, max_value: float = 100, 
                       thresholds: dict = None) -> go.Figure:
    """Create gauge chart for KPI"""
    if thresholds is None:
        thresholds = {'low': 40, 'medium': 70, 'high': 85}
    
    # Determine color based on value
    if value >= thresholds['high']:
        color = '#2ecc71'
    elif value >= thresholds['medium']:
        color = '#f39c12'
    elif value >= thresholds['low']:
        color = '#e67e22'
    else:
        color = '#e74c3c'
    
    # Determine threshold line position based on value
    if value >= thresholds['medium']:
        threshold_line = thresholds['medium']
    else:
        threshold_line = thresholds['low']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 18}},
        delta={'reference': thresholds['medium'], 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, thresholds['low']], 'color': '#ffebee'},
                {'range': [thresholds['low'], thresholds['medium']], 'color': '#fff3e0'},
                {'range': [thresholds['medium'], thresholds['high']], 'color': '#e8f5e9'},
                {'range': [thresholds['high'], max_value], 'color': '#c8e6c9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold_line
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig
