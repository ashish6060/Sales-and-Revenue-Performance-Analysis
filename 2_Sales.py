import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analysis", page_icon="📈", layout="wide")

st.title("📈 Sales Performance Analysis")
st.markdown("Explore order trends over time and across different regions.")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("../data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Month'] = df['InvoiceDate'].dt.month_name()
    df['Hour'] = df['InvoiceDate'].dt.hour
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox("Select Country", options=["All"] + list(df['Country'].unique()))

# Apply Filter
if selected_country != "All":
    filtered_df = df[df['Country'] == selected_country]
else:
    filtered_df = df

# Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Orders by Month")
    monthly_sales = filtered_df.groupby('Month')['InvoiceNo'].nunique().reset_index()
    # Sort months chronologically
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthly_sales['Month'] = pd.Categorical(monthly_sales['Month'], categories=months_order, ordered=True)
    monthly_sales = monthly_sales.sort_values('Month')
    
    fig_month = px.line(monthly_sales, x='Month', y='InvoiceNo', markers=True, title="Monthly Order Volume")
    st.plotly_chart(fig_month, use_container_width=True)

with col2:
    st.subheader("Peak Shopping Hours")
    hourly_sales = filtered_df.groupby('Hour')['InvoiceNo'].nunique().reset_index()
    fig_hour = px.bar(hourly_sales, x='Hour', y='InvoiceNo', title="Orders by Hour of Day", color='InvoiceNo', color_continuous_scale='Blues')
    st.plotly_chart(fig_hour, use_container_width=True)