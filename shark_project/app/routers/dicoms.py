# app/routers/dicoms.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import shutil, os
from app.db import SessionLocal
from app.schemas import DICOM, DICOMCreate, User
from app.process import extract_metadata
import app.crud as crud
from app.routers.auth import get_current_user
from fastapi.responses import FileResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Secure upload DICOM route
@router.post("/upload", response_model=DICOM)
async def upload_dicom(file: UploadFile = File(...), db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    os.makedirs("app/temp_files", exist_ok=True)
    file_path = f"app/temp_files/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract metadata from the DICOM file
    metadata = extract_metadata(file_path)
    # Prepare data to save, including the user who is uploading the file
    data = DICOMCreate(
        filename=file.filename,
        patient_name=metadata["patient_name"],
        modality=metadata["modality"],
        study_date=metadata["study_date"],
        owner_id=current_user.id  # Associate the DICOM file with the current user
    )

    # Create new DICOM entry in the DB
    return crud.create_dicom(db, data)

# Secure get all dicoms route
@router.get("/dicoms", response_model=list[DICOM])
def list_dicoms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Fetch DICOM files for the current user only
    return crud.get_dicoms_by_user(db, user_id=current_user.id)

# Secure get dicom by id route
@router.get("/dicoms/{dicom_id}", response_model=DICOM)
def get_dicom(dicom_id: int, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    dicom = crud.get_dicom_by_id(db, dicom_id)

    # Check if the DICOM belongs to the current user
    if dicom is None or dicom.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="DICOM not found or not owned by the current user")

    return dicom

# Secure delete dicom route
@router.delete("/dicoms/{dicom_id}")
def delete_dicom(dicom_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    dicom = crud.get_dicom_by_id(db, dicom_id)

    # Check if the DICOM belongs to the current user before deleting
    if dicom is None or dicom.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="DICOM not found or not owned by the current user")

    # Delete the file if it exists
    file_path = f"app/temp_files/{dicom.filename}"
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            raise HTTPException(status_code=500, detail="Failed to delete file")

    # Proceed to delete DB record
    crud.delete_dicom(db, dicom_id)
    return {"message": "Deleted successfully"}

@router.get("/dicoms/{dicom_id}/download")
def download_dicom(dicom_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    dicom = crud.get_dicom_by_id(db, dicom_id)
    if dicom is None or dicom.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="DICOM not found or not owned by the current user")
    file_path = f"app/temp_files/{dicom.filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(file_path, filename=dicom.filename, media_type="application/dicom")