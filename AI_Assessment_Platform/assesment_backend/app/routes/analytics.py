from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.security import verify_token

from app.services.analytics_service import (
    get_all_results,
    get_analytics_summary
)

router = APIRouter()

# -----------------------------------
# TEACHER ANALYTICS
# -----------------------------------

@router.get("/analytics")

def analytics(

    db: Session = Depends(get_db),

    current_user: dict = Depends(
        verify_token
    )
):

    if current_user["role"] != "teacher":

        return {

            "error":

            "Only teachers can access analytics"
        }

    summary = get_analytics_summary(db)

    return summary

# -----------------------------------
# TEACHER RESULTS
# -----------------------------------

@router.get("/results")

def results(

    db: Session = Depends(get_db),

    current_user: dict = Depends(
        verify_token
    )
):

    if current_user["role"] != "teacher":

        return {

            "error":

            "Only teachers can access results"
        }

    all_results = get_all_results(db)

    return all_results

# -----------------------------------
# STUDENT RESULTS
# -----------------------------------

@router.get("/my_results")

def my_results(

    db: Session = Depends(get_db),

    current_user: dict = Depends(
        verify_token
    )
):

    all_results = get_all_results(db)

    student_results = []

    for result in all_results:

        if result["student_name"] == current_user["sub"]:

            student_results.append(result)

    return student_results