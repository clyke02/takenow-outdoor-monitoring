import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

@st.cache_data
def detect_buzzers_rule_based(user_activity):
    """Rule-based buzzer detection"""
    user_activity = user_activity.copy()
    user_activity['buzzer_score'] = 0
    
    # Criteria
    user_activity.loc[user_activity['posting_rate'] > 2, 'buzzer_score'] += 1
    user_activity.loc[user_activity['avg_text_similarity'] > 0.7, 'buzzer_score'] += 2
    user_activity.loc[user_activity['comment_count'] > 10, 'buzzer_score'] += 1
    user_activity.loc[user_activity['std_text_length'] < 2, 'buzzer_score'] += 1
    user_activity.loc[user_activity['duplicate_ratio'] > 0, 'buzzer_score'] += 2
    
    # Categorize
    user_activity['buzzer_category'] = pd.cut(
        user_activity['buzzer_score'],
        bins=[-1, 1, 3, 10],
        labels=['Low Suspicion', 'Medium Suspicion', 'High Suspicion']
    )
    
    return user_activity

@st.cache_data
def detect_buzzers_ml(user_activity):
    """Machine learning based buzzer detection"""
    user_activity = user_activity.copy()
    features = ['comment_count', 'posting_rate', 'avg_text_similarity',
                'std_text_length', 'duplicate_ratio']
    
    X = user_activity[features].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    iso_forest = IsolationForest(contamination=0.1, random_state=42, n_estimators=100)
    user_activity['ml_prediction'] = iso_forest.fit_predict(X_scaled)
    user_activity['ml_score'] = iso_forest.score_samples(X_scaled)
    user_activity['ml_label'] = user_activity['ml_prediction'].map({
        -1: 'Suspected Buzzer',
        1: 'Normal User'
    })
    
    return user_activity
