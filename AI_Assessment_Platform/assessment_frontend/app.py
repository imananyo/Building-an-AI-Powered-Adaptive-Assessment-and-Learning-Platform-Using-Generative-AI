import streamlit as st

from services.api_client import (
    login_user,
    register_user
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title="AI Assessment Platform",

    page_icon="🎓",

    layout="wide"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

# -----------------------------------
# USER ALREADY LOGGED IN
# -----------------------------------

if st.session_state.logged_in:

    st.success(

        f"Welcome "

        f"{st.session_state.user['name']} 👋"
    )

    st.info(

        f"Logged in as "

        f"{st.session_state.user['role']}"
    )

    st.markdown("""

## Use the sidebar to navigate through the platform.

### Features Available

✅ AI Question Generation  
✅ Personalized Exams  
✅ Live Exam System  
✅ Auto Grading  
✅ AI Feedback  
✅ Analytics Dashboard  

""")

    st.stop()

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown("""

#  AI-Powered Assessment Platform

Generate AI exams, conduct assessments,
analyze student performance, and provide
instant AI feedback using local LLMs.

""")

st.divider()

# -----------------------------------
# TABS
# -----------------------------------

login_tab, signup_tab = st.tabs(

    [

        " Login",

        " Sign Up"
    ]
)

# ===================================
# LOGIN TAB
# ===================================

with login_tab:

    st.subheader(
        "Login To Your Account"
    )

    login_email = st.text_input(

        "Email",

        key="login_email"
    )

    login_password = st.text_input(

        "Password",

        type="password",

        key="login_password"
    )

    # -----------------------------------
    # LOGIN BUTTON
    # -----------------------------------

    if st.button("Login"):

        with st.spinner(

            "Authenticating..."
        ):

            result = login_user(

                login_email,

                login_password
            )

        # -----------------------------------
        # SUCCESS
        # -----------------------------------

        if result.get("success"):

            st.session_state.logged_in = True

            st.session_state.token = result.get(

                "access_token"
            )

            st.session_state.user = result.get(
                "user"
            )

            st.success(
                "Login Successful ✅"
            )

            st.rerun()

        else:

            st.error(

                result.get(

                    "message",

                    "Invalid Credentials"
                )
            )

# ===================================
# SIGNUP TAB
# ===================================

with signup_tab:

    st.subheader(
        "Create New Account"
    )

    signup_name = st.text_input(

        "Full Name"
    )

    signup_email = st.text_input(

        "Signup Email"
    )

    signup_password = st.text_input(

        "Signup Password",

        type="password"
    )

    signup_role = st.selectbox(

        "Select Role",

        [

            "teacher",

            "student"
        ]
    )

    # -----------------------------------
    # CREATE ACCOUNT BUTTON
    # -----------------------------------

    if st.button("Create Account"):

        signup_data = {

            "name": signup_name,

            "email": signup_email,

            "password": signup_password,

            "role": signup_role
        }

        with st.spinner(

            "Creating Account..."
        ):

            result = register_user(
                signup_data
            )

        # -----------------------------------
        # SUCCESS
        # -----------------------------------

        if "user_id" in result:

            st.success(
                "Account Created Successfully ✅"
            )

            st.info(
                "You can now login using your credentials."
            )

        else:

            st.error(

                result.get(

                    "error",

                    "Signup Failed"
                )
            )

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(

    "AI Assessment Platform • Built with "
    "FastAPI • Streamlit • Ollama • Llama3"
)