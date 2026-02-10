import pandas as pd
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_user_text_similarity(user_comments):
    """Calculate average text similarity for a user"""
    if len(user_comments) < 2:
        return 0
    
    vectorizer = TfidfVectorizer()
    try:
        X = vectorizer.fit_transform(user_comments)
        similarity = cosine_similarity(X)
        mask = ~np.eye(similarity.shape[0], dtype=bool)
        return similarity[mask].mean()
    except:
        return 0

@st.cache_data
def engineer_features(df):
    """Engineer features for buzzer detection"""
    # User activity features
    user_activity = df.groupby('authorDisplayName').agg({
        'publishedAt': ['count', 'min', 'max'],
        'textDisplay': 'count',
        'likeCount': 'mean'
    }).reset_index()
    
    user_activity.columns = ['author', 'comment_count', 'first_post', 'last_post', 
                              'total_comments', 'avg_likes']
    
    # Temporal features
    user_activity['time_span_hours'] = (user_activity['last_post'] - 
                                         user_activity['first_post']).dt.total_seconds() / 3600
    user_activity['posting_rate'] = user_activity['comment_count'] / (user_activity['time_span_hours'] + 1)
    
    # Text similarity
    user_activity['avg_text_similarity'] = user_activity['author'].apply(
        lambda x: calculate_user_text_similarity(
            df[df['authorDisplayName'] == x]['textDisplay'].values
        )
    )
    
    # Text length stats
    text_stats = df.groupby('authorDisplayName')['textLength'].agg(['mean', 'std', 'min', 'max']).reset_index()
    text_stats.columns = ['author', 'avg_text_length', 'std_text_length', 
                          'min_text_length', 'max_text_length']
    user_activity = user_activity.merge(text_stats, on='author', how='left')
    user_activity['std_text_length'].fillna(0, inplace=True)
    
    # Duplicate ratio
    duplicate_ratio = df.groupby('authorDisplayName').apply(
        lambda x: x.duplicated(subset=['textDisplay']).sum() / len(x)
    ).reset_index()
    duplicate_ratio.columns = ['author', 'duplicate_ratio']
    user_activity = user_activity.merge(duplicate_ratio, on='author', how='left')
    
    return user_activity
