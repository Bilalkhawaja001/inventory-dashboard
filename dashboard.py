import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# ... (rest of your imports and file paths)

try:
    df = pd.read_excel(file_bytes, sheet_name=sheet_name)

    st.write("## 1. Raw Data (Immediately After Loading):")
    st.dataframe(df)
    st.write("## 2. Raw Data Types (Immediately After Loading):")
    st.write(df.dtypes)

    # Convert to datetime, with VERY detailed error handling
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', infer_datetime_format=True)  # infer_datetime_format
        st.write("## 3. Data After Conversion:")
        st.dataframe(df)
        st.write("## 4. Data Types After Conversion:")
        st.write(df.dtypes)
        st.write("## 5. Number of NaT Values:")
        st.write(df['Date'].isnull().sum())

        # Show rows with NaT values (if any)
        if df['Date'].isnull().any():
            st.write("## 6. Rows with Invalid Dates (NaT):")
            st.dataframe(df[df['Date'].isnull()])

        # Check if ALL dates are NaT
        if df['Date'].isnull().all():
            st.warning("⚠️ ALL dates are invalid. Please check the 'Date' column in your Excel file.")
            date_filter = None
        else:
            df.dropna(subset=['Date'], inplace=True)  # Remove NaT rows AFTER inspection
            min_date = df['Date'].min()
            max_date = df['Date'].max()
            date_filter = st.sidebar.date_input("Select Date", value=min_date)

    except Exception as e:
        st.error(f"## 7. Error during date conversion: {e}")  # Catch ANY conversion error
        st.write("## 8. Sample of 'Date' column (for debugging):")  # Show a sample
        st.dataframe(df['Date'].head(10))  # Show first 10 values
        date_filter = None

except Exception as e:
    # ... (your file reading error handling)

# ... (rest of your code, but ONLY the date filter for now)

if date_filter:  # Only the date filter is active
    filtered_df = df[df['Date'] == date_filter]

st.dataframe(filtered_df)  # Show only the filtered data
