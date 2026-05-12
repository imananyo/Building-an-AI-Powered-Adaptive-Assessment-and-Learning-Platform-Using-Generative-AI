import streamlit as st
import requests

from components.sidebar import (
    show_sidebar
)

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(

    page_title="AI Material Simplifier",

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

.upload-box {

    padding: 30px;

    border-radius: 20px;

    background-color: #1E1E1E;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);

    margin-bottom: 20px;
}

.result-box {

    padding: 25px;

    border-radius: 20px;

    background-color: #1E1E1E;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);

    margin-top: 20px;
}

.metric-card {

    padding: 20px;

    border-radius: 15px;

    background-color: #1E1E1E;

    text-align: center;

    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

</style>
""",

    unsafe_allow_html=True
)

# ===================================
# SIDEBAR
# ===================================

show_sidebar()

# ===================================
# TITLE
# ===================================

st.title(
    "AI Study Material Simplifier"
)

st.markdown("""

Upload study materials and let AI:

✅ simplify notes  
✅ generate MCQs  
✅ create exam-ready questions

""")

st.divider()

# ===================================
# MATERIAL TITLE
# ===================================

title = st.text_input(

    "Enter Material Title"
)

# ===================================
# FILE UPLOADER
# ===================================

uploaded_file = st.file_uploader(

    "Upload PDF File",

    type=["pdf"]
)

# ===================================
# PROCESS MATERIAL
# ===================================

if uploaded_file and title:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "Generate AI Content"
    ):

        with st.spinner(

            "AI is processing material..."
        ):

            try:

                files = {

                    "file":

                    uploaded_file
                }

                response = requests.post(

                    "http://127.0.0.1:8000/simplify_material",

                    params={

                        "title": title
                    },

                    files=files
                )

                data = response.json()

                # ===================================
                # ERROR
                # ===================================

                if "error" in data:

                    st.error(
                        data["error"]
                    )

                else:

                    st.success(
                        "Material Processed Successfully"
                    )

                    st.divider()

                    # ===================================
                    # METRICS
                    # ===================================

                    col1, col2 = st.columns(2)

                    with col1:

                        st.markdown(

                            f"""
<div class="metric-card">

<h2 style="color:#00FFAA;">
{data.get('material_id')}
</h2>

<p>
Material ID
</p>

</div>
""",

                            unsafe_allow_html=True
                        )

                    with col2:

                        st.markdown(

                            f"""
<div class="metric-card">

<h2 style="color:#00BFFF;">
{data.get('generated_questions')}
</h2>

<p>
AI Generated Questions
</p>

</div>
""",

                            unsafe_allow_html=True
                        )

                    st.divider()

                    # ===================================
                    # SIMPLIFIED NOTES
                    # ===================================

                    st.subheader(
                        "Simplified Notes"
                    )

                    st.markdown(

                        f"""
<div class="result-box">

{data.get('simplified_notes')}

</div>
""",

                        unsafe_allow_html=True
                    )

                    st.divider()

                    # ===================================
                    # SUCCESS MESSAGE
                    # ===================================

                    st.success(

                        "AI exam questions generated and saved successfully."
                    )

            except Exception as e:

                st.error(
                    str(e)
                )

else:

    st.info(
        "Upload PDF and enter title."
    )