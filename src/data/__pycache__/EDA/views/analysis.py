import streamlit as st
import pandas as pd
import plotly.express as px

def show_analysis(df, user_activity):
    """Analysis page"""
    st.header("📈 Analisis Detail")
    
    # Scatter plot
    st.subheader("Posting Rate vs Text Similarity")
    fig = px.scatter(
        user_activity,
        x='posting_rate',
        y='avg_text_similarity',
        color='buzzer_score',
        size='comment_count',
        hover_data=['author', 'buzzer_category'],
        color_continuous_scale='RdYlGn_r'
    )
    fig.add_hline(y=0.7, line_dash="dash", line_color="red", 
                  annotation_text="High Similarity Threshold")
    fig.add_vline(x=2, line_dash="dash", line_color="orange",
                  annotation_text="High Rate Threshold")
    st.plotly_chart(fig, use_container_width=True)
    
    # Box plots
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Comment Count by Category")
        fig = px.box(
            user_activity,
            x='buzzer_category',
            y='comment_count',
            color='buzzer_category',
            color_discrete_sequence=['#90EE90', '#FFD700', '#FF6347']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Text Similarity by Category")
        fig = px.box(
            user_activity,
            x='buzzer_category',
            y='avg_text_similarity',
            color='buzzer_category',
            color_discrete_sequence=['#90EE90', '#FFD700', '#FF6347']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Temporal analysis
    st.subheader("⏰ Temporal Analysis")
    hourly_activity = df.groupby('hour').size().reset_index(name='count')
    fig = px.line(
        hourly_activity,
        x='hour',
        y='count',
        markers=True
    )
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Number of Comments")
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison table
    st.subheader("📊 Perbandingan Rule-Based vs ML")
    comparison = pd.crosstab(
        user_activity['buzzer_category'],
        user_activity['ml_label'],
        margins=True
    )
    st.dataframe(comparison, use_container_width=True)
    
    # Agreement analysis
    high_confidence = user_activity[
        (user_activity['buzzer_category'] == 'High Suspicion') &
        (user_activity['ml_label'] == 'Suspected Buzzer')
    ]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rule-Based High", 
                  len(user_activity[user_activity['buzzer_category'] == 'High Suspicion']))
    with col2:
        st.metric("ML Suspected", 
                  len(user_activity[user_activity['ml_label'] == 'Suspected Buzzer']))
    with col3:
        st.metric("High Confidence (Both)", len(high_confidence))
