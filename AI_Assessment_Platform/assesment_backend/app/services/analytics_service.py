from app.models import (
    Result
)

# ===================================
# GET ALL RESULTS
# ===================================

def get_all_results(db):

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
# GET ANALYTICS
# ===================================

def get_analytics(db):

    results = db.query(
        Result
    ).all()

    analytics = []

    for result in results:

        analytics.append(

            {

                "student_email":

                result.student_email,

                "exam_id":

                result.exam_id,

                "score":

                result.score,

                "percentage":

                result.percentage,

                "performance_level":

                result.performance_level
            }
        )

    return analytics

# ===================================
# GET ANALYTICS SUMMARY
# ===================================

def get_analytics_summary(db):

    results = db.query(
        Result
    ).all()

    if not results:

        return {

            "total_students": 0,

            "average_percentage": 0,

            "highest_score": 0,

            "lowest_score": 0
        }

    percentages = [

        result.percentage

        for result in results
    ]

    return {

        "total_students":

        len(results),

        "average_percentage":

        round(

            sum(percentages)

            / len(percentages),

            2
        ),

        "highest_score":

        max(percentages),

        "lowest_score":

        min(percentages)
    }