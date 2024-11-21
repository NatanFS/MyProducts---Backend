from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from app.database import engine
from app import models
from app.routers import users, reports, products, categories
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
import uvicorn
import os 

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MyProducts API",
    description="API to manage inventory",
    version="1.0.0"
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = "https://my-products-frontend.vercel.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = [
        {"field": ".".join(str(loc) for loc in error["loc"][1:]), "message": error["msg"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"errors": errors},
    )

@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request, exc):
    errors = [
        {
            "field": ".".join(str(loc) for loc in error["loc"][1:]),
            "message": error["msg"]
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error validating response",
            "errors": errors,
        }
    )

@app.exception_handler(ValidationError)
async def response_validation_exception_handler(request, exc: ValidationError):
    errors = [
        {
            "field": ".".join(map(str, error["loc"])),  
            "message": error["msg"],
            "type": error["type"] 
        }
        for error in exc.errors()
    ]
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error validating request",
            "errors": errors,
        }
    )

app.include_router(users.router)
app.include_router(reports.router)
app.include_router(products.router)
app.include_router(categories.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

