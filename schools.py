from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import School
from schemas import SchoolCreate, SchoolUpdate

router = APIRouter(prefix="/schools", tags=["Schools"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Register a school
@router.post("/")
def register_school(school: SchoolCreate, db: Session = Depends(get_db)):
    existing = db.query(School).filter(School.email == school.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="School already exists")

    new_school = School(
        name=school.name,
        email=school.email,
        phone=school.phone,
        location=school.location,
        description=school.description,
    )
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return {
        "message": "School registered successfully", 
        "school": {
            "id": new_school.id,
            "name": new_school.name,
            "email": new_school.email,
            "phone": new_school.phone,
            "location": new_school.location
        }
    }


# 2. Get all schools
@router.get("/")
def get_schools(db: Session = Depends(get_db)):
    schools = db.query(School).all()
    return {"schools": [{"id": s.id, "name": s.name, "email": s.email, "phone": s.phone, "location": s.location} for s in schools]}


# 3. Get school by ID
@router.get("/{school_id}")
def get_school(school_id: int, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return {"id": school.id, "name": school.name, "email": school.email, "phone": school.phone, "location": school.location}


# 4. Update school profile
@router.put("/{school_id}")
def update_school(school_id: int, data: SchoolUpdate, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(school, key, value)

    db.commit()
    db.refresh(school)
    return {
        "message": "School updated successfully", 
        "school": {
            "id": school.id,
            "name": school.name,
            "email": school.email,
            "phone": school.phone,
            "location": school.location
        }
    }
