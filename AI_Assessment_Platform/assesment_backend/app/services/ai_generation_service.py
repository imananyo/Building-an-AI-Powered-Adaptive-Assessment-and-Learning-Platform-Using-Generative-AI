import requests
import json
import re

# -----------------------------------
# OLLAMA URL
# -----------------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"

# -----------------------------------
# EXTRACT JSON
# -----------------------------------

def extract_json(text):

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    match = re.search(

        r"\[.*\]",

        text,

        re.DOTALL
    )

    if match:

        return match.group(0)

    return None

# -----------------------------------
# GENERATE SINGLE QUESTION
# -----------------------------------

def generate_single_question(

    topic,

    difficulty
):

    prompt = f"""

Generate EXACTLY ONE multiple choice question.

Topic:
{topic}

Difficulty:
{difficulty}

Return ONLY JSON.

FORMAT:

[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Correct Option"
  }}
]

"""

    response = requests.post(

        OLLAMA_URL,

        json={

            "model": "phi3",

            "prompt": prompt,

            "stream": False
        }
    )

    result = response.json()

    raw_response = result.get(
        "response",
        ""
    )

    json_text = extract_json(
        raw_response
    )

    if not json_text:

        raise Exception(
            "JSON extraction failed"
        )

    questions = json.loads(
        json_text
    )

    return questions[0]

# -----------------------------------
# GENERATE QUESTIONS
# -----------------------------------

def generate_questions(

    topic,

    difficulty,

    num_questions
):

    generated_questions = []

    # -----------------------------------
    # LOOP EXACT QUESTION COUNT
    # -----------------------------------

    for _ in range(num_questions):

        try:

            question = generate_single_question(

                topic,

                difficulty
            )

            question["difficulty"] = difficulty

            question["topic"] = topic

            generated_questions.append(
                question
            )

        except Exception as e:

            print("\nQUESTION GENERATION ERROR:\n")
            print(str(e))

            # -----------------------------------
            # FALLBACK QUESTION
            # -----------------------------------

            generated_questions.append(

                {

                    "question":

                    f"What is the purpose of {topic}?",

                    "options": [

                        "Correct Answer",

                        "Wrong Answer 1",

                        "Wrong Answer 2",

                        "Wrong Answer 3"
                    ],

                    "correct_answer":

                    "Correct Answer",

                    "difficulty":

                    difficulty,

                    "topic":

                    topic
                }
            )

    return generated_questions