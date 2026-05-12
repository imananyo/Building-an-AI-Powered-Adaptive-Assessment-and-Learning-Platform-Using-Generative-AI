from sqlalchemy.orm import Session

from collections import defaultdict

from app.models import (
    Question,
    Result
)

from app.services.youtube_service import (
    search_youtube_video
)

# ===================================
# CALCULATE SCORE
# ===================================

def calculate_score(

    db: Session,

    student_email,

    exam_id,

    answers
):

    # ===================================
    # FETCH QUESTIONS
    # ===================================

    questions = db.query(
        Question
    ).all()

    total_questions = len(
        questions
    )

    score = 0

    weak_topics = []

    topic_correct = defaultdict(int)

    topic_total = defaultdict(int)

    # ===================================
    # CHECK ANSWERS
    # ===================================

    for question in questions:

        qid = str(question.id)

        student_answer = answers.get(
            qid
        )

        correct_answer = question.correct_answer

        topic = question.topic

        topic_total[topic] += 1

        # -----------------------------------
        # CORRECT ANSWER
        # -----------------------------------

        if student_answer == correct_answer:

            score += 1

            topic_correct[topic] += 1

        # -----------------------------------
        # WRONG ANSWER
        # -----------------------------------

        else:

            weak_topics.append(
                topic
            )

    # ===================================
    # PERCENTAGE
    # ===================================

    if total_questions == 0:

        percentage = 0

    else:

        percentage = round(

            (score / total_questions) * 100,

            2
        )

    # ===================================
    # PERFORMANCE LEVEL
    # ===================================

    if percentage >= 85:

        performance_level = "Excellent"

    elif percentage >= 70:

        performance_level = "Good"

    elif percentage >= 50:

        performance_level = "Average"

    else:

        performance_level = "Needs Improvement"

    # ===================================
    # TOPIC ANALYSIS
    # ===================================

    topic_analysis = {}

    for topic in topic_total:

        total = topic_total[topic]

        correct = topic_correct[topic]

        accuracy = round(

            (correct / total) * 100,

            2
        )

        topic_analysis[topic] = accuracy

    # ===================================
    # REMOVE DUPLICATES
    # ===================================

    weak_topics = list(
        set(weak_topics)
    )

    # ===================================
    # DYNAMIC YOUTUBE RECOMMENDATIONS
    # ===================================

    recommended_videos = []

    added_topics = set()

    for topic in weak_topics:

        if topic not in added_topics:

            video = search_youtube_video(
                topic
            )

            if video:

                recommended_videos.append(
                    video
                )

                added_topics.add(
                    topic
                )

    # ===================================
    # SAVE RESULT
    # ===================================

    result = Result(

        student_email=student_email,

        exam_id=exam_id,

        score=score,

        percentage=percentage,

        performance_level=performance_level
    )

    db.add(result)

    db.commit()

    # ===================================
    # RETURN RESULT
    # ===================================

    return {

        "score": score,

        "total_questions": total_questions,

        "percentage": percentage,

        "performance_level": performance_level,

        "weak_topics": weak_topics,

        "topic_analysis": topic_analysis,

        "recommended_videos":

        recommended_videos
    }