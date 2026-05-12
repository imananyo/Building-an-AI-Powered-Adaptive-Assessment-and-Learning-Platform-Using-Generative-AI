from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import (
    SessionLocal
)

from app.models import (
    Exam
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
# CREATE EXAM
# ===================================

@router.post("/create_exam")

def create_exam(

    data: dict,

    db: Session = Depends(get_db)
):

    try:

        exam = Exam(

            title=data.get(
                "title"
            ),

            description=data.get(
                "description"
            ),

            duration_minutes=data.get(
                "duration_minutes"
            )
        )

        db.add(exam)

        db.commit()

        db.refresh(exam)

        return {

            "message":

            "Exam created successfully",

            "exam_id":

            exam.id
        }

    except Exception as e:

        return {

            "error":

            str(e)
        }

# ===================================
# FETCH EXAMS
# ===================================

@router.get("/exams")

def get_exams(

    db: Session = Depends(get_db)
):

    try:

        exams = db.query(
            Exam
        ).all()

        output = []

        for exam in exams:

            output.append(

                {

                    "id":

                    exam.id,

                    "title":

                    exam.title,

                    "description":

                    exam.description,

                    "duration_minutes":

                    exam.duration_minutes
                }
            )

        return output

    except Exception as e:

        return {

            "error":

            str(e)
        }