import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image

# ✅ Correct File Paths
excel_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"
logo_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Logo.jpeg"  # Correct URL if needed
sheet_name = "Inventory"

# 🔥 Load Excel File from GitHub
try:
    response = requests.get(excel_url)
    response.raise_for_status()
    file_bytes = BytesIO(response.content)
    df = pd.read_excel(file_bytes, sheet_name=sheet_name)
except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()

# ✅ Ensure Required Columns Exist & Fill NaN Values
required_columns = ["Date", "Item Description", "Category", "Quantity", "UOM", "Price", "Vendor"]
for col in required_columns:
    if col not in df.columns:
        st.error(f"❌ Missing required column: {col}")
        st.stop()

df.fillna({"Quantity": 0, "Price": 0, "Category": "Unknown", "Vendor": "Unknown", "UOM": "N/A"}, inplace=True)
df["Quantity"] = df["Quantity"].fillna(0).astype(int)
df["Price"] = df["Price"].fillna(0).astype(int)

# ✅ FIX PRICE & QUANTITY RANGE
quantity_min, quantity_max = 0, 1000  # 🔥 Fixed max Quantity to 1000
price_min, price_max = 1000, 100000  # 🔥 Fixed Price Range to 1000 - 100000

# 🎨 Apply CSS for UI Styling (Small Logo)
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: flex-start; margin-bottom: 20px;">
        <img src="{logo_url}" width="48" height="48" style="margin-right: 10px;">
        <div>
            <h2 style="margin: 0; font-size: 20px; color: #333;">Centralized Mess</h2>
            <h4 style="margin: 0; font-size: 14px; color: #666;">Liberty Eco Campus Nooriabad</h4>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# 🎯 Sidebar Filters
st.sidebar.header("🔍 **Filters**")

# Date Filter (handle potential errors and NaT)
try:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime, handle errors
    df.dropna(subset=['Date'], inplace=True)  # Remove rows with NaT dates
    if not df['Date'].empty:
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        date_filter = st.sidebar.date_input("Select Date", value=min_date)  # Initialize with min_date
    else:
        st.warning("⚠️ No valid dates available for filtering.")
        date_filter = None
except (TypeError, ValueError):
    st.warning("⚠️ Could not convert 'Date' column to datetime. Filter will not work correctly.")
    date_filter = None


item_filter = st.sidebar.text_input("Search Item Description")

category_options = df["Category"].dropna().unique().tolist()
uom_options = df["UOM"].dropna().unique().tolist()
vendor_options = df["Vendor"].dropna().unique().tolist()

category_filter = st.sidebar.multiselect("Select Category", category_options)
quantity_filter = st.sidebar.slider("Select Quantity Range", min_value=quantity_min, max_value=quantity_max, value=(quantity_min, quantity_max))
uom_filter = st.sidebar.multiselect("Select UOM", uom_options)
price_filter = st.sidebar.slider("Select Price Range", min_value=price_min, max_value=price_max, value=(price_min, price_max))
vendor_filter = st.sidebar.multiselect("Select Vendor", vendor_options)

# Apply Filters
filtered_df = df.copy()

if date_filter:
    filtered_df = filtered_df[filtered_df['Date'] == date_filter]  # Exact date match

if item_filter:
    filtered_df = filtered_df[filtered_df["Item Description"].str.contains(item_filter, case=False, na=False)]

if category_filter:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]
if quantity_filter:
    filtered_df = filtered_df[(filtered_df["Quantity"] >= quantity_filter[0]) & (filtered_df["Quantity"] <= quantity_filter[1])]
if uom_filter:
    filtered_df = filtered_df[filtered_df["UOM"].isin(uom_filter)]
if price_filter:
    filtered_df = filtered_df[(filtered_df["Price"] >= price_filter[0]) & (filtered_df["Price"] <= price_filter[1])]
if vendor_filter:
    filtered_df = filtered_df[filtered_df["Vendor"].isin(vendor_filter)]



# 📋 Data Table
st.subheader("<h3><b>Inventory Management System</b></h3>") # Title Added and formatted
st.dataframe(filtered_df)

st.write("🔄 **Use Filters to Update Data!**")
