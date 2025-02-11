import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# ✅ Correct File Paths
excel_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Fixed_Inventory_Management.xlsx"
logo_url = "https://raw.githubusercontent.com/Bilalkhawaja001/inventory-dashboard/main/Logo.jpeg"
sheet_name = "Inventory"

try:
    response = requests.get(logo_url)
    response.raise_for_status()  # Check for successful response
    image = Image.open(BytesIO(response.content))
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

except requests.exceptions.RequestException as e:
    st.error(f"❌ Error downloading logo: {e}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error opening logo: {e}")
    st.stop()



try:
    response = requests.get(excel_url)
    response.raise_for_status()  # Check for successful response
    file_bytes = BytesIO(response.content)  # Define file_bytes HERE

    df = pd.read_excel(file_bytes, sheet_name=sheet_name)

    st.write("## 1. Raw Data (Immediately After Loading):")
    st.dataframe(df)
    st.write("## 2. Raw Data Types (Immediately After Loading):")
    st.write(df.dtypes)

    # Convert to datetime, with VERY detailed error handling
    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', infer_datetime_format=True)

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
        st.error(f"## 7. Error during date conversion: {e}")
        st.write("## 8. Sample of 'Date' column (for debugging):")
        st.dataframe(df['Date'].head(10))
        date_filter = None  # Set date_filter to None in case of error

except requests.exceptions.RequestException as e:  # Handle URL errors
    st.error(f"❌ Error downloading Excel file: {e}")
    st.stop()
except Exception as e:  # Handle other Excel reading errors
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()


# 🎯 Sidebar Filters
st.sidebar.header("🔍 **Filters**")
# ... (rest of your sidebar filter code: item_filter, category_filter, etc.)

# Apply Filters (Handle date_filter being None)
filtered_df = df.copy()

if date_filter:  # Only the date filter is active
    filtered_df = filtered_df[filtered_df['Date'] == date_filter]

# ... (Apply other filters similarly)

st.dataframe(filtered_df)  # Show the filtered data
