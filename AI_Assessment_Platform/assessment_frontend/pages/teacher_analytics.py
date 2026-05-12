import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import (
    show_sidebar
)

from services.api_client import (
    fetch_analytics
)

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="Teacher Analytics",

    layout="wide"
)

# ===================================
# LOGIN CHECK
# ===================================

if "logged_in" not in st.session_state:

    st.warning(
        "Please login first."
    )

    st.stop()

# ===================================
# ROLE CHECK
# ===================================

user = st.session_state.get(
    "user",
    {}
)

if user.get("role") != "teacher":

    st.error(
        "Teacher Access Only"
    )

    st.stop()

# ===================================
# SIDEBAR
# ===================================

show_sidebar()

# ===================================
# PAGE TITLE
# ===================================

st.title(
    "Teacher Analytics Dashboard"
)

st.markdown("""

Analyze student performance,
weak areas, and exam statistics.

""")

st.divider()

# ===================================
# FETCH ANALYTICS
# ===================================

analytics = fetch_analytics(

    st.session_state.token
)

# ===================================
# DEBUG
# ===================================

print("ANALYTICS:", analytics)

# ===================================
# EMPTY CHECK
# ===================================

if not analytics:

    st.info(
        "No analytics data available."
    )

    st.stop()

# ===================================
# ENSURE LIST FORMAT
# ===================================

if isinstance(analytics, dict):

    if "data" in analytics:

        analytics = analytics["data"]

    else:

        analytics = [analytics]

# ===================================
# DATAFRAME
# ===================================

try:

    df = pd.DataFrame(
        analytics
    )

except Exception as e:

    st.error(
        f"DataFrame Error: {e}"
    )

    st.stop()

# ===================================
# EMPTY DF
# ===================================

if df.empty:

    st.info(
        "No analytics records found."
    )

    st.stop()

# ===================================
# TABLE
# ===================================

st.subheader(
    "Student Performance Table"
)

st.dataframe(

    df,

    use_container_width=True
)

st.divider()

# ===================================
# SAFE COLUMN CHECKS
# ===================================

required_columns = [

    "percentage",

    "student_email",

    "performance_level"
]

for col in required_columns:

    if col not in df.columns:

        st.error(
            f"Missing column: {col}"
        )

        st.stop()

# ===================================
# KPI METRICS
# ===================================

average_percentage = round(

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

total_students = len(df)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Average Score",

        f"{average_percentage}%"
    )

with col2:

    st.metric(

        "Highest Score",

        f"{highest_score}%"
    )

with col3:

    st.metric(

        "Lowest Score",

        f"{lowest_score}%"
    )

with col4:

    st.metric(

        "Total Students",

        total_students
    )

st.divider()

# ===================================
# SCORE DISTRIBUTION
# ===================================

st.subheader(
    "Performance Distribution"
)

hist_fig = px.histogram(

    df,

    x="percentage",

    nbins=10,

    title="Score Distribution"
)

st.plotly_chart(

    hist_fig,

    use_container_width=True
)

# ===================================
# PERFORMANCE CHART
# ===================================

st.subheader(
    "Student Performance"
)

bar_fig = px.bar(

    df,

    x="student_email",

    y="percentage",

    color="performance_level",

    title="Performance Comparison"
)

st.plotly_chart(

    bar_fig,

    use_container_width=True
)

st.divider()

# ===================================
# WEAK STUDENTS
# ===================================

st.subheader(
    "Weak Students"
)

weak_students = df[

    df["percentage"] < 50
]

if weak_students.empty:

    st.success(
        "No weak students detected."
    )

else:

    st.dataframe(

        weak_students,

        use_container_width=True
    )

st.divider()

# ===================================
# AI INSIGHTS
# ===================================

st.subheader(
    "AI Insights"
)

if average_percentage >= 85:

    st.success("""

Students are performing exceptionally well.

""")

elif average_percentage >= 70:

    st.info("""

Students are performing well overall.

""")

elif average_percentage >= 50:

    st.warning("""

Students need additional practice.

""")

else:

    st.error("""

Students require major improvement.

""")