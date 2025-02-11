import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# ✅ Correct File Paths
excel_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"
logo_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Logo.jpeg"
sheet_name = "Inventory"

# 🔥 Custom Header with Logo and Text
st.markdown(
    f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <img src="{logo_url}" width="48" height="48" style="margin-right: 15px;">
        <div>
            <h2 style="margin: 0; font-size: 20px; color: #333;">Centralized Mess</h2>
            <h4 style="margin: 0; font-size: 14px; color: #666;">Liberty Eco Campus Nooriabad</h4>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔥 Load Excel File from GitHub
try:
    response = requests.get(excel_url)
    response.raise_for_status()
    file_bytes = BytesIO(response.content)
    df = pd.read_excel(file_bytes, sheet_name=sheet_name)
except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()

# ✅ Data Cleaning
required_columns = ["Date", "Item Description", "Category", "Quantity", "UOM", "Price", "Vendor"]
for col in required_columns:
    if col not in df.columns:
        st.error(f"❌ Missing required column: {col}")
        st.stop()

df.fillna({
    "Quantity": 0, 
    "Price": 0, 
    "Category": "Unknown", 
    "Vendor": "Unknown", 
    "UOM": "N/A"
}, inplace=True)

# 🎯 Enhanced Sidebar Filters
st.sidebar.header("🔍 **Advanced Filters**")

# Category Filter
category_options = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox(
    "Select Category", 
    category_options,
    index=0
)

# UOM Filter
uom_options = ["All"] + sorted(df["UOM"].unique().tolist())
selected_uom = st.sidebar.selectbox(
    "Select Unit of Measure", 
    uom_options,
    index=0
)

# Vendor Filter
vendor_options = ["All"] + sorted(df["Vendor"].unique().tolist())
selected_vendor = st.sidebar.selectbox(
    "Select Vendor", 
    vendor_options,
    index=0
)

# Quantity and Price Filters
quantity_range = st.sidebar.slider(
    "Select Quantity Range",
    min_value=int(df["Quantity"].min()),
    max_value=int(df["Quantity"].max()),
    value=(int(df["Quantity"].min()), int(df["Quantity"].max()))
)

price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=int(df["Price"].min()),
    max_value=int(df["Price"].max()),
    value=(int(df["Price"].min()), int(df["Price"].max()))
)

# 🔄 Apply Filters
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_uom != "All":
    filtered_df = filtered_df[filtered_df["UOM"] == selected_uom]

if selected_vendor != "All":
    filtered_df = filtered_df[filtered_df["Vendor"] == selected_vendor]

filtered_df = filtered_df[
    (filtered_df["Quantity"] >= quantity_range[0]) & 
    (filtered_df["Quantity"] <= quantity_range[1]) &
    (filtered_df["Price"] >= price_range[0]) & 
    (filtered_df["Price"] <= price_range[1])
]

# 📋 Display Filtered Data
st.subheader("📊 Filtered Inventory Data")
st.dataframe(
    filtered_df,
    use_container_width=True,
    height=600,
    hide_index=True
)

st.success(f"✅ Showing {len(filtered_df)} matching records")
