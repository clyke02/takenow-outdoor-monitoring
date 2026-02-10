import streamlit as st
import plotly.express as px

def show_dashboard(df, user_activity):
    """Dashboard page"""
    st.header("📊 Dashboard Overview")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Komentar", f"{len(df):,}")
    with col2:
        st.metric("Total Users", f"{len(user_activity):,}")
    with col3:
        high_suspicion = len(user_activity[user_activity['buzzer_category'] == 'High Suspicion'])
        st.metric("High Suspicion", high_suspicion, 
                  delta=f"{high_suspicion/len(user_activity)*100:.1f}%")
    with col4:
        ml_buzzers = len(user_activity[user_activity['ml_label'] == 'Suspected Buzzer'])
        st.metric("ML Suspected", ml_buzzers,
                  delta=f"{ml_buzzers/len(user_activity)*100:.1f}%")
    
    st.markdown("---")
    
    # Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribusi Kategori (Rule-Based)")
        category_counts = user_activity['buzzer_category'].value_counts()
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            color_discrete_sequence=['#90EE90', '#FFD700', '#FF6347']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Distribusi ML Prediction")
        ml_counts = user_activity['ml_label'].value_counts()
        fig = px.pie(
            values=ml_counts.values,
            names=ml_counts.index,
            color_discrete_sequence=['#87CEEB', '#FF69B4']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Buzzer Score Distribution
    st.subheader("Distribusi Buzzer Score")
    fig = px.histogram(
        user_activity,
        x='buzzer_score',
        nbins=9,
        color='buzzer_category',
        color_discrete_sequence=['#90EE90', '#FFD700', '#FF6347']
    )
    fig.update_layout(xaxis_title="Buzzer Score", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Suspected Buzzers
    st.subheader("🚨 Top 10 Suspected Buzzers")
    top_buzzers = user_activity.sort_values('buzzer_score', ascending=False).head(10)
    
    display_cols = ['author', 'comment_count', 'posting_rate', 'avg_text_similarity',
                    'duplicate_ratio', 'buzzer_score', 'buzzer_category']
    
    st.dataframe(
        top_buzzers[display_cols].style.background_gradient(
            subset=['buzzer_score'], cmap='Reds'
        ),
        use_container_width=True
    )
