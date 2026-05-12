from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import (
    SessionLocal
)

from app.models import (
    ExamQuestion
)

# ===================================
# ROUTER
# ===================================

router = APIRouter()

# ===================================
# DATABASE
# ===================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()

# ===================================
# ADD QUESTIONS TO EXAM
# ===================================

@router.post("/add_questions_to_exam")

def add_questions_to_exam(

    data: dict,

    db: Session = Depends(get_db)
):

    exam_id = data.get(
        "exam_id"
    )

    question_ids = data.get(
        "question_ids",
        []
    )

    # -----------------------------------
    # SAVE MAPPINGS
    # -----------------------------------

    for question_id in question_ids:

        mapping = ExamQuestion(

            exam_id=exam_id,

            question_id=question_id
        )

        db.add(mapping)

    db.commit()

    return {

        "message":

        "Questions assigned successfully"
    }