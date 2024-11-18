from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schemas, models, auth
from app.database import get_db
from datetime import datetime, date, time, timedelta
from typing import List, Optional
from app.models import Product


router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)

from sqlalchemy.sql import func
from typing import Optional
from datetime import datetime, date, time

@router.get("/dashboard_metrics", response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Fetch metrics for the dashboard, including sales summary.
    """
    query = db.query(models.Product).filter(models.Product.user_id == current_user.id)

    if start_date:
        start_datetime = datetime.combine(start_date, time.min)
        query = query.filter(models.Product.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, time.max)
        query = query.filter(models.Product.created_at <= end_datetime)

    total_products = query.count()

    low_stock_products = query.filter(models.Product.stock <= 10).count()

    total_stock_value = query.with_entities(func.sum(models.Product.stock * models.Product.price)).scalar() or 0

    total_sales = query.with_entities(func.sum(models.Product.sales)).scalar() or 0

    total_revenue = query.with_entities(func.sum(models.Product.sales * models.Product.price)).scalar() or 0

    return schemas.DashboardMetrics(
        total_products=total_products,
        low_stock_products=low_stock_products,
        total_stock_value=total_stock_value,
        total_sales=total_sales,
        total_revenue=total_revenue,
        start_date=start_date,
        end_date=end_date,
    )

@router.get("/products_by_category", response_model=List[schemas.ProductsByCategory])
def products_by_category(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Get a breakdown of the number of products by category within a date range.
    """
    query = db.query(models.Category.name.label("category_name"), func.count(models.Product.id).label("product_count")).join(
        models.Product, models.Category.id == models.Product.category_id
    ).filter(models.Product.user_id == current_user.id)

    if start_date:
        start_datetime = datetime.combine(start_date, time.min)
        query = query.filter(models.Product.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, time.max)
        query = query.filter(models.Product.created_at <= end_datetime)

    results = query.group_by(models.Category.name).all()

    return [
        schemas.ProductsByCategory(category=r.category_name, product_count=r.product_count)
        for r in results
    ]


@router.get("/most_sold_products", response_model=List[schemas.MostSoldProduct])
def most_sold_products(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(10, description="Number of top products to return"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Get a list of the most sold products within a date range.
    """
    query = db.query(
        models.Product.id,
        models.Product.name,
        func.sum(models.Product.sales).label("total_sold"),
    ).filter(models.Product.user_id == current_user.id)

    if start_date:
        start_datetime = datetime.combine(start_date, time.min)
        query = query.filter(models.Product.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, time.max)
        query = query.filter(models.Product.created_at <= end_datetime)

    results = query.group_by(models.Product.id, models.Product.name).order_by(
        func.sum(models.Product.sales).desc()
    ).limit(limit).all()

    return [
        schemas.MostSoldProduct(
            id=r.id,
            name=r.name,
            total_sold=r.total_sold,
        )
        for r in results
    ]


@router.get("/most_sold_categories", response_model=List[schemas.MostSoldCategory])
def most_sold_categories(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(10, description="Number of top categories to return"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Get a list of the most sold categories within a date range.
    """
    query = db.query(
        models.Category.name.label("category_name"),
        func.sum(models.Product.sales).label("total_sold"),
    ).join(models.Product, models.Category.id == models.Product.category_id).filter(
        models.Product.user_id == current_user.id
    )

    if start_date:
        start_datetime = datetime.combine(start_date, time.min)
        query = query.filter(models.Product.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, time.max)
        query = query.filter(models.Product.created_at <= end_datetime)

    results = query.group_by(models.Category.name).order_by(
        func.sum(models.Product.sales).desc()
    ).limit(limit).all()

    return [
        schemas.MostSoldCategory(
            category=r.category_name,
            total_sold=r.total_sold,
        )
        for r in results
    ]

@router.get("/sales_over_time")
def sales_over_time(
    start_date: str = None,
    end_date: str = None, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
    ):
    if not start_date:
        start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
    if not end_date:
        end_date = datetime.utcnow().isoformat()
    
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    
    data = db.query(
        func.date(Product.created_at).label("date"),
        func.sum(Product.sales).label("total_sales")
    ).filter(
        Product.created_at >= start_date, 
        Product.created_at <= end_date,
        current_user.id == Product.user_id,
    ).group_by(
        func.date(Product.created_at)
    ).order_by(
        func.date(Product.created_at)
    ).all()
    
    return [{"date": record.date, "total_sales": record.total_sales} for record in data]