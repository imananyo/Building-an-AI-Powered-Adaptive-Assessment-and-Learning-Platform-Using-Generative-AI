from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import (
    SessionLocal
)

from app.models import (
    Question,
    ExamQuestion,
    Result,
    StudentSubmission
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
# START EXAM
# ===================================

@router.get("/start_exam/{exam_id}")

def start_exam(

    exam_id: int,

    db: Session = Depends(get_db)
):

    mappings = db.query(
        ExamQuestion
    ).filter(

        ExamQuestion.exam_id == exam_id
    ).all()

    question_ids = [

        mapping.question_id

        for mapping in mappings
    ]

    questions = db.query(
        Question
    ).filter(

        Question.id.in_(question_ids)
    ).all()

    output = []

    for question in questions:

        output.append(

            {

                "id":

                question.id,

                "question":

                question.question,

                "option_a":

                question.option_a,

                "option_b":

                question.option_b,

                "option_c":

                question.option_c,

                "option_d":

                question.option_d,

                "topic":

                question.topic
            }
        )

    return output

# ===================================
# SUBMIT EXAM
# ===================================

@router.post("/submit_exam")

def submit_exam(

    data: dict,

    db: Session = Depends(get_db)
):

    try:

        student_email = data.get(
            "student_email"
        )

        exam_id = data.get(
            "exam_id"
        )

        answers = data.get(
            "answers",
            {}
        )

        # ===================================
        # FETCH EXAM QUESTIONS
        # ===================================

        mappings = db.query(
            ExamQuestion
        ).filter(

            ExamQuestion.exam_id == exam_id
        ).all()

        question_ids = [

            mapping.question_id

            for mapping in mappings
        ]

        questions = db.query(
            Question
        ).filter(

            Question.id.in_(question_ids)
        ).all()

        # ===================================
        # INITIALIZE VARIABLES
        # ===================================

        score = 0

        weak_topics = []

        total_questions = len(
            questions
        )

        # ===================================
        # CHECK ANSWERS
        # ===================================

        for question in questions:

            student_answer = answers.get(
                str(question.id)
            )

            # SAVE SUBMISSION

            submission = StudentSubmission(

                student_email=student_email,

                exam_id=exam_id,

                question_id=question.id,

                selected_answer=student_answer
            )

            db.add(submission)

            # CHECK CORRECT ANSWER

            if (

                student_answer
                ==
                question.correct_answer
            ):

                score += 1

            else:

                weak_topics.append(
                    question.topic
                )

        # ===================================
        # CALCULATE PERCENTAGE
        # ===================================

        if total_questions > 0:

            percentage = round(

                (score / total_questions)
                * 100,

                2
            )

        else:

            percentage = 0

        # ===================================
        # PERFORMANCE LEVEL
        # ===================================

        if percentage >= 80:

            performance_level = "Excellent"

        elif percentage >= 60:

            performance_level = "Good"

        elif percentage >= 40:

            performance_level = "Average"

        else:

            performance_level = "Needs Improvement"

        # ===================================
        # REMOVE DUPLICATE TOPICS
        # ===================================

        weak_topics = list(
            set(weak_topics)
        )

        # ===================================
        # SAVE RESULT
        # ===================================

        result = Result(

            student_email=student_email,

            exam_id=exam_id,

            score=score,

            total_questions=total_questions,

            percentage=percentage,

            weak_topics=", ".join(
                weak_topics
            ),

            performance_level=performance_level
        )

        db.add(result)

        db.commit()

        db.refresh(result)

        # ===================================
        # RETURN RESPONSE
        # ===================================

        return {

            "message":

            "Exam submitted successfully",

            "result": {

                "score":
                score,

                "total_questions":
                total_questions,

                "percentage":
                percentage,

                "performance_level":
                performance_level,

                "weak_topics":
                weak_topics
            }
        }

    except Exception as e:

        return {

            "error":

            str(e)
        }