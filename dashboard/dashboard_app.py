# dashboard_app.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart B2B Dashboard", layout="wide")

st.title("📦 Smart B2B Order Processing Dashboard")

# Load data
orders = pd.read_csv("../data/processed_orders.csv")
inventory = pd.read_csv("../data/inventory_updated.csv")
reorders = pd.read_csv("../data/reorder_requests.csv")

# KPI Section
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("✅ Total Orders", len(orders))

with col2:
    st.metric("📦 Total Stock", inventory["Stock"].sum())

with col3:
    st.metric("⚠️ Reorders", len(reorders))
    
# Show metrics
st.subheader("Processed Orders")
st.dataframe(orders)

st.subheader("Updated Inventory")
st.dataframe(inventory)

st.subheader("Reorder Requests")
st.dataframe(reorders)

