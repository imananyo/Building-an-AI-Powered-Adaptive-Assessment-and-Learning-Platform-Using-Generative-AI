import streamlit as st
import os

# ===================================
# SAFE PAGE LINK
# ===================================

def safe_page_link(

    path,

    label
):

    try:

        current_dir = os.path.dirname(
            __file__
        )

        frontend_dir = os.path.abspath(

            os.path.join(
                current_dir,
                ".."
            )
        )

        full_path = os.path.join(

            frontend_dir,

            path
        )

        if os.path.exists(full_path):

            st.sidebar.page_link(

                path,

                label=label
            )

    except Exception as e:

        print(e)

# ===================================
# SIDEBAR
# ===================================

def show_sidebar():

    st.sidebar.title(
        "AI Assessment Platform"
    )

    st.sidebar.divider()

    # ===================================
    # USER INFO
    # ===================================

    user = st.session_state.get(
        "user",
        {}
    )

    if user:

        st.sidebar.success(

            f"Logged in as: {user.get('role', '').title()}"
        )

    st.sidebar.divider()

    # ===================================
    # HOME
    # ===================================

    safe_page_link(

        "app.py",

        "Home"
    )

    # ===================================
    # TEACHER PAGES
    # ===================================

    if user.get("role") == "teacher":

        safe_page_link(

            "pages/generate_questions.py",

            "Generate Questions"
        )

        safe_page_link(

            "pages/create_exam.py",

            "Create Exam"
        )

        safe_page_link(

            "pages/exam_builder.py",

            "Exam Builder"
        )

        safe_page_link(

            "pages/teacher_analytics.py",

            "Teacher Analytics"
        )

    # ===================================
    # STUDENT PAGES
    # ===================================

    elif user.get("role") == "student":

        safe_page_link(

            "pages/live_exam.py",

            "Live Exam"
        )

        safe_page_link(

            "pages/student_dashboard.py",

            "Student Dashboard"
        )

    # ===================================
    # AI CHATBOT
    # ===================================

    safe_page_link(

        "pages/ai_chatbot.py",

        "AI Tutor Assistant"
    )

    # ===================================
    # MATERIAL SIMPLIFIER
    # ===================================

    safe_page_link(

        "pages/material_simplifier.py",

        "AI Material Simplifier"
    )

    st.sidebar.divider()

    # ===================================
    # LOGOUT
    # ===================================

    if st.sidebar.button(
        "Logout"
    ):

        st.session_state.clear()

        st.switch_page(
            "app.py"
        )