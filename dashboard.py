import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image
import base64

# ✅ Correct File Paths
excel_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"
logo_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Logo.jpeg"
sheet_name = "Inventory"

# 🔥 Load Logo from GitHub and Resize
try:
    response = requests.get(logo_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    new_size = (48, 48)  # 48px x 48px
    resized_image = image.resize(new_size)
    st.image(resized_image, caption="Centralized Mess\nLiberty Eco Campus Nooriabad", use_column_width=False) # use_column_width=False
except Exception as e:
    st.warning(f"⚠️ Logo file not found. Please check the path. Error: {e}")

# 🔥 Load Excel File from GitHub
try:
    response = requests.get(excel_url)
    response.raise_for_status()
    file_bytes = BytesIO(response.content)
    df = pd.read_excel(file_bytes, sheet_name=sheet_name)
except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()

# ... (rest of your code remains the same)

# 🎨 Apply CSS for UI Styling (Modified)
st.markdown(
    """
    <style>
    .inventory-box {
        text-align: center;
        font-size: 30px; /* Reduced font size */
        font-weight: bold;
        margin-top: 20px;
        padding: 10px; /* Reduced padding */
        border-radius: 10px;
        background: linear-gradient(to right, #4A90E2, #50E3C2);
        color: white;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        width: 100%;
    }
    </style>
    <div class="inventory-box">INVENTORY MANAGEMENT</div>
    """,
    unsafe_allow_html=True
)


# ... (rest of your code remains the same)
