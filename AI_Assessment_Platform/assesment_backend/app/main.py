from fastapi import FastAPI

from app.database import engine
from app.models import Base

# ===================================
# IMPORT ROUTERS
# ===================================

from app.routes.auth import (
    router as auth_router
)

from app.routes.questions import (
    router as question_router
)

from app.routes.exams import (
    router as exam_router
)

from app.routes.analytics import (
    router as analytics_router
)

from app.routes.exam_management import (
    router as exam_management_router
)

from app.routes.exam_assembly import (
    router as exam_assembly_router
)

from app.routes.exam_delivery import (
    router as exam_delivery_router
)

from app.routes.results import (
    router as results_router
)

# ===================================
# CHATBOT ROUTER
# ===================================

from app.routes.chatbot import (
    router as chatbot_router
)

# ===================================
# MATERIALS ROUTER
# ===================================

from app.routes.materials import (
    router as materials_router
)

# ===================================
# CREATE DATABASE TABLES
# ===================================

Base.metadata.create_all(
    bind=engine
)

# ===================================
# FASTAPI APP
# ===================================

app = FastAPI(

    title="AI Assessment Platform API"
)

# ===================================
# INCLUDE ROUTERS
# ===================================

app.include_router(
    auth_router
)

app.include_router(
    question_router
)

app.include_router(
    exam_router
)

app.include_router(
    analytics_router
)

app.include_router(
    exam_management_router
)

app.include_router(
    exam_assembly_router
)

app.include_router(
    exam_delivery_router
)

# ===================================
# AI CHATBOT
# ===================================

app.include_router(
    chatbot_router
)

# ===================================
# MATERIAL SIMPLIFIER
# ===================================

app.include_router(
    materials_router
)

# ===================================
# RESULTS
# ===================================

app.include_router(
    results_router
)

# ===================================
# ROOT API
# ===================================

@app.get("/")

def home():

    return {

        "message":

        "AI Assessment Backend Running"
    }