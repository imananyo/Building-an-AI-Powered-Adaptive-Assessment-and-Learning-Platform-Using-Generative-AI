from app.models import ExamQuestion
from app.models import Question

# -----------------------------------
# FETCH EXAM FOR STUDENT
# -----------------------------------

def get_exam_for_student(

    db,

    exam_id
):

    mappings = db.query(
        ExamQuestion
    ).filter(

        ExamQuestion.exam_id == exam_id
    ).all()

    questions = []

    for mapping in mappings:

        question = db.query(
            Question
        ).filter(

            Question.id == mapping.question_id
        ).first()

        if question:

            questions.append({

                "id": question.id,

                "question": question.question,

                "options": [

                    question.option_a,

                    question.option_b,

                    question.option_c,

                    question.option_d
                ]
            })

    return questions