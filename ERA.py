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
# CSS
# =================================================
st.markdown("""
<style>
.main { background: linear-gradient(to right, #141E30, #243B55); }
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
}
.blue { background: linear-gradient(135deg,#396afc,#2948ff); }
.green { background: linear-gradient(135deg,#11998e,#38ef7d); }
.orange { background: linear-gradient(135deg,#f7971e,#ffd200); }
.red { background: linear-gradient(135deg,#ff416c,#ff4b2b); }
.purple { background: linear-gradient(135deg,#667eea,#764ba2); }
</style>
""", unsafe_allow_html=True)

# =================================================
# LOAD DATA (ROBUST)
# =================================================
def load_data(file):
    if file is not None:
        if file.name.endswith(".xlsx"):
            return pd.read_excel(file)
        else:
            return pd.read_csv(file)

    # fallback if file exists in repo
    if os.path.exists("social_media_engagement_enhanced.csv.xlsx"):
        return pd.read_excel("social_media_engagement_enhanced.csv.xlsx")

    return None

# =================================================
# FILE UPLOADER
# =================================================
st.sidebar.header("📁 Upload Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

df = load_data(uploaded_file)

if df is None:
    st.error("❌ Please upload the dataset to continue.")
    st.stop()

# =================================================
# DATA PREP
# =================================================
df["date"] = pd.to_datetime(df["date"])
df["revenue_generated"] = df["ad_spend"] * (1 + df["roi"])

# =================================================
# FILTERS
# =================================================
st.sidebar.header("🎛 Filters")

platform = st.sidebar.multiselect(
    "Platform", df["platform"].unique(), df["platform"].unique()
)

content = st.sidebar.multiselect(
    "Content Type", df["content_type"].unique(), df["content_type"].unique()
)

year = st.sidebar.multiselect(
    "Year", df["year"].unique(), df["year"].unique()
)

filtered_df = df[
    (df["platform"].isin(platform)) &
    (df["content_type"].isin(content)) &
    (df["year"].isin(year))
]

# =================================================
# HEADER
# =================================================
st.markdown("""
<h1 class="gradient-text" style="text-align:center;">
🚀 Social Media Analytics Pro Dashboard
</h1>
""", unsafe_allow_html=True)

# =================================================
# KPI CARDS
# =================================================
c1, c2, c3, c4, c5 = st.columns(5)

c1.markdown(f"<div class='metric-card blue'><h3>Engagement</h3><h2>{int(filtered_df.engagement.sum())}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card green'><h3>Eng Rate</h3><h2>{filtered_df.engagement_rate.mean():.2f}%</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card orange'><h3>Ad Spend</h3><h2>₹{int(filtered_df.ad_spend.sum())}</h2></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card red'><h3>Revenue</h3><h2>₹{int(filtered_df.revenue_generated.sum())}</h2></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='metric-card purple'><h3>ROI</h3><h2>{filtered_df.roi.mean():.2f}</h2></div>", unsafe_allow_html=True)

# =================================================
# CHARTS
# =================================================
st.bar_chart(filtered_df.groupby("platform")["engagement_rate"].mean())
st.line_chart(filtered_df.groupby("post_hour")["engagement"].mean())

# =================================================
# DOWNLOAD
# =================================================
st.download_button(
    "⬇️ Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_social_media_data.csv",
    "text/csv"
)

st.markdown("<hr><center>© 2025 Social Media Analytics Pro</center>", unsafe_allow_html=True)
