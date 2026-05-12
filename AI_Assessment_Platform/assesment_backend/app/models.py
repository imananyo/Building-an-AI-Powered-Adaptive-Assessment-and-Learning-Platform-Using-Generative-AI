from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Text
)

from sqlalchemy.ext.declarative import (
    declarative_base
)

from sqlalchemy.orm import relationship

# ===================================
# BASE
# ===================================

Base = declarative_base()

# ===================================
# USER TABLE
# ===================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String
    )

    email = Column(
        String,
        unique=True
    )

    password = Column(
        String
    )

    role = Column(
        String
    )

# ===================================
# QUESTION TABLE
# ===================================

class Question(Base):

    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text
    )

    option_a = Column(
        String
    )

    option_b = Column(
        String
    )

    option_c = Column(
        String
    )

    option_d = Column(
        String
    )

    correct_answer = Column(
        String
    )

    difficulty = Column(
        String
    )

    topic = Column(
        String
    )

    created_by = Column(
        String
    )

# ===================================
# EXAM TABLE
# ===================================

class Exam(Base):

    __tablename__ = "exams"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String
    )

    description = Column(
        Text
    )

    duration_minutes = Column(
        Integer
    )

# ===================================
# EXAM QUESTION MAPPING
# ===================================

class ExamQuestion(Base):

    __tablename__ = "exam_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    exam_id = Column(
        Integer,
        ForeignKey("exams.id")
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id")
    )

# ===================================
# STUDENT SUBMISSION
# ===================================

class StudentSubmission(Base):

    __tablename__ = "student_submissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_email = Column(
        String
    )

    exam_id = Column(
        Integer
    )

    question_id = Column(
        Integer
    )

    selected_answer = Column(
        String
    )

# ===================================
# RESULT TABLE
# ===================================

class Result(Base):

    __tablename__ = "results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_email = Column(
        String
    )

    exam_id = Column(
        Integer
    )

    score = Column(
        Integer
    )

    total_questions = Column(
        Integer
    )

    percentage = Column(
        Float
    )

    weak_topics = Column(
        Text
    )

    performance_level = Column(
        String
    )

# ===================================
# STUDY MATERIAL TABLE
# ===================================

class StudyMaterial(Base):

    __tablename__ = "study_materials"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String
    )

    filename = Column(
        String
    )

    extracted_text = Column(
        Text
    )

    simplified_notes = Column(
        Text
    )