from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from ..db import get_db
from .. import models
from ..schemas.question import QuestionCreate, QuestionResponse

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("", response_model=list[QuestionResponse])
def list_questions(
    db: Session = Depends(get_db),
    category_id: int | None = Query(default=None),
):
    q = db.query(models.Question).options(joinedload(models.Question.category)).order_by(models.Question.id.desc())
    if category_id is not None:
        q = q.filter(models.Question.category_id == category_id)
    return q.all()

@router.post("", response_model=QuestionResponse, status_code=201)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    if payload.category_id is not None and not db.get(models.Category, payload.category_id):
        raise HTTPException(status_code=404, detail="category_id not found")
    q = models.Question(text=payload.text, answer=payload.answer, category_id=payload.category_id)
    db.add(q); db.commit(); db.refresh(q)
    # чтобы в ответе была категория
    db.refresh(q, attribute_names=["category"])
    return q
