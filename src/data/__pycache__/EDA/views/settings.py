import streamlit as st

def show_settings():
    """Settings page"""
    st.header("⚙️ Settings & Export")
    
    st.subheader("Export Data")
    
    if st.button("Generate CSV Export"):
        st.success("Export generated! Download below:")
        st.download_button(
            label="Download buzzer_detection_results.csv",
            data="Sample data",
            file_name="buzzer_detection_results.csv",
            mime="text/csv"
        )
    
    st.subheader("About")
    st.markdown("""
    ### Sistem Deteksi Buzzer MBG
    
    **Versi:** 1.0
    
    **Metodologi:**
    - Rule-Based Detection (6 kriteria)
    - Machine Learning (Isolation Forest)
    - Network Analysis (Text Similarity)
    
    **Dataset:** Komentar YouTube tentang Program Makan Bergizi Gratis
    
    **Developed by:** Tim Penelitian PSD
    """)
