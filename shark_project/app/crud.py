# app/crud.py
from sqlalchemy.orm import Session
from app.models import DICOMMetadata, User
from app.schemas import DICOMCreate, UserCreate
from passlib.context import CryptContext

def create_dicom(db: Session, data: DICOMCreate):
    record = DICOMMetadata(**data.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_all_dicoms(db: Session):
    return db.query(DICOMMetadata).all()

def get_dicom_by_id(db: Session, dicom_id: int):
    return db.query(DICOMMetadata).filter(DICOMMetadata.id == dicom_id).first()

def delete_dicom(db: Session, dicom_id: int):
    record = get_dicom_by_id(db, dicom_id)
    if record:
        db.delete(record)
        db.commit()
    return record

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CRUD operation for creating a user
def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CRUD operation for getting a user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# CRUD operation for getting a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Get all DICOM files for a user
def get_dicoms_by_user(db: Session, user_id: int):
    return db.query(DICOMMetadata).filter(DICOMMetadata.owner_id == user_id).all()