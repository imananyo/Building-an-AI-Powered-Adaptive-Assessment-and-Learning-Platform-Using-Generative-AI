import streamlit as st
import pandas as pd

from components.sidebar import (
    show_sidebar
)

from services.api_client import (

    fetch_questions,

    fetch_exams,

    add_questions_to_exam,

    create_exam
)

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="Exam Builder",

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
# TITLE
# ===================================

st.title(
    "Exam Builder"
)

st.markdown("""

Assign questions to exams and build
custom assessments.

""")

st.divider()

# ===================================
# CREATE NEW EXAM
# ===================================

st.subheader(
    "Create New Exam"
)

new_exam_title = st.text_input(
    "Exam Title"
)

new_exam_description = st.text_area(
    "Exam Description"
)

new_exam_duration = st.number_input(

    "Duration (Minutes)",

    min_value=1,

    value=30
)

if st.button(
    "Create Exam"
):

    if not new_exam_title:

        st.error(
            "Please enter exam title."
        )

    else:

        exam_data = {

            "title":

            new_exam_title,

            "description":

            new_exam_description,

            "duration_minutes":

            new_exam_duration
        }

        response = create_exam(

            exam_data,

            st.session_state.token
        )

        if response:

            st.success(
                "Exam Created Successfully"
            )

            st.rerun()

        else:

            st.error(
                "Failed to create exam"
            )

st.divider()

# ===================================
# FETCH EXAMS
# ===================================

exams = fetch_exams()

if not exams:

    st.info(
        "No exams available."
    )

    st.stop()

# ===================================
# EXAM DROPDOWN
# ===================================

exam_titles = [

    exam["title"]

    for exam in exams
]

selected_exam_title = st.selectbox(

    "Select Exam",

    exam_titles
)

selected_exam = next(

    exam

    for exam in exams

    if exam["title"] == selected_exam_title
)

selected_exam_id = selected_exam["id"]

st.divider()

# ===================================
# FETCH QUESTIONS
# ===================================

questions = fetch_questions()

if not questions:

    st.info(
        "No questions available."
    )

    st.stop()

# ===================================
# DISPLAY QUESTIONS
# ===================================

st.subheader(
    "Available Questions"
)

question_df = pd.DataFrame(

    [

        {

            "id":

            q["id"],

            "question":

            q["question"],

            "difficulty":

            q["difficulty"],

            "topic":

            q["topic"]
        }

        for q in questions
    ]
)

st.dataframe(

    question_df,

    use_container_width=True
)

st.divider()

# ===================================
# QUESTION SELECTION
# ===================================

question_options = {

    f"{q['id']} - {q['question'][:80]}":

    q["id"]

    for q in questions
}

selected_questions = st.multiselect(

    "Select Questions for Exam",

    options=list(
        question_options.keys()
    )
)

# ===================================
# ASSIGN QUESTIONS
# ===================================

if st.button(
    "Assign Questions to Exam"
):

    if not selected_questions:

        st.warning(
            "Please select questions."
        )

    else:

        question_ids = [

            question_options[q]

            for q in selected_questions
        ]

        response = add_questions_to_exam(

            selected_exam_id,

            question_ids,

            st.session_state.token
        )

        if response:

            st.success(
                "Questions Assigned Successfully"
            )

        else:

            st.error(
                "Failed to assign questions."
            )

st.divider()

# ===================================
# SUMMARY
# ===================================

st.subheader(
    "Exam Summary"
)

st.info(

    f"""
Selected Exam:
{selected_exam_title}

Questions Selected:
{len(selected_questions)}
"""
)