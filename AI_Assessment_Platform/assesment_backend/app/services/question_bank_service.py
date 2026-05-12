from app.models import Question

# -----------------------------------
# SAVE GENERATED QUESTIONS
# -----------------------------------

def save_generated_questions(

    db,

    questions,

    teacher_email
):

    saved_questions = []

    for question_data in questions:

        # -----------------------------------
        # OPTIONS
        # -----------------------------------

        options = question_data.get(
            "options",
            []
        )

        # -----------------------------------
        # DATABASE OBJECT
        # -----------------------------------

        db_question = Question(

            question=question_data.get(
                "question"
            ),

            option_a=options[0]
            if len(options) > 0 else "",

            option_b=options[1]
            if len(options) > 1 else "",

            option_c=options[2]
            if len(options) > 2 else "",

            option_d=options[3]
            if len(options) > 3 else "",

            correct_answer=question_data.get(
                "correct_answer"
            ),

            difficulty=question_data.get(
                "difficulty"
            ),

            topic=question_data.get(
                "topic"
            ),

            created_by=teacher_email
        )

        # -----------------------------------
        # ADD TO DATABASE
        # -----------------------------------

        db.add(db_question)

        saved_questions.append(
            db_question
        )

    # -----------------------------------
    # SAVE CHANGES
    # -----------------------------------

    db.commit()

    return saved_questions