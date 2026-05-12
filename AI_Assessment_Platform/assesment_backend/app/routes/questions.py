from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import Question

from app.security import verify_token

from app.services.ai_generation_service import (
    generate_questions
)

from app.services.question_bank_service import (
    save_generated_questions
)

router = APIRouter()

# -----------------------------------
# GENERATE QUESTIONS
# -----------------------------------

@router.post("/generate_questions")

def ai_generate_questions(

    data: dict,

    db: Session = Depends(get_db),

    current_user: dict = Depends(
        verify_token
    )
):

    if current_user["role"] != "teacher":

        return {

            "error":

            "Only teachers can generate questions"
        }

    topic = data.get("topic")

    difficulty = data.get("difficulty")

    num_questions = data.get(
        "num_questions"
    )

    questions = generate_questions(

        topic,

        difficulty,

        num_questions
    )

    save_generated_questions(

        db,

        questions,

        current_user["email"]
    )

    return {

        "generated_questions":
        questions
    }

# -----------------------------------
# FETCH QUESTIONS
# -----------------------------------

@router.get("/questions")

def fetch_questions(

    db: Session = Depends(get_db)
):

    questions = db.query(
        Question
    ).all()

    serialized_questions = []

    for question in questions:

        serialized_questions.append({

            "id": question.id,

            "question": question.question,

            "difficulty":
            question.difficulty,

            "topic":
            question.topic
        })

    return serialized_questions