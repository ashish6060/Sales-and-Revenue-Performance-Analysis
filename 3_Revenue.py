import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Revenue Analysis", page_icon="💰", layout="wide")

st.title("💰 Revenue Analysis")
st.markdown("Deep dive into revenue generation across time, countries, and products.")
st.markdown("---")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("../data/Online_Retail.xlsx")
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] >= 1]
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Month'] = df['InvoiceDate'].dt.strftime('%Y-%m') # Year-Month format for trend
    return df

with st.spinner("Loading Revenue Data..."):
    df = load_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Revenue Trend")
    monthly_rev = df.groupby('Month')['Revenue'].sum().reset_index()
    monthly_rev = monthly_rev.sort_values('Month')
    fig_trend = px.line(monthly_rev, x='Month', y='Revenue', markers=True, title="Revenue Over Time")
    fig_trend.update_yaxes(tickprefix="$")
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("Top 10 Revenue-Generating Countries")
    country_rev = df.groupby('Country')['Revenue'].sum().reset_index()
    country_rev = country_rev.sort_values('Revenue', ascending=False).head(10)
    fig_country = px.bar(country_rev, x='Revenue', y='Country', orientation='h', title="Revenue by Country", color='Revenue', color_continuous_scale='Greens')
    fig_country.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_country, use_container_width=True)

st.markdown("---")
st.subheader("Top 10 Best-Selling Products by Revenue")
product_rev = df.groupby('Description')['Revenue'].sum().reset_index()
product_rev = product_rev.sort_values('Revenue', ascending=False).head(10)
fig_product = px.bar(product_rev, x='Revenue', y='Description', orientation='h', color='Revenue', color_continuous_scale='Oranges')
fig_product.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_product, use_container_width=True)