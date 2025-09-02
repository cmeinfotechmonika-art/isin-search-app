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
        # Try fetching the file from Google Drive
        response = requests.get(drive_url, timeout=10)
        response.raise_for_status()  # Raise error if failed
        return pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        st.error(f"⚠️ Could not fetch data online. Reason: {e}")
        return None

df = load_data()

# If online file not available, let user upload manually
if df is None:
    uploaded_file = st.file_uploader("Upload the CSV file manually:", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

if df is not None:
    # Input box for ISIN
    isin_to_search = st.text_input("Enter ISIN to search:")

    if st.button("Search"):
        filtered_df = df[df['ISIN'] == isin_to_search]

        if filtered_df.empty:
            st.warning(f"No data found for ISIN {isin_to_search}")
        else:
            st.success(f"Data found for ISIN {isin_to_search}")
            st.dataframe(filtered_df)  # Show table on page

            # Option to download as CSV
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






