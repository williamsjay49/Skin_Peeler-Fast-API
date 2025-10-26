from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class DICOMMetadata(Base):
    __tablename__ = "dicom_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    patient_name = Column(String)
    modality = Column(String)
    study_date = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Foreign key to link the DICOM file to the User (owner)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Define relationship back to User
    owner = relationship("User", back_populates="dicoms")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Relationship with DICOM files
    dicoms = relationship("DICOMMetadata", back_populates="owner")
