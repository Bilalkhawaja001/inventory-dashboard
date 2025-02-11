import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
import requests  
from io import BytesIO  

# ✅ Correct File Paths
logo_path = "C:/Bilal/LOGO.PNG"  
file_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"  # 👈 Apni file ka sahi link yahan daalo!

# 🔥 Load Excel File from GitHub
try:
    response = requests.get(file_url)
    response.raise_for_status()  
    file_bytes = BytesIO(response.content)  

    df = pd.read_excel(file_bytes, sheet_name="Inventory")  # 👈 Sheet ka naam confirm karo!

except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()  

st.dataframe(df)  # ✅ Check karo data aa raha hai ya nahi
