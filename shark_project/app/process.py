# app/process.py
import pydicom
import logging

from fastapi import HTTPException


def extract_metadata(file_path: str):
    try:
        dicom = pydicom.dcmread(file_path)
        logging.info(f"DICOM metadata: {dicom}")
        return {
            "patient_name": str(dicom.get("PatientName", "Unknown")),
            "modality": str(dicom.get("Modality", "Unknown")),
            "study_date": str(dicom.get("StudyDate", "Unknown")),
        }
    except Exception as e:
        logging.error(f"Error reading DICOM file: {e}")
        raise HTTPException(status_code=500, detail="Error reading DICOM file")
