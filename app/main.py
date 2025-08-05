from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, summarize, theme_engine
from .database import SessionLocal, engine, Base
from typing import Optional, Dict
from fastapi.routing import APIRouter

router = APIRouter()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Feedback Summarizer API")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/feedback", response_model=schemas.FeedbackOut)
def add_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    if not feedback.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")
    return crud.create_feedback(db, feedback)


@app.get("/feedback/themes")
def get_themes(db: Session = Depends(get_db)):
    feedbacks = crud.get_all_feedback(db)
    comments = [fb.comment for fb in feedbacks]
    theme_map = theme_engine.group_feedback_by_theme(comments)

    summaries = []
    for theme, theme_comments in theme_map.items():
        summary = summarize.summarize_comments(theme, theme_comments)
        summaries.append({"name": theme, "summary": summary})
    return {"themes": summaries}


@app.get("/feedback/stats")
def get_feedback_stats(db: Session = Depends(get_db)) -> Dict:
    """
    Returns overall stats from the feedback:
    - Total number of feedback entries
    - Most common theme
    - Negative sentiment ratio per theme
    """
    feedbacks = crud.get_all_feedback(db)
    comments = [fb.comment for fb in feedbacks]
    total_feedback = len(comments)

    # Group feedback by theme using embedding-based or fallback grouping
    grouped: Dict[str, list] = (
        theme_engine.group_feedback_by_theme(comments) if comments else {}
    )

    # Most common theme based on count
    most_common_theme: Optional[str] = (
        max(grouped.items(), key=lambda item: len(item[1]))[0] if grouped else None
    )

    # Negative theme ratios, e.g. {"Staff & Service": 0.4}
    negative_theme_ratios: Dict[str, float] = (
        theme_engine.get_negative_theme_ratio(comments) if comments else {}
    )

    return {
        "total_feedback": total_feedback,
        "most_common_theme": most_common_theme,
        "negative_theme_ratio": negative_theme_ratios,
    }
