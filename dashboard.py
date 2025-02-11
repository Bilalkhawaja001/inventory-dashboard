import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
import requests  # ✅ HTTP request karne ke liye
from io import BytesIO  # ✅ Excel ko memory mein load karne ke liye

# ✅ Correct File Paths
logo_path = "C:/Bilal/LOGO.PNG"  # Ensure this file exists
file_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"
sheet_name = "Inventory"

# 🔥 Load Excel File
try:
    response = requests.get(file_url)
    response.raise_for_status()  # ✅ Agar koi error ho toh raise karega
    file_bytes = BytesIO(response.content)  # ✅ File ko memory mein store karna

    df = pd.read_excel(file_bytes, sheet_name=sheet_name)  # ✅ Pandas se read karna

except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()  # ✅ Agar file load na ho toh app stop karo

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

# ✅ Convert Image to Base64 for Correct Display
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

if os.path.exists(logo_path):
    logo_base64 = get_base64_image(logo_path)
else:
    st.warning("⚠️ Logo file not found. Please check the path.")
    logo_base64 = ""

# 🎨 Apply CSS for Perfect Alignment
st.markdown(
    f"""
    <style>
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        position: relative;
        top: 10px;
        left: 10px;
        background: white;
        padding: 10px 15px;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        width: auto;
        max-width: 400px;
    }}
    .header-container img {{
        width: 48px;
        height: 48px;
        display: inline-block;
    }}
    .header-container div {{
        margin-left: 10px;
        display: inline-block;
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
        margin-top: 80px;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(to right, #4A90E2, #50E3C2);
     
