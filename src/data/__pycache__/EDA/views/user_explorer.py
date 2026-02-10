import streamlit as st

def show_user_explorer(df, user_activity):
    """User explorer page"""
    st.header("👤 User Explorer")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.multiselect(
            "Filter by Category",
            options=['Low Suspicion', 'Medium Suspicion', 'High Suspicion'],
            default=['High Suspicion', 'Medium Suspicion']
        )
    
    with col2:
        ml_filter = st.multiselect(
            "Filter by ML Label",
            options=['Normal User', 'Suspected Buzzer'],
            default=['Suspected Buzzer']
        )
    
    # Apply filters
    filtered = user_activity[
        (user_activity['buzzer_category'].isin(category_filter)) &
        (user_activity['ml_label'].isin(ml_filter))
    ]
    
    st.write(f"Found {len(filtered)} users matching filters")
    
    # Select user
    selected_user = st.selectbox(
        "Select User to Inspect:",
        options=filtered['author'].tolist()
    )
    
    if selected_user:
        user_data = user_activity[user_activity['author'] == selected_user].iloc[0]
        user_comments = df[df['authorDisplayName'] == selected_user]
        
        # User stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Buzzer Score", int(user_data['buzzer_score']))
            st.metric("Category", user_data['buzzer_category'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Comment Count", int(user_data['comment_count']))
            st.metric("Posting Rate", f"{user_data['posting_rate']:.2f}/hour")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Text Similarity", f"{user_data['avg_text_similarity']:.4f}")
            st.metric("Duplicate Ratio", f"{user_data['duplicate_ratio']:.2%}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Comments
        st.subheader(f"Comments by {selected_user}")
        st.dataframe(
            user_comments[['publishedAt', 'textDisplay', 'likeCount']].sort_values('publishedAt'),
            use_container_width=True
        )
