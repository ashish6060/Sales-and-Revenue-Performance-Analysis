import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPI Dashboard", page_icon="📊", layout="wide")

st.title("📊 Key Performance Indicators")
st.markdown("---")

# Use st.cache_data to load the dataset only once
@st.cache_data
def load_data():
    df = pd.read_excel("../data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] >= 1]
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

with st.spinner("Loading Data..."):
    df = load_data()

# Calculate KPIs
total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
total_products = df['Description'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

# Display KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Total Products", f"{total_products:,}")
col5.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")
st.subheader("Dataset Overview")
st.dataframe(df.head(100), use_container_width=True) # Display a sample