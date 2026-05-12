from fastapi import APIRouter

import requests

# ===================================
# ROUTER
# ===================================

router = APIRouter()

# ===================================
# CHATBOT API
# ===================================

@router.post("/chatbot")

def chatbot(data: dict):

    user_message = data.get(
        "message"
    )

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "phi3",

                "prompt": f"""

You are an AI educational tutor.

Explain concepts clearly and simply.

Student Question:
{user_message}

""",

                "stream": False
            }
        )

        output = response.json()

        return {

            "response":

            output.get(
                "response",
                "No response generated."
            )
        }

    except Exception as e:

        return {

            "response":

            f"Error: {str(e)}"
        }