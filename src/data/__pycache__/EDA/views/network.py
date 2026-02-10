import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def show_network(df, user_activity):
    """Network analysis page"""
    st.header("🕸️ Network Analysis")
    
    st.info("Creating network based on text similarity between users...")
    
    # Create corpus
    author_corpus = df.groupby("authorDisplayName")["textDisplay"].apply(lambda x: " ".join(x))
    
    custom_stopwords = ['aku', 'di', 'yang', 'nya', 'itu', 'kak', 'saya', 
                        'dari', 'tapi', 'juga', 'ya']
    
    vectorizer = TfidfVectorizer(stop_words=custom_stopwords, min_df=3, max_df=0.85)
    X_tfidf = vectorizer.fit_transform(author_corpus)
    
    similarity_matrix = cosine_similarity(X_tfidf)
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=author_corpus.index,
        columns=author_corpus.index
    )
    
    # Create network
    threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.3, 0.05)
    
    G = nx.Graph()
    for i in similarity_df.index:
        for j in similarity_df.columns:
            if i != j and similarity_df.loc[i, j] > threshold:
                G.add_edge(i, j, weight=similarity_df.loc[i, j])
    
    # Network stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nodes", G.number_of_nodes())
    with col2:
        st.metric("Edges", G.number_of_edges())
    with col3:
        if G.number_of_nodes() > 0:
            avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
            st.metric("Avg Degree", f"{avg_degree:.2f}")
    with col4:
        if G.number_of_nodes() > 0:
            density = nx.density(G)
            st.metric("Density", f"{density:.4f}")
    
    # Visualize
    if G.number_of_nodes() > 0 and G.number_of_nodes() < 200:
        st.subheader("Network Visualization")
        
        fig, ax = plt.subplots(figsize=(15, 10))
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
        
        # Node colors based on buzzer category
        node_colors = []
        for node in G.nodes():
            if node in user_activity['author'].values:
                category = user_activity[user_activity['author'] == node]['buzzer_category'].values[0]
                if category == 'High Suspicion':
                    node_colors.append('red')
                elif category == 'Medium Suspicion':
                    node_colors.append('orange')
                else:
                    node_colors.append('lightblue')
            else:
                node_colors.append('gray')
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100, alpha=0.7, ax=ax)
        nx.draw_networkx_edges(G, pos, alpha=0.2, ax=ax)
        
        ax.set_title("Social Network (Red=High Suspicion, Orange=Medium, Blue=Low)")
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.warning(f"Network too large ({G.number_of_nodes()} nodes) or empty. Adjust threshold.")
    
    # Top central nodes
    if G.number_of_nodes() > 0:
        st.subheader("Top 10 Central Users")
        degree_centrality = nx.degree_centrality(G)
        top_central = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        central_df = pd.DataFrame(top_central, columns=['Author', 'Centrality'])
        st.dataframe(central_df, use_container_width=True)
