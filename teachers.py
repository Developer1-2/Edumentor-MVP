from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Teacher
from schemas import TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/teachers", tags=["Teachers"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Create teacher profile
@router.post("/")
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    new_teacher = Teacher(
        subject=teacher.subject,
        bio=teacher.bio,
        location=teacher.location,
        phone=getattr(teacher, 'phone', None),
        experience_years=getattr(teacher, 'experience_years', None),
        user_id=getattr(teacher, 'user_id', None)
    )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return {
        "message": "Teacher profile created",
        "teacher": {
            "id": new_teacher.id,
            "subject": new_teacher.subject,
            "bio": new_teacher.bio,
            "location": new_teacher.location
        }
    }


# 2. Get all teachers (active only)
@router.get("/")
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all()
    result = []
    for t in teachers:
        # Try to include related user name and active status if available
        name = None
        verified = False
        try:
            if hasattr(t, 'user') and t.user:
                name = t.user.name
                verified = bool(getattr(t.user, 'active', False))
        except Exception:
            name = None

        result.append({
            "id": t.id,
            "name": name or f"Teacher #{t.id}",
            "subject": t.subject,
            "bio": t.bio,
            "location": t.location,
            "phone": getattr(t, 'phone', None),
            "experience": getattr(t, 'experience_years', None),
            "verified": verified
        })

    return {"teachers": result}


# 3. Get teacher by ID
@router.get("/{teacher_id}")
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {
        "id": teacher.id,
        "subject": teacher.subject,
        "bio": teacher.bio,
        "location": teacher.location,
        "phone": getattr(teacher, 'phone', None),
        "experience": getattr(teacher, 'experience_years', None)
    }


# 5. Get teacher by linked user id
@router.get("/by_user/{user_id}")
def get_teacher_by_user(user_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found for user")
    return {
        "id": teacher.id,
        "subject": teacher.subject,
        "bio": teacher.bio,
        "location": teacher.location,
        "phone": getattr(teacher, 'phone', None),
        "experience": getattr(teacher, 'experience_years', None)
    }


# 4. Update teacher info
@router.put("/{teacher_id}")
def update_teacher(teacher_id: int, teacher_data: TeacherUpdate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    for key, value in teacher_data.dict(exclude_unset=True).items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return {
        "message": "Teacher updated successfully",
        "teacher": {
            "id": teacher.id,
            "subject": teacher.subject,
            "bio": teacher.bio,
            "location": teacher.location
        }
    }
