import streamlit as st

from components.sidebar import (
    show_sidebar
)

from services.api_client import (

    fetch_exams,

    start_exam,

    submit_exam
)

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="Live Exam",

    layout="wide"
)

# ===================================
# CUSTOM CSS
# ===================================

st.markdown(

    """
<style>

.main {

    background-color: #0E1117;
}

h1, h2, h3, h4 {

    color: white;
}

.metric-card {

    padding: 25px;

    border-radius: 20px;

    background-color: #1E1E1E;

    text-align: center;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);

    transition: 0.3s;
}

.metric-card:hover {

    transform: scale(1.03);
}

.metric-title {

    font-size: 18px;

    color: #AAAAAA;
}

.metric-value {

    font-size: 35px;

    font-weight: bold;
}

.section-box {

    padding: 20px;

    border-radius: 15px;

    background-color: #1E1E1E;

    margin-bottom: 20px;
}

</style>
""",

    unsafe_allow_html=True
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

if user.get("role") != "student":

    st.error(
        "Student Access Only"
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
    "AI Live Examination"
)

st.markdown("""

Attempt your assigned assessment
and analyze your performance instantly.

""")

st.divider()

# ===================================
# FETCH EXAMS
# ===================================

exams = fetch_exams()

if not exams:

    st.warning(
        "No exams available."
    )

    st.stop()

# ===================================
# EXAM OPTIONS
# ===================================

exam_options = {

    exam["title"]: exam

    for exam in exams
}

selected_exam_title = st.selectbox(

    "Select Exam",

    list(exam_options.keys())
)

selected_exam = exam_options[
    selected_exam_title
]

selected_exam_id = selected_exam["id"]

# ===================================
# RESET IF EXAM CHANGES
# ===================================

if (

    "current_exam_id"
    not in st.session_state

):

    st.session_state.current_exam_id = (
        selected_exam_id
    )

if (

    st.session_state.current_exam_id
    !=
    selected_exam_id
):

    st.session_state.started_exam = False

    st.session_state.current_exam_id = (
        selected_exam_id
    )

# ===================================
# EXAM INFO
# ===================================

st.info(

    f"""
Exam:
{selected_exam['title']}

Duration:
{selected_exam['duration_minutes']} minutes
"""
)

st.divider()

# ===================================
# START EXAM
# ===================================

if st.button(
    "Start Exam"
):

    st.session_state.started_exam = True

# ===================================
# SHOW QUESTIONS
# ===================================

if st.session_state.get(
    "started_exam",
    False
):

    questions = start_exam(

        selected_exam_id,

        st.session_state.token
    )

    # ===================================
    # EMPTY QUESTIONS
    # ===================================

    if not questions:

        st.warning(
            "No questions assigned to this exam."
        )

        st.stop()

    # ===================================
    # ANSWER STORAGE
    # ===================================

    student_answers = {}

    # ===================================
    # DISPLAY QUESTIONS
    # ===================================

    for index, question in enumerate(

        questions,

        start=1
    ):

        st.markdown(

            f"""
<div class="section-box">

<h3>
Question {index}
</h3>

<p>
{question["question"]}
</p>

</div>
""",

            unsafe_allow_html=True
        )

        options = [

            question["option_a"],

            question["option_b"],

            question["option_c"],

            question["option_d"]
        ]

        selected_answer = st.radio(

            "Select Answer",

            options,

            key=f"{selected_exam_id}_{question['id']}"
        )

        student_answers[
            str(question["id"])
        ] = selected_answer

        st.divider()

    # ===================================
    # SUBMIT EXAM
    # ===================================

    if st.button(
        "Submit Exam"
    ):

        with st.spinner(

            "Evaluating Exam..."
        ):

            result = submit_exam(

                exam_id=selected_exam_id,

                answers=student_answers,

                token=st.session_state.token
            )

        # ===================================
        # RESULT DISPLAY
        # ===================================

        if "result" in result:

            exam_result = result["result"]

            st.success(
                "Exam Submitted Successfully"
            )

            st.divider()

            # ===================================
            # KPI CARDS
            # ===================================

            col1, col2, col3 = st.columns(3)

            with col1:

                st.markdown(

                    f"""
<div class="metric-card">

<div class="metric-value" style="color:#00FFAA;">
{exam_result['score']}
</div>

<div class="metric-title">
Score
</div>

</div>
""",

                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(

                    f"""
<div class="metric-card">

<div class="metric-value" style="color:#00BFFF;">
{exam_result['percentage']}%
</div>

<div class="metric-title">
Percentage
</div>

</div>
""",

                    unsafe_allow_html=True
                )

            with col3:

                st.markdown(

                    f"""
<div class="metric-card">

<div class="metric-value" style="color:#FFD700;">
{exam_result['performance_level']}
</div>

<div class="metric-title">
Performance
</div>

</div>
""",

                    unsafe_allow_html=True
                )

            st.divider()

            # ===================================
            # WEAK TOPICS
            # ===================================

            weak_topics = exam_result.get(

                "weak_topics",

                []
            )

            st.subheader(
                "Weak Topic Analysis"
            )

            if weak_topics:

                for topic in weak_topics:

                    st.error(
                        f"Weak Area: {topic}"
                    )

            else:

                st.success(
                    "No weak topics detected."
                )

            st.divider()

            # ===================================
            # STUDY RECOMMENDATIONS
            # ===================================

            st.subheader(
                "AI Study Recommendations"
            )

            recommendations = []

            for topic in weak_topics:

                recommendations.append(

                    f"Revise concepts related to {topic}"
                )

            if not recommendations:

                recommendations = [

                    "Continue practicing advanced questions",

                    "Take mock tests regularly"
                ]

            for recommendation in recommendations:

                st.info(
                    recommendation
                )

            st.divider()

            # ===================================
            # VIDEO RECOMMENDATIONS
            # ===================================

            st.subheader(
                "Recommended Learning Videos"
            )

            recommended_videos = exam_result.get(

                "recommended_videos",

                []
            )

            if recommended_videos:

                for video in recommended_videos:

                    st.markdown(

                        f"""
<div class="section-box">

<h4>
🎥 {video['title']}
</h4>

<a href="{video['url']}" target="_blank">

Watch on YouTube

</a>

</div>
""",

                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No video recommendations available."
                )

        else:

            st.error(
                "Exam submission failed."
            )