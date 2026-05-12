from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import (
    SessionLocal
)

from app.models import (
    Result
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
# FETCH ALL RESULTS
# ===================================

@router.get("/results")

def get_results(

    db: Session = Depends(get_db)
):

    results = db.query(
        Result
    ).all()

    output = []

    for result in results:

        output.append(

            {

                "student_email":

                result.student_email,

                "exam_id":

                result.exam_id,

                "score":

                result.score,

                "total_questions":

                result.total_questions,

                "percentage":

                result.percentage,

                "weak_topics":

                result.weak_topics,

                "performance_level":

                result.performance_level
            }
        )

    return output

# ===================================
# FETCH STUDENT RESULTS
# ===================================

@router.get("/my_results")

def get_my_results(

    student_email: str,

    db: Session = Depends(get_db)
):

    results = db.query(
        Result
    ).filter(

        Result.student_email
        ==
        student_email
    ).all()

    output = []

    for result in results:

        output.append(

            {

                "exam":

                f"Exam {result.exam_id}",

                "student_email":

                result.student_email,

                "score":

                result.score,

                "total_questions":

                result.total_questions,

                "percentage":

                result.percentage,

                "weak_topics":

                result.weak_topics,

                "performance_level":

                result.performance_level
            }
        )

    return output