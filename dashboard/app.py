import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from streamlit_autorefresh import st_autorefresh


# Database connection setup
DB_HOST = "localhost"
DB_NAME = "uberdb"
DB_USER = "user"
DB_PASS = "password"
DB_PORT = "5432"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Streamlit config
st.set_page_config(page_title="Uber Real-Time Dashboard", layout="wide")
st.title("🚖 Uber Real-Time Rides Dashboard")

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="data_refresh")

# Function to fetch recent rides
@st.cache_data(ttl=5)
def load_data():
    query = """
    SELECT * FROM rides
    ORDER BY pickup_datetime DESC
    LIMIT 3000;
    """
    return pd.read_sql(query, engine)

# Load and display data
df = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("Total Rides", len(df))
col2.metric("Total Passengers", df["passenger_count"].sum())
col3.metric("Latest Timestamp", str(df["pickup_datetime"].max())[:19])

st.markdown("### Ride Density Map (last 1000 points)")
st.map(df[["latitude", "longitude"]].dropna())

st.caption("🔄 Dashboard refreshes automatically every 5 seconds.")
