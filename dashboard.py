import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import base64

# ✅ Load Logo (Optional)
logo_path = "C:/Bilal/LOGO.PNG"  # Ensure this file exists

# ✅ Corrected File Path from GitHub
file_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"

# 🔥 Load Excel File
try:
    response = requests.get(file_url)
    response.raise_for_status()
    file_bytes = BytesIO(response.content)
    df = pd.read_excel(file_bytes, sheet_name="Inventory")
except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()

# ✅ Ensure Required Columns Exist & Handle Missing Values
required_columns = ["Date", "Item Description", "Category", "Quantity", "UOM", "Price", "Vendor"]
for col in required_columns:
    if col not in df.columns:
        st.error(f"❌ Missing required column: {col}")
        st.stop()

df.fillna({"Quantity": 0, "Price": 0, "Category": "Unknown", "Vendor": "Unknown", "UOM": "N/A"}, inplace=True)
df["Quantity"] = df["Quantity"].astype(int)
df["Price"] = df["Price"].astype(int)

# ✅ Set Quantity & Price Range
quantity_min, quantity_max = 0, 1000
price_min, price_max = 1000, 100000

# ✅ Convert Image to Base64 for Display
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""

logo_base64 = get_base64_image(logo_path)

# 🎨 Apply CSS Styling
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
    }}
    .header-container img {{
        width: 48px;
        height: 48px;
        margin-right: 10px;
    }}
    .inventory-box {{
        text-align: center;
        font-size: 50px;
        font-weight: bold;
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

# 🎯 Large Centered `Inventory Management` Title
st.markdown("<div class='inventory-box'>INVENTORY MANAGEMENT</div>", unsafe_allow_html=True)

# 🔍 Sidebar Filters
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

# 📋 Display Data Table
st.subheader("📋 Inventory Data")
st.dataframe(df)

st.write("🔄 **Use Filters to Update Data!**")
