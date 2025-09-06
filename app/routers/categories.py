from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
from ..schemas.question import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    if db.query(models.Category).filter(models.Category.name == payload.name).first():
        raise HTTPException(status_code=409, detail="Category already exists")
    c = models.Category(name=payload.name)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).order_by(models.Category.name.asc()).all()

@router.put("/{cid}", response_model=CategoryResponse)
def update_category(cid: int, payload: CategoryCreate, db: Session = Depends(get_db)):
    c = db.get(models.Category, cid)
    if not c:
        raise HTTPException(status_code=404, detail="Category not found")
    # (необязательно) проверка уникальности
    conflict = db.query(models.Category).filter(models.Category.id != cid, models.Category.name == payload.name).first()
    if conflict:
        raise HTTPException(status_code=409, detail="Category with this name already exists")
    c.name = payload.name
    db.commit(); db.refresh(c)
    return c

@router.delete("/{cid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(cid: int, db: Session = Depends(get_db)):
    c = db.get(models.Category, cid)
    if not c:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(c); db.commit()
    return None
