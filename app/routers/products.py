from fastapi import APIRouter, HTTPException, Depends, Query, Form, UploadFile, File, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import Product, User, Category
from app.schemas import ProductCreate, ProductResponse, ProductPaginatedResponse, ProductUpdateInput
from app.auth import get_current_user
from typing import List, Optional
from sqlalchemy.sql import func
from datetime import datetime
import os
from pathlib import Path
import shutil
from math import ceil
from pydantic import ValidationError

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("/", response_model=ProductResponse)
def create_product(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    sales: int = Form(0),
    image: Optional[UploadFile] = File(None), 
    code: Optional[str] = Form(None),
    category_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category_id_int = int(category_id) if category_id else None
    existing_product = db.query(Product).filter(Product.code == code).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product code already exists")

    file_path = None

    if image:
        upload_folder = "uploads/product_images"
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, image.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        sales=sales,
        image=file_path,  
        code=code,
        category_id=category_id_int,
        user_id=current_user.id,
    )

    try:
        ProductResponse.from_orm(new_product)  
    except ValidationError as e:
        raise e
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


@router.get("/", response_model=ProductPaginatedResponse)
def get_products(
    request: Request,
    category: Optional[str] = None,
    low_stock_threshold: Optional[int] = Query(None, description="Filter products with stock below this threshold"),
    search: Optional[str] = Query(None, description="Search products by name or description"),
    order_by: Optional[str] = Query(None, description="Order by a specific field: name, price, stock, or category"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page (max 100)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product).filter(Product.user_id == current_user.id)
    
    if category:
        query = query.filter(Product.category.has(id=category))
    
    if low_stock_threshold is not None:
        query = query.filter(Product.stock < low_stock_threshold)
    
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )
    
    if order_by in ["name", "price", "stock", "category", "sales", "code", 'description']:
        order_function = Product.__table__.columns.get(order_by)
        if order_function is not None:
            if order == "desc":
                query = query.order_by(order_function.desc())
            else:
                query = query.order_by(order_function.asc())

    total_items = query.count()
    total_pages = ceil(total_items / page_size)
    offset = (page - 1) * page_size
    paginated_query = query.offset(offset).limit(page_size)
    
    products = paginated_query.all()

    base_url = request.base_url
    for product in products:
        if product.image:
            normalized_path = product.image.replace("\\", "/")
            product.image = f"{base_url}uploads/{normalized_path.split('uploads/')[-1]}"

    serialized_products = [ProductResponse.from_orm(product) for product in products]

    return ProductPaginatedResponse(
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        total_items=total_items,
        products=serialized_products,
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    request: Request,
    product_id: int,
    product: ProductUpdateInput = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = db.query(Product).filter(
        Product.id == product_id, Product.user_id == current_user.id
    ).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.image:
        UPLOAD_DIR = "uploads/product_images"
        Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

        image_path = Path(UPLOAD_DIR) / product.image.filename
        with open(image_path, "wb") as f:
            f.write(await product.image.read())

        base_url = str(request.base_url).rstrip("/")
        db_product.image = f"{base_url}/{UPLOAD_DIR}/{product.image.filename}"

    if product.name:
        db_product.name = product.name
    if product.description:
        db_product.description = product.description
    if product.price:
        db_product.price = product.price
    if product.stock:
        db_product.stock = product.stock
    if product.sales:
        db_product.sales = product.sales
    if product.code:
        db_product.code = product.code
    if product.category_id:
        db_product.category_id = product.category_id
    
    try:
        ProductResponse.from_orm(db_product)  
    except ValidationError as e:
        raise 

    db.commit()
    db.refresh(db_product)

    return db_product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return
