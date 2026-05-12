import streamlit as st

# Check login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.warning("Please login first")

    st.stop()

# Dashboard UI
st.title("📊 Student Dashboard")

st.subheader("Welcome Student")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Upcoming Exams",
    3
)

col2.metric(
    "Completed Exams",
    10
)

col3.metric(
    "Average Score",
    "40%"
)

st.divider()

st.subheader("Recent Activity")

st.write("✅ Physics Midterm Completed")

st.write("📝 AI Quiz Tomorrow")

st.write("📈 Performance Improved")