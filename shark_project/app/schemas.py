from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base DICOM schema
class DICOMBase(BaseModel):
    filename: str
    patient_name: str
    modality: str
    study_date: str  # Change to `datetime` if you want to handle it as a date

# DICOM creation schema
class DICOMCreate(DICOMBase):
    owner_id: int  # Foreign key to the user who owns the DICOM file

# DICOM schema with ID and timestamp
class DICOM(DICOMBase):
    id: int
    uploaded_at: datetime  # Ensure `uploaded_at` is a datetime field

    class Config:
        orm_mode = True


# User creation schema with optional fields
class UserCreate(BaseModel):
    email: str
    username: str
    first_name: Optional[str] = None  # Make `first_name` optional
    last_name: Optional[str] = None   # Make `last_name` optional
    password: str

# User schema with optional `first_name` and `last_name`, and default `is_active` field
class User(BaseModel):
    id: int
    email: str
    username: str
    first_name: Optional[str] = None  # Make `first_name` optional
    last_name: Optional[str] = None   # Make `last_name` optional
    is_active: bool = True  # Default value is True

    class Config:
        orm_mode = True


# Login schema with username and password
class Login(BaseModel):
    username: str
    password: str
