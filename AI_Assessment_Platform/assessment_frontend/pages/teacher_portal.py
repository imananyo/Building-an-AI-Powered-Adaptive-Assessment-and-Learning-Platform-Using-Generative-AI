import streamlit as st

from services.api_client import (
    generate_ai_questions
)

from components.sidebar import (
    show_sidebar
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title="Teacher Portal",

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

if user.get("role") != "teacher":

    st.error(
        "Teacher Access Only"
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
    "Teacher Portal"
)

st.markdown("""

Generate AI-powered MCQ questions
for assessments and examinations.

""")

st.divider()

# ===================================
# QUESTION GENERATION
# ===================================

st.subheader(
    "AI Question Generation"
)

# -----------------------------------
# INPUTS
# -----------------------------------

topic = st.text_input(
    "Enter Topic"
)

difficulty = st.selectbox(

    "Select Difficulty",

    [

        "Easy",

        "Medium",

        "Hard"
    ]
)

num_questions = st.slider(

    "Number of Questions",

    min_value=1,

    max_value=10,

    value=3
)

st.divider()

# -----------------------------------
# GENERATE BUTTON
# -----------------------------------

if st.button("Generate Questions"):

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not topic:

        st.warning(
            "Please enter a topic."
        )

    else:

        # -----------------------------------
        # LOADING SPINNER
        # -----------------------------------

        with st.spinner(

            "Generating AI Questions..."
        ):

            result = generate_ai_questions(

                topic,

                difficulty,

                num_questions,

                st.session_state.token
            )

        questions = result.get(

            "generated_questions",

            []
        )

        # -----------------------------------
        # EMPTY STATE
        # -----------------------------------

        if not questions:

            st.error(
                "No questions generated."
            )

        else:

            st.success(

                f"{len(questions)} "
                f"Questions Generated Successfully"
            )

            st.divider()

            # -----------------------------------
            # DISPLAY QUESTIONS
            # -----------------------------------

            for index, question in enumerate(

                questions,

                start=1
            ):

                st.subheader(
                    f"Question {index}"
                )

                st.write(
                    question["question"]
                )

                st.write(
                    f"A. {question['options'][0]}"
                )

                st.write(
                    f"B. {question['options'][1]}"
                )

                st.write(
                    f"C. {question['options'][2]}"
                )

                st.write(
                    f"D. {question['options'][3]}"
                )

                st.success(

                    f"Correct Answer: "

                    f"{question['correct_answer']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.info(

                        f"Difficulty: "

                        f"{question['difficulty']}"
                    )

                with col2:

                    st.info(

                        f"Topic: "

                        f"{question['topic']}"
                    )

                st.divider()