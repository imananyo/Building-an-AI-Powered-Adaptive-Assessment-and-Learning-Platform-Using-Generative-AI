import requests
import streamlit as st

# ===================================
# BASE URL
# ===================================

BASE_URL = "http://127.0.0.1:8000"

# ===================================
# LOGIN USER
# ===================================

def login_user(

    email,

    password
):

    try:

        response = requests.post(

            f"{BASE_URL}/login",

            data={

                "username": email,

                "password": password
            }
        )

        return response.json()

    except Exception as e:

        return {

            "success": False,

            "message": str(e)
        }

# ===================================
# REGISTER USER
# ===================================

def register_user(data):

    try:

        response = requests.post(

            f"{BASE_URL}/register",

            json=data
        )

        return response.json()

    except Exception as e:

        return {

            "error": str(e)
        }

# ===================================
# GENERATE AI QUESTIONS
# ===================================

def generate_ai_questions(

    topic,

    difficulty,

    num_questions,

    token
):

    try:

        response = requests.post(

            f"{BASE_URL}/generate_questions",

            headers={

                "Authorization":

                f"Bearer {token}"
            },

            json={

                "topic": topic,

                "difficulty": difficulty,

                "num_questions": num_questions
            }
        )

        if response.status_code != 200:

            return {

                "generated_questions": []
            }

        if not response.text:

            return {

                "generated_questions": []
            }

        return response.json()

    except Exception as e:

        print(e)

        return {

            "generated_questions": []
        }

# ===================================
# FETCH QUESTIONS
# ===================================

def fetch_questions():

    try:

        response = requests.get(

            f"{BASE_URL}/questions"
        )

        if response.status_code != 200:

            return []

        if not response.text:

            return []

        return response.json()

    except Exception as e:

        print(e)

        return []

# ===================================
# CREATE EXAM
# ===================================

def create_exam(

    exam_data,

    token
):

    try:

        response = requests.post(

            f"{BASE_URL}/create_exam",

            headers={

                "Authorization":

                f"Bearer {token}"
            },

            json=exam_data
        )

        if response.status_code != 200:

            return {}

        if not response.text:

            return {}

        return response.json()

    except Exception as e:

        print(e)

        return {}

# ===================================
# FETCH EXAMS
# ===================================

def fetch_exams():

    try:

        response = requests.get(

            f"{BASE_URL}/exams"
        )

        if response.status_code != 200:

            return []

        if not response.text:

            return []

        return response.json()

    except Exception as e:

        print(e)

        return []

# ===================================
# ADD QUESTIONS TO EXAM
# ===================================

def add_questions_to_exam(

    exam_id,

    question_ids,

    token
):

    try:

        response = requests.post(

            f"{BASE_URL}/add_questions_to_exam",

            headers={

                "Authorization":

                f"Bearer {token}"
            },

            json={

                "exam_id": exam_id,

                "question_ids": question_ids
            }
        )

        if response.status_code != 200:

            return {}

        if not response.text:

            return {}

        return response.json()

    except Exception as e:

        print(e)

        return {}

# ===================================
# START EXAM
# ===================================

def start_exam(

    exam_id,

    token
):

    try:

        response = requests.get(

            f"{BASE_URL}/start_exam/{exam_id}",

            headers={

                "Authorization":

                f"Bearer {token}"
            }
        )

        if response.status_code != 200:

            return []

        if not response.text:

            return []

        return response.json()

    except Exception as e:

        print(e)

        return []

# ===================================
# SUBMIT EXAM
# ===================================

def submit_exam(

    exam_id,

    answers,

    token
):

    try:

        # -----------------------------------
        # GET LOGGED-IN USER
        # -----------------------------------

        user = st.session_state.get(

            "user",

            {}
        )

        student_email = user.get(
            "email"
        )

        # -----------------------------------
        # API REQUEST
        # -----------------------------------

        response = requests.post(

            f"{BASE_URL}/submit_exam",

            json={

                "student_email":

                student_email,

                "exam_id":

                exam_id,

                "answers":

                answers
            },

            headers={

                "Authorization":

                f"Bearer {token}"
            }
        )

        # -----------------------------------
        # SAFE RESPONSE
        # -----------------------------------

        if response.status_code != 200:

            return {}

        if not response.text:

            return {}

        return response.json()

    except Exception as e:

        print(e)

        return {}

# ===================================
# FETCH ANALYTICS
# ===================================

def fetch_analytics(token):

    try:

        response = requests.get(

            f"{BASE_URL}/analytics",

            headers={

                "Authorization":

                f"Bearer {token}"
            }
        )

        if response.status_code != 200:

            return []

        if not response.text:

            return []

        return response.json()

    except Exception as e:

        print(e)

        return []

# ===================================
# FETCH RESULTS
# ===================================

def fetch_results(token):

    try:

        response = requests.get(

            f"{BASE_URL}/results",

            headers={

                "Authorization":

                f"Bearer {token}"
            }
        )

        if response.status_code != 200:

            return []

        if not response.text:

            return []

        return response.json()

    except Exception as e:

        print(e)

        return []

# ===================================
# FETCH MY RESULTS
# ===================================

def fetch_my_results(

    student_email
):

    try:

        response = requests.get(

            f"{BASE_URL}/my_results",

            params={

                "student_email":

                student_email
            }
        )

        # -----------------------------------
        # SAFE RESPONSE
        # -----------------------------------

        if response.status_code != 200:

            return []

        if not response.text:

            return []

        if response.text.strip() == "":

            return []

        return response.json()

    except Exception as e:

        print(e)

        return []