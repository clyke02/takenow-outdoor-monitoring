import pandas as pd
import streamlit as st
import re

@st.cache_data
def load_data():
    """Load the YouTube comments datasets"""
    try:
        data_4287 = pd.read_csv('dataset/youtube-comments-4287.csv')
        data_4287['video_id'] = 'video_1'
        data_1970 = pd.read_csv('dataset/youtube-comments-1970.csv')
        data_1970['video_id'] = 'video_2'
        data_399 = pd.read_csv('dataset/youtube-comments-399.csv')
        data_399['video_id'] = 'video_3'
        
        merged_data = pd.concat([data_4287, data_1970, data_399], ignore_index=True)
        return merged_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def clean_text(text):
    """Clean text data"""
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.replace('dapet', 'dapat')
    return text

@st.cache_data
def preprocess_data(df):
    """Preprocess the data"""
    df = df.copy()
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    df['textDisplay'] = df['textDisplay'].apply(clean_text)
    df['textLength'] = df['textDisplay'].apply(lambda x: len(str(x).split()))
    df['hour'] = df['publishedAt'].dt.hour
    df['day_of_week'] = df['publishedAt'].dt.dayofweek
    return df
