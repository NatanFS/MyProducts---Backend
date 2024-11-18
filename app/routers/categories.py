from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Category, User
from app.schemas import CategoryCreate, CategoryResponse
from app.auth import get_current_user 
from typing import List

router = APIRouter(
    prefix="/products/categories",
    tags=["categories"],
)


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user), 
):
    new_category = Category(**category.dict(), user_id=current_user.id)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    
    return categories

@router.delete("/{category_id}", response_model=CategoryResponse, status_code=200)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = db.query(Category).filter(
        Category.id == category_id, Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404, detail="Category not found or not authorized to delete"
        )

    db.delete(category)
    db.commit()

    return category

