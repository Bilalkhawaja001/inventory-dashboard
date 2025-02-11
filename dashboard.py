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
    # Check for NaT *after* conversion
    if df['Date'].isnull().all():  # Check if *all* dates are NaT
        st.warning("⚠️ No valid dates available for filtering. Please check the 'Date' column in your Excel file.")
        date_filter = None  # Important: Set to None if no valid dates
    else:
        df.dropna(subset=['Date'], inplace=True)  # Remove rows with NaT dates ONLY if there are valid dates
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        date_filter = st.sidebar.date_input("Select Date", value=min_date)  # Initialize with min_date

except (TypeError, ValueError):
    st.warning("⚠️ Could not convert 'Date' column to datetime. Please check the 'Date' column in your Excel file for formatting issues.")  # More specific message
    date_filter = None

# ... (rest of the filter code: item_filter, category_filter, etc.)

# Apply Filters (Handle date_filter being None)
filtered_df = df.copy()

if date_filter is not None:  # Check if date_filter has a value
    filtered_df = filtered_df[filtered_df['Date'] == date_filter]  # Exact date match

# ... (rest of the filtering logic)

# 📋 Data Table
st.markdown("<h3><b>Inventory Management System</b></h3>", unsafe_allow_html=True)  # Correct title display
st.dataframe(filtered_df)

st.write("🔄 **Use Filters to Update Data!**")
