# streamlit.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime
import pytz

# ----------------------
# Page Config & Styling
# ----------------------
st.set_page_config(
    page_title="Irish Rail Analytics",
    page_icon="🚂",
    layout="wide",
)

st.markdown("""
<style>
/* Global App Background + Text */
.stApp {
    background-color: #fafafa;
    color: #333 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Headings & Captions */
h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: #333 !important;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e0e0e0;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
div[data-testid="metric-container"] * {
    color: #333 !important;
}

/* Light theme for DataFrames */
[data-testid="stDataFrame"] {
    background-color: #fff !important;
    color: #333 !important;
    border-radius: 8px;
    border: 1px solid #ddd;
}
[data-testid="stDataFrame"] td, 
[data-testid="stDataFrame"] th {
    background-color: #fff !important;
    color: #333 !important;
}
[data-testid="stDataFrame"] div {
    color: #333 !important;
}

/* Buttons */
.stButton > button {
    border-radius: 6px;
    background-color: #fff;
    border: 1px solid #ddd;
    color: #333 !important;
}
.stButton > button:hover {
    background-color: #f2f2f2;
    color: #000 !important;
}

/* Folium Map iframe fix: prevent black box */
div.st-folium iframe {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------
# Database Connection
# ----------------------
@st.cache_resource
def get_engine():
    try:
        secrets = st.secrets["connections"]["postgresql"]
        return create_engine(
            f"postgresql+psycopg2://{secrets['username']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['database']}"
        )
    except KeyError:
        db = st.secrets["database"]
        return create_engine(
            f"postgresql+psycopg2://{db['DB_USER']}:{db['DB_PASSWORD']}@{db['DB_HOST']}:{db['DB_PORT']}/{db['DB_NAME']}"
        )

def run_query(query: str) -> pd.DataFrame:
    try:
        engine = get_engine()
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()

# ----------------------
# Data Fetching
# ----------------------
@st.cache_data(ttl=60)
def get_kpis():
    return run_query("""
    SELECT
        ROUND(AVG(CASE WHEN "delay_minutes" <= 5 THEN 1 ELSE 0 END) * 100, 1) AS on_time_pct,
        ROUND(AVG("delay_minutes"::numeric), 1) AS avg_delay,
        COUNT(*) AS total_trains,
        SUM(CASE WHEN "TrainStatus" = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
        MAX("enhanced_at") AS last_update,
        COUNT(*) FILTER (WHERE "delay_minutes" > 30) AS severely_delayed,
        ROUND(AVG(CASE WHEN "delay_minutes" > 0 THEN "delay_minutes" END), 1) AS avg_delay_when_delayed
    FROM "current_trains"
    WHERE "TrainDate" = CURRENT_DATE;
    """)

@st.cache_data(ttl=60)
def get_live_trains():
    return run_query("""
    SELECT 
        ct."TrainCode", ct."Direction", ct."TrainStatus",
        ct."TrainLatitude", ct."TrainLongitude", ct."delay_minutes",
        ct."current_location", ct."train_type", ct."PublicMessage",
        tm."TrainOrigin", tm."TrainDestination"
    FROM "current_trains" ct
    LEFT JOIN (
        SELECT DISTINCT ON ("TrainCode", "TrainDate") "TrainCode", "TrainDate", "TrainOrigin", "TrainDestination"
        FROM "train_movements"
        ORDER BY "TrainCode", "TrainDate", "LocationOrder"
    ) tm ON ct."TrainCode" = tm."TrainCode" AND ct."TrainDate" = tm."TrainDate"
    WHERE ct."TrainDate" = CURRENT_DATE
    AND ct."TrainLatitude" IS NOT NULL AND ct."TrainLongitude" IS NOT NULL
    ORDER BY ct."enhanced_at" DESC;
    """)

@st.cache_data(ttl=300)
def get_stations():
    return run_query("""
    SELECT "StationDesc","StationCode","StationType","StationLatitude","StationLongitude"
    FROM "stations"
    WHERE "StationLatitude" IS NOT NULL AND "StationLongitude" IS NOT NULL
    ORDER BY "StationType", "StationDesc";
    """)

@st.cache_data(ttl=300)
def get_delay_distribution():
    return run_query("""
    SELECT delay_category, COUNT(*) as count FROM (
        SELECT CASE 
            WHEN COALESCE("delay_minutes", 0) <= 5 THEN 'On Time'
            WHEN "delay_minutes" <= 15 THEN 'Minor Delay'
            WHEN "delay_minutes" <= 30 THEN 'Major Delay'
            ELSE 'Severe Delay' END as delay_category
        FROM "current_trains"
        WHERE "TrainDate" = CURRENT_DATE
    ) categorized
    GROUP BY delay_category
    ORDER BY CASE delay_category
        WHEN 'On Time' THEN 1 WHEN 'Minor Delay' THEN 2
        WHEN 'Major Delay' THEN 3 WHEN 'Severe Delay' THEN 4 END;
    """)

# ----------------------
# Header
# ----------------------
st.title("🚂 Irish Rail Analytics")
st.caption("Real-time train performance and network insights for Ireland")

# ----------------------
# Force Refresh Button
# ----------------------
if st.button("🔄 Force Refresh"):
    st.cache_data.clear()
    st.rerun()

# ----------------------
# KPIs
# ----------------------
kpi_df = get_kpis()
tz = pytz.timezone("Europe/Dublin")

if not kpi_df.empty:
    kpis = kpi_df.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("On-Time %", f"{kpis['on_time_pct']:.1f}%")
    col2.metric("Avg Delay", f"{kpis['avg_delay']:.1f} min")
    col3.metric("Total Trains", f"{kpis['total_trains']:,}")
    col4.metric("Cancelled", f"{kpis['cancelled']:,}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Severely Delayed", f"{kpis['severely_delayed']:,}")
    col6.metric("Avg Delay (Delayed Only)", f"{kpis['avg_delay_when_delayed'] or 0:.1f} min")

    if kpis['last_update']:
        db_update_utc = pd.to_datetime(kpis['last_update']).tz_localize("UTC")
        db_update_local = db_update_utc.tz_convert(tz)
        col7.metric("Last Update (UTC)", db_update_utc.strftime('%H:%M'))
        col8.metric("Last Update (GMT)", db_update_local.strftime('%H:%M'))
    else:
        col7.metric("Last Update (UTC)", "N/A")
        col8.metric("Last Update (GMT", "N/A")
else:
    st.warning("No KPI data available.")

# ----------------------
# Live Map
# ----------------------
st.subheader("📍 Live Train Positions")
col_map, col_info = st.columns([3, 1])
stations_df, trains_df = get_stations(), get_live_trains()

with col_map:
    m = folium.Map(location=[53.35, -6.26], zoom_start=7, tiles="CartoDB positron")

    for _, s in stations_df.iterrows():
        folium.CircleMarker(
            [s['StationLatitude'], s['StationLongitude']],
            radius=6, popup=s['StationDesc'],
            color="#2E86C1", fillColor="#2E86C1", fillOpacity=0.6
        ).add_to(m)

    for _, t in trains_df.iterrows():
        delay = t.get('delay_minutes', 0) or 0
        color = 'green' if delay <= 5 else 'orange' if delay <= 15 else 'red'
        folium.Marker(
            [t['TrainLatitude'], t['TrainLongitude']],
            popup=f"<b>{t['TrainCode']}</b><br>{t.get('TrainOrigin','?')} → {t.get('TrainDestination','?')}<br>Delay: {delay} min",
            icon=folium.Icon(color=color, icon="train", prefix="fa")
        ).add_to(m)

    st_folium(m, height=600, width="100%", returned_objects=[])

with col_info:
    st.metric("Stations", len(stations_df))
    st.metric("Live Trains", len(trains_df))
    st.markdown("""
    **Legend**  
    🟢 ≤5 min | 🟠 6–15 min | 🔴 >15 min
    """)

# ----------------------
# Delay Distribution
# ----------------------
st.subheader("📊 Delay Distribution")
dist = get_delay_distribution()
if not dist.empty:
    fig = px.pie(
        dist,
        names="delay_category",
        values="count",
        hole=0.4,
        color="delay_category",
        color_discrete_map={
            "On Time":"#28a745",
            "Minor Delay":"#ffc107",
            "Major Delay":"#fd7e14",
            "Severe Delay":"#dc3545"
        },
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Current Trains Table
# ----------------------
st.subheader("🚆 Current Trains")
trains_df = get_live_trains()
if not trains_df.empty:
    trains_df['delay_minutes'] = trains_df['delay_minutes'].fillna(0)

    def punctuality(delay):
        if delay <= 5: return 'On Time'
        elif delay <= 15: return 'Minor Delay'
        elif delay <= 30: return 'Major Delay'
        else: return 'Severe Delay'

    trains_df['Punctuality'] = trains_df['delay_minutes'].apply(punctuality)

    display_df = trains_df[['TrainCode','TrainOrigin','TrainDestination','TrainStatus','delay_minutes','train_type','Punctuality']]
    display_df = display_df.rename(columns={
        'TrainCode':'Train','TrainOrigin':'From','TrainDestination':'To',
        'TrainStatus':'Status','delay_minutes':'Delay (min)','train_type':'Type'
    })

    color_map = {
        'On Time': '#28a745','Minor Delay': '#ffc107',
        'Major Delay': '#fd7e14','Severe Delay': '#dc3545'
    }
    def color_punctuality(val): return f'color: {color_map.get(val, "#333")}'

    st.dataframe(
        display_df.fillna("Unknown").style.applymap(color_punctuality, subset=['Punctuality']),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No live train data available.")

# ----------------------
# Footer
# ----------------------
st.markdown(f"---\n*Last refreshed (local): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

# ----------------------
# Data Limitations
# ----------------------
with st.expander("⚠️ Data Limitations"):
    st.markdown("""
    Irish Rail realtime data comes with several important caveats:

    - Times are estimates; trains can recover delays.
    - Coverage weaker on: Athlone–Westport, Cork, Mallow–Tralee, Limerick lines, Rosslare, Dundalk–Belfast.
    - API only returns near-term trains (next 5–90 mins).
    - Some origin/terminating stations show `00:00`.
    - Provided as-is; no guarantees of accuracy or uptime.
    """)
