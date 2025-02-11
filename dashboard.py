import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image

# ... (rest of your imports and file paths)

try:
    df = pd.read_excel(file_bytes, sheet_name=sheet_name)
    st.write("## Raw Data (Immediately After Loading):")  # Show immediately
    st.dataframe(df)
    st.write("## Raw Data Types (Immediately After Loading):")
    st.write(df.dtypes)
except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()

# ... (rest of the code for required columns, fillna, price/quantity ranges, logo, sidebar)

try:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    st.write("## Data After Conversion:")
    st.dataframe(df)
    st.write("## Data Types After Conversion:")
    st.write(df.dtypes)
    st.write("## Number of NaT Values:")
    st.write(df['Date'].isnull().sum())

    if df['Date'].isnull().any():
        st.warning(f"⚠️ Some dates could not be parsed.  Number of invalid dates: {df['Date'].isnull().sum()}.  Please check the 'Date' column in your Excel file.")
        st.dataframe(df[df['Date'].isnull()])  # Show rows with NaT values
        df.dropna(subset=['Date'], inplace=True)  # Or replace NaT with a default date
        if df['Date'].empty:
            st.warning("⚠️ No valid dates remain after handling invalid date values.")
            date_filter = None
        else:
            min_date = df['Date'].min()
            max_date = df['Date'].max()
            date_filter = st.sidebar.date_input("Select Date", value=min_date)
    else:
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        date_filter = st.sidebar.date_input("Select Date", value=min_date)

except (TypeError, ValueError) as e:
    st.error(f"⚠️ Error during date conversion: {e}.  Please check the 'Date' column in your Excel file for formatting issues.")
    date_filter = None

# ... (rest of your code for filtering, data table, etc.)
