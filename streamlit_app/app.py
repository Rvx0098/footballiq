import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="FootballIQ Elite",
    page_icon="⚽",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/players_data-2025_2026.csv")

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right,#050816,#0b1120);
    color: white;
}

/* REMOVE STREAMLIT DEFAULT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    max-width: 100%;
}

/* HERO */
.hero-container {
    background: linear-gradient(135deg, rgba(0,245,255,0.08), rgba(0,0,0,0.2));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 40px;
    backdrop-filter: blur(20px);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 70px;
    font-weight: 800;
    color: white;
    line-height: 1;
}

.hero-subtitle {
    font-size: 20px;
    color: #94a3b8;
}

/* KPI CARDS */

.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 24px;
    backdrop-filter: blur(12px);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 25px rgba(0,245,255,0.2);
}

.metric-title {
    color: #94a3b8;
    font-size: 14px;
}

.metric-value {
    color: white;
    font-size: 42px;
    font-weight: 700;
}

/* SECTION */
.section-card {
    background: rgba(255,255,255,0.03);
    border-radius: 24px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    margin-bottom: 25px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: white;
    margin-bottom: 20px;
}

/* TABLES */

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚽ FootballIQ")
st.sidebar.caption("Elite Intelligence Platform")

teams = st.sidebar.multiselect(
    "Select Teams",
    df["Squad"].dropna().unique(),
    default=df["Squad"].dropna().unique()[:5]
)

filtered_df = df[df["Squad"].isin(teams)]

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero-container">
    <div class="hero-title">FootballIQ</div>
    <div class="hero-subtitle">
        Premium AI Powered Football Analytics Platform
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI ROW
# =========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL GOALS</div>
        <div class="metric-value">{int(filtered_df['Gls'].sum())}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TOTAL ASSISTS</div>
        <div class="metric-value">{int(filtered_df['Ast'].sum())}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">PLAYERS</div>
        <div class="metric-value">{len(filtered_df)}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TEAMS</div>
        <div class="metric-value">{filtered_df['Squad'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================
# TOP SCORERS
# =========================

st.markdown("""
<div class="section-card">
<div class="section-title">🏆 Top Goal Scorers</div>
</div>
""", unsafe_allow_html=True)

top_scorers = filtered_df.sort_values(
    by="Gls",
    ascending=False
).head(10)

fig = px.bar(
    top_scorers,
    x="Player",
    y="Gls",
    color="Squad",
    template="plotly_dark",
    height=500
)

fig.update_layout(
    paper_bgcolor="#0b1120",
    plot_bgcolor="#0b1120",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# ASSIST LEADERS
# =========================

st.markdown("""
<div class="section-card">
<div class="section-title">🎯 Assist Leaders</div>
</div>
""", unsafe_allow_html=True)

assist_df = filtered_df.sort_values(
    by="Ast",
    ascending=False
).head(10)

assist_fig = px.bar(
    assist_df,
    x="Player",
    y="Ast",
    color="Squad",
    template="plotly_dark",
    height=500
)

assist_fig.update_layout(
    paper_bgcolor="#0b1120",
    plot_bgcolor="#0b1120",
    font_color="white"
)

st.plotly_chart(assist_fig, use_container_width=True)

# =========================
# PLAYER SEARCH
# =========================

st.markdown("""
<div class="section-card">
<div class="section-title">🔍 Player Intelligence</div>
</div>
""", unsafe_allow_html=True)

player = st.selectbox(
    "Search Player",
    filtered_df["Player"].dropna().unique()
)

player_df = filtered_df[
    filtered_df["Player"] == player
]

st.dataframe(player_df)

# =========================
# RADAR CHART
# =========================

st.markdown("""
<div class="section-card">
<div class="section-title">📊 Radar Analytics</div>
</div>
""", unsafe_allow_html=True)

if not player_df.empty:

    values = [
        player_df["Gls"].values[0],
        player_df["Ast"].values[0],
        player_df["PK"].values[0] if "PK" in player_df.columns else 0
    ]

    categories = ["Goals", "Assists", "Penalties"]

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=player
    ))

    radar.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        font_color="white",
        height=500
    )

    st.plotly_chart(radar, use_container_width=True)

# =========================
# AI PREDICTIONS
# =========================

st.markdown("""
<div class="section-card">
<div class="section-title">🤖 AI Prediction Engine</div>
</div>
""", unsafe_allow_html=True)

ml_df = filtered_df[["Age", "Ast", "Gls"]].dropna()

ml_df["ElitePlayer"] = (
    ml_df["Gls"] > ml_df["Gls"].median()
).astype(int)

X = ml_df[["Age", "Ast"]]
y = ml_df["ElitePlayer"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

st.metric(
    "AI Accuracy",
    f"{accuracy * 100:.2f}%"
)

age = st.slider("Player Age", 16, 40, 22)
assists = st.slider("Player Assists", 0, 20, 5)

prediction = model.predict([[age, assists]])

if prediction[0] == 1:
    st.success("🌟 Elite Player Predicted")
else:
    st.warning("⚠️ Average Performance Prediction")

# =========================
# HEATMAP
# =========================

st.markdown("""
<div class="section-card">
<div class="section-title">🔥 Tactical Heatmap</div>
</div>
""", unsafe_allow_html=True)

heatmap = filtered_df.groupby("Squad")[["Gls","Ast"]].mean()

heat_fig = px.imshow(
    heatmap,
    text_auto=True,
    template="plotly_dark",
    color_continuous_scale="Blues"
)

heat_fig.update_layout(
    paper_bgcolor="#0b1120",
    font_color="white"
)

st.plotly_chart(heat_fig, use_container_width=True)

# =========================
# RAW DATA
# =========================

st.markdown("""
<div class="section-card">
<div class="section-title">📁 Raw Dataset</div>
</div>
""", unsafe_allow_html=True)

st.dataframe(filtered_df.head(50))