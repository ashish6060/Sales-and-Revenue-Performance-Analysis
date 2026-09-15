import streamlit as st

st.set_page_config(page_title="Business Insights", page_icon="💡", layout="wide")

st.title("💡 Business Insights & Recommendations")
st.markdown("Data-driven strategies derived from Exploratory Data Analysis and Machine Learning.")
st.markdown("---")

st.header("Key Findings")
col1, col2 = st.columns(2)

with col1:
    st.info("**Top Geographic Market:** The United Kingdom dominates sales, but secondary markets show high average order values.")
    st.info("**Time-Based Trends:** Peak shopping occurs between 12 PM and 3 PM, with massive seasonal spikes in November (Pre-Holiday).")

with col2:
    st.success("**VIP Customers:** A tiny fraction of the customer base (Champions) drives a disproportionately massive percentage of total revenue.")
    st.warning("**At-Risk Churn:** The largest segment by volume consists of one-off buyers who haven't returned to the store in over 6 months.")

st.markdown("---")
st.header("Actionable Recommendations")

st.markdown("""
### 1. Retention Strategy for 'At-Risk' Customers
*   **Action:** Deploy automated re-engagement email campaigns featuring personalized discount codes for customers who have not purchased in over 100 days.
*   **Goal:** Convert single-purchase, dormant users into returning customers before they completely churn.

### 2. Maximizing 'VIP' and 'Loyal' Value
*   **Action:** Introduce a tiered loyalty program offering early access to new product lines and dedicated support.
*   **Goal:** Maintain high retention rates and incentivize high-frequency buyers to consolidate their purchasing with this platform.

### 3. Geographical Expansion
*   **Action:** Allocate targeted digital marketing spend to growing secondary European markets (e.g., Germany, France) utilizing localized promotions.
*   **Goal:** Diversify revenue streams and reduce the heavy dependency on the domestic UK market.

### 4. Inventory & Server Optimization
*   **Action:** Scale up backend server capacity and pre-stock top-performing items well ahead of Q4.
*   **Goal:** Prevent stockouts and website crashes during peak historical shopping hours (mid-day) and peak seasonal months (November/December).
""")