from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from app import schemas, models, database, auth
from fastapi.security import OAuth2PasswordRequestForm
from app.database import engine, get_db
from sqlalchemy.orm import sessionmaker
import os
from pydantic import ValidationError
from app.supabase import create_client, SUPABASE_URL, SUPABASE_KEY
from dotenv import load_dotenv
import uuid

load_dotenv()
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=schemas.UserBase)
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        validated_user = schemas.UserCreate(
            name=name,
            email=email,
            password=password,
            profile_image=profile_image.filename
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid user data")

    db_user = db.query(models.User).filter(models.User.email == validated_user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    bucket_name = "profile_images"
    unique_id = uuid.uuid4().hex
    file_extension = profile_image.filename.split(".")[-1]
    file_name = f"{validated_user.email}_{unique_id}.{file_extension}"
    
    file_content = await profile_image.read() 

    response = supabase.storage.from_(bucket_name).upload(file_name, file_content)
    if not response.path:  
        raise HTTPException(status_code=500, detail=f"Failed to upload profile image: {response.error.message}")

    profile_image_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{file_name}"

    hashed_password = auth.get_password_hash(validated_user.password)
    
    new_user = models.User(
        name=validated_user.name,
        email=validated_user.email,
        profile_image=profile_image_url,
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