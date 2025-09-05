import streamlit as st
import pandas as pd
import mysql.connector
from datetime import date

st.title("📊 ISIN Data Search Tool (MySQL)")

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="cminfo@1234",
        database="isin_db"
    )

# ISIN input
isin_to_search = st.text_input("Enter ISIN to search:")

# Global date picker (not restricted to ISIN min/max)
start_date = st.date_input("Start Date", value=date(2000, 1, 1), min_value=date(2000, 1, 1), max_value=date(2025, 12, 31))
end_date = st.date_input("End Date", value=date.today(), min_value=date(2000, 1, 1), max_value=date(2025, 12, 31))

if st.button("🔍 Search"):
    try:
        conn = get_connection()
        query = """
            SELECT *
            FROM isin_data
            WHERE ISIN = %s AND Trade BETWEEN %s AND %s
        """
        df = pd.read_sql(query, conn, params=[isin_to_search, start_date, end_date])
        conn.close()

        if df.empty:
            st.warning(f"No data found for ISIN {isin_to_search} between {start_date} and {end_date}")
        else:
            st.success(f"✅ Found {len(df)} records")
            st.dataframe(df)

            # Download option
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv,
                file_name=f"{isin_to_search}_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Database error: {e}")
