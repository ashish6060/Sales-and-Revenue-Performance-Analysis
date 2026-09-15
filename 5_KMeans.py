import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from sklearn.metrics import silhouette_score

st.set_page_config(page_title="Customer Segmentation", page_icon="👥", layout="wide")
st.title("👥 K-Means Customer Segmentation")
st.markdown("Machine learning clustering to identify actionable customer profiles based on RFM metrics.")
st.markdown("---")

# 1. Load Data and RFM Table
@st.cache_data
def load_rfm_data():
    df = pd.read_excel("../data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] >= 1]
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    reference_date = df['InvoiceDate'].max() + pd.Timedelta('1 day')
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'Revenue': 'sum'
    }).reset_index()
    rfm.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'Revenue': 'Monetary'}, inplace=True)
    return rfm

try:
    rfm = load_rfm_data()
    
    # 2. Load Models
    scaler = joblib.load('../models/scaler.pkl')
    kmeans_model = joblib.load('../models/kmeans.pkl')
    
    # 3. Scale and Predict
    rfm_scaled = scaler.transform(rfm[['Recency', 'Frequency', 'Monetary']])
    rfm['Cluster'] = kmeans_model.predict(rfm_scaled)
    
    # Assign Business Labels to Clusters (Adjust based on your specific cluster outputs)
    cluster_names = {0: 'At Risk', 1: 'VIP / Champions', 2: 'Loyal Customers', 3: 'Casual Shoppers'}
    rfm['Segment'] = rfm['Cluster'].map(cluster_names)
    
    # 4. Evaluation Metric
    sil_score = silhouette_score(rfm_scaled, rfm['Cluster'])
    
    st.subheader("Model Evaluation")
    st.metric("Silhouette Score", f"{sil_score:.4f}")
    st.markdown("*(A score closer to 1 indicates well-defined, distinct clusters)*")
    st.markdown("---")
    
    # 5. Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Customer Distribution")
        cluster_counts = rfm['Segment'].value_counts().reset_index()
        cluster_counts.columns = ['Segment', 'Count']
        fig_pie = px.pie(cluster_counts, values='Count', names='Segment', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.subheader("Cluster Profile (Recency vs Monetary)")
        # log_y is used because Monetary values can have massive outliers
        fig_scatter = px.scatter(rfm, x='Recency', y='Monetary', color='Segment', log_y=True, hover_data=['Frequency'])
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    # 6. Cluster Summary Table
    st.subheader("Cluster Summary Averages")
    summary = rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().round(2)
    st.dataframe(summary, use_container_width=True)
    
except FileNotFoundError:
    st.error("Model files not found! Ensure scaler.pkl and kmeans.pkl exist in the '../models/' directory.")