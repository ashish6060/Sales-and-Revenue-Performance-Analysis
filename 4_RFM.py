import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RFM Analysis", page_icon="🎯", layout="wide")

st.title("🎯 RFM (Recency, Frequency, Monetary) Analysis")
st.markdown("Evaluating customer value based on their purchasing behavior.")
st.markdown("---")

@st.cache_data
def load_and_calculate_rfm():
    df = pd.read_excel("../data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] >= 1]
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Calculate RFM
    reference_date = df['InvoiceDate'].max() + pd.Timedelta('1 day')
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'Revenue': 'sum'
    }).reset_index()
    
    rfm.rename(columns={
        'InvoiceDate': 'Recency (Days)', 
        'InvoiceNo': 'Frequency (Orders)', 
        'Revenue': 'Monetary Value ($)'
    }, inplace=True)
    return rfm

with st.spinner("Calculating RFM Metrics..."):
    rfm_df = load_and_calculate_rfm()

st.subheader("RFM Data Overview")
st.dataframe(rfm_df.head(50), use_container_width=True)

st.markdown("---")
st.subheader("Metric Distributions")
st.markdown("Visualizing the spread of customer behavior. *(Note: Using logarithmic scale for clarity due to outliers)*")

col1, col2, col3 = st.columns(3)

with col1:
    fig_r = px.box(rfm_df, y='Recency (Days)', title="Recency Distribution")
    st.plotly_chart(fig_r, use_container_width=True)

with col2:
    fig_f = px.box(rfm_df, y='Frequency (Orders)', title="Frequency Distribution", log_y=True)
    st.plotly_chart(fig_f, use_container_width=True)

with col3:
    fig_m = px.box(rfm_df, y='Monetary Value ($)', title="Monetary Distribution", log_y=True)
    st.plotly_chart(fig_m, use_container_width=True)