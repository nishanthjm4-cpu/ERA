import streamlit as st
import pandas as pd
import os

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Social Media Analytics Pro",
    page_icon="🚀",
    layout="wide"
)

# =================================================
# ADVANCED CSS + ANIMATIONS
# =================================================
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #141E30, #243B55);
}
.gradient-text {
    background: linear-gradient(90deg,#00c6ff,#0072ff,#7f00ff,#e100ff);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 6s infinite linear;
}
@keyframes gradientMove {
    0% { background-position: 0%; }
    100% { background-position: 300%; }
}
.metric-card {
    padding: 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-8px) scale(1.03);
}
.blue { background: linear-gradient(135deg,#396afc,#2948ff); }
.green { background: linear-gradient(135deg,#11998e,#38ef7d); }
.orange { background: linear-gradient(135deg,#f7971e,#ffd200); }
.red { background: linear-gradient(135deg,#ff416c,#ff4b2b); }
.purple { background: linear-gradient(135deg,#667eea,#764ba2); }
.progress-bar {
    height: 12px;
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg,#38ef7d,#11998e);
}
</style>
""", unsafe_allow_html=True)

# =================================================
# LOAD DATA (SAFE)
# =================================================
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    elif os.path.exists("social_media_engagement.csv"):
        df = pd.read_csv("social_media_engagement.csv")
    else:
        return None

    df["date"] = pd.to_datetime(df["date"])
    return df

# =================================================
# FILE UPLOADER
# =================================================
st.sidebar.markdown("## 📁 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload Social Media CSV",
    type=["csv"]
)

df = load_data(uploaded_file)

if df is None:
    st.warning("⚠️ Please upload the CSV file to continue.")
    st.stop()

# =================================================
# DERIVED METRICS
# =================================================
df["revenue_generated"] = df["ad_spend"] * (1 + df["roi"])

# =================================================
# SIDEBAR FILTERS
# =================================================
st.sidebar.markdown("## 🎛️ Dashboard Controls")

platform_filter = st.sidebar.multiselect(
    "📱 Platform", df["platform"].unique(), df["platform"].unique()
)

content_filter = st.sidebar.multiselect(
    "🖼️ Content Type", df["content_type"].unique(), df["content_type"].unique()
)

year_filter = st.sidebar.multiselect(
    "📅 Year", df["year"].unique(), df["year"].unique()
)

filtered_df = df[
    (df["platform"].isin(platform_filter)) &
    (df["content_type"].isin(content_filter)) &
    (df["year"].isin(year_filter))
]

# =================================================
# HEADER
# =================================================
st.markdown("""
<h1 class="gradient-text" style="text-align:center;">
🚀 Social Media Analytics Pro Dashboard
</h1>
<p style="text-align:center;color:#dcdcdc;font-size:18px;">
Engagement • Content • ROI • Revenue • Best Posting Time
</p>
""", unsafe_allow_html=True)

# =================================================
# KPI CARDS
# =================================================
c1, c2, c3, c4, c5 = st.columns(5)

c1.markdown(f"""
<div class="metric-card blue">
<h3>Total Engagement</h3>
<h2>{int(filtered_df["engagement"].sum())}</h2>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="metric-card green">
<h3>Avg Engagement Rate</h3>
<h2>{round(filtered_df["engagement_rate"].mean(),2)}%</h2>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="metric-card orange">
<h3>Ad Spend</h3>
<h2>₹ {int(filtered_df["ad_spend"].sum())}</h2>
</div>
""", unsafe_allow_html=True)

c4.markdown(f"""
<div class="metric-card red">
<h3>Revenue</h3>
<h2>₹ {int(filtered_df["revenue_generated"].sum())}</h2>
</div>
""", unsafe_allow_html=True)

c5.markdown(f"""
<div class="metric-card purple">
<h3>Avg ROI</h3>
<h2>{round(filtered_df["roi"].mean(),2)}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="progress-bar"></div>', unsafe_allow_html=True)

# =================================================
# TABS
# =================================================
tab1, tab2, tab3, tab4 = st.tabs(
    ["📱 Engagement", "🖼️ Content", "💰 ROI", "⏰ Best Time"]
)

with tab1:
    st.bar_chart(
        filtered_df.groupby("platform")["engagement_rate"].mean()
    )

with tab2:
    st.bar_chart(
        filtered_df.groupby("content_type")["engagement"].mean()
    )

with tab3:
    st.bar_chart(
        filtered_df.groupby("campaign_name")["roi"].mean()
    )

with tab4:
    st.line_chart(
        filtered_df.groupby("post_hour")["engagement"].mean()
    )

# =================================================
# DOWNLOAD
# =================================================
st.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_social_media_data.csv",
    "text/csv"
)

# =================================================
# FOOTER
# =================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray;'>© 2025 Social Media Analytics Pro</p>",
    unsafe_allow_html=True
)
