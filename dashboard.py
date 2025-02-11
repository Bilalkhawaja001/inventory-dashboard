import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import base64
from io import BytesIO

# ✅ GitHub File Paths
logo_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/LOGO.PNG"
file_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"
sheet_name = "Inventory"

# ✅ Load Logo from GitHub
try:
    response = requests.get(logo_url)
    response.raise_for_status()
    logo_base64 = base64.b64encode(response.content).decode()
except Exception as e:
    st.warning(f"⚠️ Logo file not found. Please check the path. Error: {e}")
    logo_base64 = ""

# ✅ Load Excel File from GitHub
try:
    response = requests.get(file_url)
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
quantity_min, quantity_max = 0, 1000
price_min, price_max = 1000, 100000

# ✅ Apply CSS for Styling
st.markdown(
    f"""
    <style>
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background: white;
        padding: 10px 15px;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        width: auto;
        max-width: 400px;
    }}
    .header-container img {{
        width: 48px;
        height: 48px;
    }}
    .header-container div {{
        margin-left: 10px;
    }}
    .header-container h1 {{
        font-size: 24px;
        margin: 0;
        font-weight: bold;
        color: black;
    }}
    .header-container h3 {{
        font-size: 14px;
        margin: 0;
        font-weight: normal;
        color: black;
    }}
    .inventory-box {{
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        margin-top: 40px;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(to right, #4A90E2, #50E3C2);
        color: white;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }}
    </style>
    <div class="header-container">
        <img src="data:image/png;base64,{logo_base64}">
        <div>
            <h1>Centralized Mess</h1>
            <h3>Liberty Eco Campus Nooriabad</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 🎯 Add Inventory Management Title
st.markdown("<div class='inventory-box'>INVENTORY MANAGEMENT</div>", unsafe_allow_html=True)

# ✅ Sidebar Filters
st.sidebar.header("🔍 **Filters**")
date_filter = st.sidebar.date_input("Select Date")
item_filter = st.sidebar.text_input("Search Item Description")

category_options = df["Category"].dropna().unique().tolist()
uom_options = df["UOM"].dropna().unique().tolist()
vendor_options = df["Vendor"].dropna().unique().tolist()

category_filter = st.sidebar.multiselect("Select Category", category_options)
quantity_filter = st.sidebar.slider("Select Quantity Range", min_value=quantity_min, max_value=quantity_max, value=(quantity_min, quantity_max))
uom_filter = st.sidebar.multiselect("Select UOM", uom_options)
price_filter = st.sidebar.slider("Select Price Range", min_value=price_min, max_value=price_max, value=(price_min, price_max))
vendor_filter = st.sidebar.multiselect("Select Vendor", vendor_options)

# 📋 Data Table
st.subheader("📋 Inventory Data")
st.dataframe(df)

st.write("🔄 **Use Filters to Update Data!**")
