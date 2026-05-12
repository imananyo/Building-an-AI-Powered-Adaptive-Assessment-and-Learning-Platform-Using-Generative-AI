import streamlit as st
import requests

from components.sidebar import (
    show_sidebar
)

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="AI Tutor Assistant",

    layout="wide"
)

# ===================================
# SIDEBAR
# ===================================

show_sidebar()

# ===================================
# TITLE
# ===================================

st.title(
    "AI Tutor Assistant"
)

st.markdown("""

Ask doubts, concepts, coding questions,
or weak-topic related questions.

""")

st.divider()

# ===================================
# CHAT HISTORY
# ===================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# ===================================
# USER INPUT
# ===================================

user_input = st.text_input(

    "Ask Your Question"
)

# ===================================
# SEND BUTTON
# ===================================

if st.button(
    "Ask AI"
):

    if user_input:

        with st.spinner(

            "AI is thinking..."
        ):

            response = requests.post(

                "http://127.0.0.1:8000/chatbot",

                json={

                    "message": user_input
                }
            )

            data = response.json()

            ai_response = data.get(

                "response",

                "No response."
            )

            st.session_state.chat_history.append(

                {

                    "question": user_input,

                    "answer": ai_response
                }
            )

# ===================================
# DISPLAY CHAT
# ===================================

for chat in reversed(

    st.session_state.chat_history
):

    st.markdown(

        f"""
<div style="
padding:20px;
border-radius:15px;
background-color:#1E1E1E;
margin-bottom:20px;
box-shadow:0px 4px 10px rgba(0,0,0,0.3);
">

<h4 style="color:#00BFFF;">
Student
</h4>

<p>
{chat['question']}
</p>

<hr>

<h4 style="color:#00FFAA;">
AI Tutor
</h4>

<p>
{chat['answer']}
</p>

</div>
""",

        unsafe_allow_html=True
    )