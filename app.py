import streamlit as st
import pandas as pd
import requests
import io

st.title("ISIN Data Search Tool")

# Google Drive direct download link
drive_url = "https://drive.google.com/uc?export=download&id=1NyGPHMIjeO_DsDds9mip0dtDH6s4gpjm"

@st.cache_data
def load_data():
    try:
        response = requests.get(drive_url, timeout=10)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        st.error(f"⚠️ Could not fetch data online. Reason: {e}")
        return None

df = load_data()

# Allow manual upload if not loaded
if df is None:
    uploaded_file = st.file_uploader("Upload the CSV file manually:", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

if df is not None:
    # Convert Trade column to datetime
    df["Trade"] = pd.to_datetime(df["Trade"], dayfirst=True, errors="coerce")

    # Input for ISIN
    isin_to_search = st.text_input("Enter ISIN to search:")

    # Date filter
    min_date = df["Trade"].min()
    max_date = df["Trade"].max()
    date_range = st.date_input(
        "Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if st.button("Search"):
        # Filter by ISIN
        filtered_df = df[df['ISIN'] == isin_to_search]

        # Filter by date range
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df["Trade"] >= pd.to_datetime(start_date)) &
                (filtered_df["Trade"] <= pd.to_datetime(end_date))
            ]

        # Show results
        if filtered_df.empty:
            st.warning(f"No data found for ISIN {isin_to_search} in selected date range")
        else:
            st.success(f"Data found for ISIN {isin_to_search}")
            st.dataframe(filtered_df)

            # Download button
            output_file = f"filtered_{isin_to_search}.csv"
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv,
                file_name=output_file,
                mime="text/csv"
            )
else:
    st.warning("No data available. Please upload CSV file manually.")
