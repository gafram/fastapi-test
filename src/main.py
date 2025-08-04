import sqlite3

from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, Query, Depends
from typing import List, Annotated, Literal, Generator

POSITIVE = ["хорош", "люблю"]
NEGATIVE = ["плох", "ненавиж"]
DATABASE_PATH = "./reviews.db"

app = FastAPI()

class Review(BaseModel):
    text: str

class ProcessedReview(Review):
    id: int
    sentiment: str
    created_at: str

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def get_sentiment(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in POSITIVE):
        return "positive"
    elif any(word in lowered for word in NEGATIVE):
        return "negative"
    return "neutral"

@app.post("/reviews", response_model=ProcessedReview)
def post_review(
    review: Review,
    session: sqlite3.Connection = Depends(get_db)
):
    """
    Adds a new review to the database.

    Args:
        review: Review payload containing the text.
        session: Injected database connection.

    Returns:
        ProcessedReview: The stored review with ID, sentiment, and creation timestamp.
    """
    sentiment = get_sentiment(review.text)
    created_at = datetime.utcnow().isoformat()

    cursor = session.cursor()
    cursor.execute(
        "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
        (review.text, sentiment, created_at)
    )
    session.commit()
    review_id = cursor.lastrowid

    return ProcessedReview(
        id=review_id,
        text=review.text,
        sentiment=sentiment,
        created_at=created_at
    )

@app.get("/reviews", response_model=List[ProcessedReview])
def get_reviews(
    sentiment: Annotated[Literal["negative"], Query(...)],
    session: sqlite3.Connection = Depends(get_db)
):
    """
    Retrieves reviews from the database filtered by sentiment.

    Args:
        sentiment: The sentiment to filter by(currently only “negative”).
        session: Injected database connection.

    Returns:
        List[ProcessedReview]: A list of matching reviews.
    """
    cursor = session.cursor()
    cursor.execute(
        "SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ?",
        (sentiment,)
    )
    rows = cursor.fetchall()
    return [ProcessedReview(id=id, text=text, sentiment=sentiment, created_at=created_at) for id, text, sentiment, created_at in rows]

init_db()