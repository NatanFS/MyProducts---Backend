from pydantic import BaseModel, Field, PositiveInt, PositiveFloat, constr, EmailStr, field_validator, FieldValidationInfo
from typing import Optional, List
from datetime import datetime, date
from fastapi import Form,  UploadFile

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Name must be between 3 and 50 characters")
    email: EmailStr = Field(..., description="A valid email address")
    profile_image: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Name must be between 3 and 50 characters")
    password: str = Field(..., min_length=6, max_length=100, description="Password must be between 6 and 100 characters")
    email: EmailStr = Field(..., description="A valid email address")

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str


class SalesSummary(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    total_sales: int = Field(..., ge=0, description="Total sales must be a non-negative integer")
    total_revenue: float = Field(..., ge=0.0, description="Total revenue must be a non-negative number")


class ProductsByCategory(BaseModel):
    category: str
    product_count: int = Field(..., ge=0, description="Product count must be a non-negative integer")


class LowStockProduct(BaseModel):
    id: int
    name: str
    stock: int = Field(..., ge=0, description="Stock must be a non-negative integer")
    category: str

# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Category name must be between 3 and 50 characters")
    description: Optional[str] = Field(None, max_length=200, description="Description must not exceed 200 characters")


class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Product name should have 3–100 characters.",
        example="Wireless Mouse",
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Brief product description (max 500 characters).",
        example="A high-precision wireless mouse.",
    )
    price: PositiveFloat = Field(
        ...,
        description="Product price must be a positive number.",
        example=29.99,
    )
    stock: PositiveInt = Field(
        ...,
        description="Number of items in stock (must be greater than 0).",
        example=150,
    )
    sales: int = Field(
        0,
        ge=0,
        description="Total number of items sold (must not be negative).",
        example=25,
    )
    image: Optional[str] = Field(
        None,
        description="URL for product image.",
        example="https://example.com/image.jpg",
    )
    code: str = Field(
        ...,
        max_length=50,
        description="Unique product code or SKU (max 50 characters).",
        example="PROD-001-WM",
    )
    category_id: Optional[int] = Field(
        ...,
        description="ID of the category this product belongs to.",
        example=5,
    )
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("name")
    def validate_name(cls, value: str, info: FieldValidationInfo) -> str:
        if len(value) < 3:
            raise ValueError("Product name must have at least 3 characters.")
        if len(value) > 100:
            raise ValueError("Product name must not exceed 100 characters.")
        return value
    
class ProductUpdateInput:
    def __init__(
        self,
        name: str = Form(
            ...,
            min_length=3,
            max_length=100,
            description="Product name should have 3–100 characters.",
            example="Wireless Mouse",
        ),
        description: Optional[str] = Form(
            None,
            max_length=500,
            description="Brief product description (max 500 characters).",
            example="A high-precision wireless mouse.",
        ),
        price: PositiveFloat = Form(
            ...,
            description="Product price must be a positive number.",
            example=29.99,
        ),
        stock: PositiveInt = Form(
            ...,
            description="Number of items in stock (must be greater than 0).",
            example=150,
        ),
        sales: int = Form(
            0,
            ge=0,
            description="Total number of items sold (must not be negative).",
            example=25,
        ),
        image: Optional[UploadFile] = Form(
            None,
            description="File upload for product image.",
        ),
        code: Optional[str] = Form(
            ...,
            max_length=50,
            description="Unique product code or SKU (max 50 characters).",
            example="PROD-001-WM",
        ),
        category_id: Optional[int] = Form(
            None,
            description="ID of the category this product belongs to.",
            example=5,
        ),
    ):
        
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.sales = sales
        self.image = image
        self.code = code
        self.category_id = category_id
    
class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: Optional[int]
    category: Optional[CategoryResponse]

    class Config:
        orm_mode = True
        from_attributes = True
        

class ProductPaginatedResponse(BaseModel):
    page: int
    page_size: int
    total_pages: int
    total_items: int
    products: List[ProductResponse]


class MostSoldProduct(BaseModel):
    id: int
    name: str
    total_sold: int

    class Config:
        orm_mode = True

class MostSoldCategory(BaseModel):
    category: Optional[str] 
    total_sold: int

    class Config:
        orm_mode = True

class DashboardMetrics(BaseModel):
    total_products: int
    low_stock_products: int
    total_stock_value: float
    total_sales: int
    total_revenue: float
    start_date: Optional[date]
    end_date: Optional[date]

    class Config:
        orm_mode = True

class ProductCreateRequest(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int
    sales: Optional[int] = 0
    code: str
    category_id: Optional[int]
    fake_created_at: Optional[datetime] = Field(None, description="Manually set the created_at timestamp")
