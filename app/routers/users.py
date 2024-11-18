from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from app import schemas, models, database, auth
from fastapi.security import OAuth2PasswordRequestForm
from app.database import engine, get_db
from sqlalchemy.orm import sessionmaker
from app.schemas import UserCreate
import shutil
import os
from pydantic import ValidationError

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=schemas.UserBase)
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        validated_user = UserCreate(
            name=name,
            email=email,
            password=password,
            profile_image=profile_image
        )
    except ValidationError:
        raise 

    db_user = db.query(models.User).filter(models.User.email == validated_user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    upload_folder = "uploads/profile_images"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, profile_image.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)
    
    hashed_password = auth.get_password_hash(validated_user.password)
    
    new_user = models.User(
        name=validated_user.name,
        email=validated_user.email,
        profile_image=file_path,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
    
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user