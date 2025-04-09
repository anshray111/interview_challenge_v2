from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
import csv
import io
from typing import Optional, List
from pydantic import BaseModel

from db.database import get_db
from db.models import Business, Symptom, BusinessSymptom

router = APIRouter()


class SymptomResponse(BaseModel):
    business_id: int
    business_name: str
    symptom_code: str
    symptom_name: str
    symptom_diagnostic: bool

    class Config:
        orm_mode = True


@router.get('/status')
async def get_status():
    try:
        return {"status": "Health OK"}
    except Exception as e:
        return {'Error': str(e)}


@router.get('/symptoms', response_model=List[SymptomResponse])
async def get_symptoms(
    business_id: Optional[int] = None,
    diagnostic: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get business and symptom data with optional filtering by business_id and diagnostic value
    """
    query = (
        db.query(
            Business.id.label('business_id'),
            Business.name.label('business_name'),
            Symptom.code.label('symptom_code'),
            Symptom.name.label('symptom_name'),
            BusinessSymptom.diagnostic.label('symptom_diagnostic')
        )
        .join(BusinessSymptom, Business.id == BusinessSymptom.business_id)
        .join(Symptom, Symptom.code == BusinessSymptom.symptom_code)
    )
    
    if business_id is not None:
        query = query.filter(Business.id == business_id)
    
    if diagnostic is not None:
        query = query.filter(BusinessSymptom.diagnostic == diagnostic)
    
    results = query.all()
    
    return [
        SymptomResponse(
            business_id=row.business_id,
            business_name=row.business_name,
            symptom_code=row.symptom_code,
            symptom_name=row.symptom_name,
            symptom_diagnostic=row.symptom_diagnostic
        )
        for row in results
    ]


@router.post('/import-csv')
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Import CSV data into the database
    """
    
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    content = await file.read()
    csv_data = io.StringIO(content.decode('utf-8'))
    csv_reader = csv.DictReader(csv_data)
    
    # Track businesses and symptoms that have been added
    processed_businesses = set()
    processed_symptoms = set()
    
    for row in csv_reader:
        business_id = int(row['Business ID'])
        business_name = row['Business Name']
        symptom_code = row['Symptom Code']
        symptom_name = row['Symptom Name']
        
        # Convert various forms of true/false to boolean
        symptom_diagnostic_str = row['Symptom Diagnostic'].lower()
        symptom_diagnostic = (
            symptom_diagnostic_str == 'true' or 
            symptom_diagnostic_str == 'yes'
        )
        
        # Add business if not already in database
        if business_id not in processed_businesses:
            existing_business = db.query(Business).filter(Business.id == business_id).first()
            if not existing_business:
                business = Business(id=business_id, name=business_name)
                db.add(business)
                db.flush()
            processed_businesses.add(business_id)
        
        # Add symptom if not already in database
        if symptom_code not in processed_symptoms:
            existing_symptom = db.query(Symptom).filter(Symptom.code == symptom_code).first()
            if not existing_symptom:
                symptom = Symptom(code=symptom_code, name=symptom_name)
                db.add(symptom)
                db.flush()
            processed_symptoms.add(symptom_code)
        
        # Add business-symptom relationship
        existing_relation = (
            db.query(BusinessSymptom)
            .filter(
                BusinessSymptom.business_id == business_id,
                BusinessSymptom.symptom_code == symptom_code
            )
            .first()
        )
        
        if not existing_relation:
            business_symptom = BusinessSymptom(
                business_id=business_id,
                symptom_code=symptom_code,
                diagnostic=symptom_diagnostic
            )
            db.add(business_symptom)
    
    db.commit()
    
    return {"message": "CSV data imported successfully"}