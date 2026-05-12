from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from pypdf import PdfReader

import requests
import tempfile
import os
import json

from app.database import SessionLocal

from app.models import (
    StudyMaterial,
    Question
)

# ===================================
# ROUTER
# ===================================

router = APIRouter()

# ===================================
# DATABASE SESSION
# ===================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

# ===================================
# SIMPLIFY MATERIAL
# ===================================

@router.post("/simplify_material")

async def simplify_material(

    title: str,

    file: UploadFile = File(...),

    db: Session = Depends(get_db)
):

    try:

        # ===================================
        # VALIDATE FILE
        # ===================================

        if not file.filename.endswith(".pdf"):

            return {

                "error":

                "Only PDF files are supported."
            }

        # ===================================
        # SAVE TEMP FILE
        # ===================================

        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".pdf"
        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_path = temp_file.name

        # ===================================
        # READ PDF
        # ===================================

        reader = PdfReader(
            temp_path
        )

        extracted_text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                extracted_text += (
                    page_text + "\n"
                )

        # ===================================
        # DELETE TEMP FILE
        # ===================================

        os.remove(temp_path)

        # ===================================
        # CHECK EMPTY TEXT
        # ===================================

        if not extracted_text.strip():

            return {

                "error":

                "No readable text found."
            }

        # ===================================
        # LIMIT TEXT
        # ===================================

        extracted_text = extracted_text[:5000]

        # ===================================
        # AI SIMPLIFICATION PROMPT
        # ===================================

        prompt = f"""

You are an AI educational assistant.

Simplify the following study material
into beginner-friendly notes.

Instructions:

- Explain concepts clearly
- Use simple language
- Add examples
- Use bullet points
- Create concise notes

Study Material:

{extracted_text}

"""

        # ===================================
        # CALL OLLAMA FOR NOTES
        # ===================================

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "phi3",

                "prompt": prompt,

                "stream": False
            },

            timeout=300
        )

        output = response.json()

        simplified_notes = output.get(

            "response",

            "No notes generated."
        )

        # ===================================
        # GENERATE MCQ QUESTIONS
        # ===================================

        mcq_prompt = f"""

You are an AI exam generator.

Generate 5 multiple choice questions
from the following study material.

Return ONLY valid JSON format.

Format:

[
  {{
    "question": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    "correct_answer": "...",
    "difficulty": "Easy",
    "topic": "..."
  }}
]

Study Material:

{extracted_text}

"""

        # ===================================
        # CALL OLLAMA FOR MCQ
        # ===================================

        mcq_response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "phi3",

                "prompt": mcq_prompt,

                "stream": False
            },

            timeout=300
        )

        mcq_output = mcq_response.json()

        generated_questions = mcq_output.get(

            "response",

            "[]"
        )

        # ===================================
        # CLEAN RESPONSE
        # ===================================

        generated_questions = generated_questions.strip()

        if generated_questions.startswith("```json"):

            generated_questions = (

                generated_questions
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        # ===================================
        # PARSE JSON
        # ===================================

        try:

            questions_data = json.loads(
                generated_questions
            )

        except Exception:

            questions_data = []

        # ===================================
        # SAVE MATERIAL TO DATABASE
        # ===================================

        material = StudyMaterial(

            title=title,

            filename=file.filename,

            extracted_text=extracted_text,

            simplified_notes=simplified_notes
        )

        db.add(material)

        db.commit()

        db.refresh(material)

        # ===================================
        # SAVE GENERATED QUESTIONS
        # ===================================

        saved_questions = []

        for item in questions_data:

            try:

                question = Question(

                    question=item.get(
                        "question"
                    ),

                    option_a=item.get(
                        "option_a"
                    ),

                    option_b=item.get(
                        "option_b"
                    ),

                    option_c=item.get(
                        "option_c"
                    ),

                    option_d=item.get(
                        "option_d"
                    ),

                    correct_answer=item.get(
                        "correct_answer"
                    ),

                    difficulty=item.get(
                        "difficulty",
                        "Easy"
                    ),

                    topic=item.get(
                        "topic",
                        title
                    ),

                    created_by="AI Material Generator"
                )

                db.add(question)

                saved_questions.append(
                    question
                )

            except Exception as e:

                print(e)

        db.commit()

        # ===================================
        # RETURN RESPONSE
        # ===================================

        return {

            "message":

            "Material uploaded successfully",

            "material_id":

            material.id,

            "simplified_notes":

            simplified_notes,

            "generated_questions":

            len(saved_questions)
        }

    except Exception as e:

        return {

            "error":

            str(e)
        }