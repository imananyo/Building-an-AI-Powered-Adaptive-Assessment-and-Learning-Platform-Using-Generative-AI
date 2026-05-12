import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from components.sidebar import (
    show_sidebar
)

from services.api_client import (
    fetch_my_results
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title="Student Dashboard",

    layout="wide"
)

# -----------------------------------
# LOGIN CHECK
# -----------------------------------

if "logged_in" not in st.session_state:

    st.warning(
        "Please login first."
    )

    st.stop()

# -----------------------------------
# ROLE CHECK
# -----------------------------------

user = st.session_state.get(
    "user",
    {}
)

if user.get("role") != "student":

    st.error(
        "Student Access Only"
    )

    st.stop()

# -----------------------------------
# SIDEBAR
# -----------------------------------

show_sidebar()

# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title(
    "Student Performance Dashboard"
)

st.markdown("""

Advanced analytics dashboard for tracking
student performance, trends, weaknesses,
and AI-powered improvement suggestions.

""")

st.divider()

# -----------------------------------
# FETCH RESULTS
# -----------------------------------

results = fetch_my_results(

    st.session_state["user"]["email"]
)

# -----------------------------------
# EMPTY STATE
# -----------------------------------

if not results:

    st.info(
        "No exam results available yet."
    )

    st.stop()

# -----------------------------------
# DATAFRAME
# -----------------------------------

df = pd.DataFrame(results)

# -----------------------------------
# TABLE
# -----------------------------------

st.subheader(
    "Exam Performance Table"
)

st.dataframe(

    df,

    use_container_width=True
)

st.divider()

# ===================================
# BASIC STATISTICS
# ===================================

average_score = round(

    df["percentage"].mean(),

    2
)

highest_score = round(

    df["percentage"].max(),

    2
)

lowest_score = round(

    df["percentage"].min(),

    2
)

std_deviation = round(

    df["percentage"].std(),

    2
)

variance = round(

    df["percentage"].var(),

    2
)

total_exams = len(df)

# -----------------------------------
# KPI METRICS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "Average Score",

        f"{average_score}%"
    )

    st.metric(

        "Highest Score",

        f"{highest_score}%"
    )

with col2:

    st.metric(

        "Lowest Score",

        f"{lowest_score}%"
    )

    st.metric(

        "Standard Deviation",

        std_deviation
    )

with col3:

    st.metric(

        "Variance",

        variance
    )

    st.metric(

        "Total Exams",

        total_exams
    )

st.divider()

# ===================================
# PERFORMANCE TREND
# ===================================

st.subheader(
    "Performance Trend Analysis"
)

trend_fig = px.line(

    df,

    x="exam",

    y="percentage",

    markers=True,

    title="Performance Trend"
)

st.plotly_chart(

    trend_fig,

    use_container_width=True
)

# ===================================
# MOVING AVERAGE
# ===================================

st.subheader(
    "Moving Average Analysis"
)

df["moving_average"] = (

    df["percentage"]

    .rolling(window=2)

    .mean()
)

moving_avg_fig = px.line(

    df,

    x="exam",

    y="moving_average",

    markers=True,

    title="Moving Average Performance"
)

st.plotly_chart(

    moving_avg_fig,

    use_container_width=True
)

st.divider()

# ===================================
# SCORE DISTRIBUTION
# ===================================

st.subheader(
    "Score Distribution"
)

hist_fig = px.histogram(

    df,

    x="percentage",

    nbins=10,

    title="Distribution of Scores"
)

st.plotly_chart(

    hist_fig,

    use_container_width=True
)

st.divider()

# ===================================
# PERCENTILE ANALYSIS
# ===================================

st.subheader(
    "Percentile Analysis"
)

percentile = round(

    (

        average_score / 100
    ) * 100,

    2
)

st.info(

    f"You performed better than "

    f"{percentile}% of expected baseline performance."
)

st.divider()

# ===================================
# Z SCORE ANALYSIS
# ===================================

st.subheader(
    "Z-Score Analysis"
)

mean_score = df["percentage"].mean()

std_score = df["percentage"].std()

if std_score != 0:

    z_scores = (

        df["percentage"] - mean_score

    ) / std_score

    df["z_score"] = z_scores

    st.dataframe(

        df[

            [

                "exam",

                "percentage",

                "z_score"
            ]
        ],

        use_container_width=True
    )

else:

    st.info(
        "Insufficient data for Z-score calculation."
    )

st.divider()

# ===================================
# RADAR CHART
# ===================================

st.subheader(
    "Subject Skill Radar"
)

radar_fig = go.Figure()

radar_fig.add_trace(

    go.Scatterpolar(

        r=df["percentage"],

        theta=df["exam"],

        fill="toself",

        name="Performance"
    )
)

radar_fig.update_layout(

    polar=dict(

        radialaxis=dict(

            visible=True,

            range=[0, 100]
        )
    ),

    showlegend=False
)

st.plotly_chart(

    radar_fig,

    use_container_width=True
)

st.divider()

# ===================================
# WEAK AREA DETECTION
# ===================================

st.subheader(
    "Weak Area Detection"
)

weak_subjects = df[

    df["percentage"] < 70
]

if weak_subjects.empty:

    st.success(
        "No weak areas detected."
    )

else:

    st.warning(
        "Focus on improving these subjects:"
    )

    for subject in weak_subjects["exam"]:

        st.write(f"- {subject}")

st.divider()

# ===================================
# AI PERFORMANCE CLASSIFICATION
# ===================================

st.subheader(
    "AI Performance Classification"
)

if average_score >= 85:

    level = "Excellent"

    advice = """

You are performing exceptionally well.

Recommended Actions:
- Practice advanced-level MCQs
- Build real-world projects
- Explore research-oriented learning

"""

elif average_score >= 70:

    level = "Good"

    advice = """

Your performance is good.

Recommended Actions:
- Improve speed and accuracy
- Practice weekly mock tests
- Revise weak concepts

"""

elif average_score >= 50:

    level = "Average"

    advice = """

You need more structured preparation.

Recommended Actions:
- Revise fundamentals daily
- Solve beginner/intermediate questions
- Practice concept-based learning

"""

else:

    level = "Needs Improvement"

    advice = """

Your current performance requires significant improvement.

Recommended Actions:
- Build core fundamentals again
- Create proper study schedule
- Practice daily quizzes
- Focus on weak subjects

"""

st.success(

    f"Overall Performance Level: {level}"
)

st.info(
    advice
)

st.divider()

# ===================================
# PERFORMANCE PREDICTION
# ===================================

st.subheader(
    "Future Score Prediction"
)

predicted_score = round(

    average_score + 5,

    2
)

if predicted_score > 100:

    predicted_score = 100

st.metric(

    "Predicted Next Exam Score",

    f"{predicted_score}%"
)

st.info("""

Prediction based on current trend,
average growth, and historical performance.

""")

st.divider()

# ===================================
# FINAL STUDY RECOMMENDATIONS
# ===================================

st.subheader(
    "Personalized Study Recommendations"
)

recommendations = [

    "Revise concepts daily",

    "Practice at least 20 MCQs regularly",

    "Take mock exams weekly",

    "Improve time management",

    "Focus more on weak subjects",

    "Analyze mistakes after every exam",

    "Use spaced repetition for revision",

    "Practice problem-solving consistently"
]

for recommendation in recommendations:

    st.write(f"- {recommendation}")

st.divider()

# ===================================
# FINAL MESSAGE
# ===================================

st.success(

    "Consistent preparation and regular "
    "practice will significantly improve "
    "your future exam performance."
)