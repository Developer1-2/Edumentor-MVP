
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import JobPosting, School, JobApplication, Notification
from schemas import JobPostingCreate, JobPostingUpdate, JobPostingOut, JobApplicationCreate, JobApplicationOut, NotificationCreate, NotificationOut
import typing as t

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Create a job posting
@router.post("/", response_model=JobPostingOut)
def create_job_posting(job: JobPostingCreate, school_id: int, db: Session = Depends(get_db)):
    """Create a new job posting for a school"""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    new_job = JobPosting(
        school_id=school_id,
        title=job.title,
        subject=job.subject,
        experience=job.experience,
        description=job.description,
        salary=job.salary,
        status="Active"
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    # Notify all teachers about new job
    teacher_ids = [t.id for t in db.query(JobApplication.teacher_id).distinct()]
    for tid in teacher_ids:
        notif = Notification(
            recipient_user_id=tid,
            type="job_posted",
            content=f"New job posted: {job.title}"
        )
        db.add(notif)
    db.commit()
    return new_job

    # --- Job Application Endpoints ---

@router.post("/apply/", response_model=JobApplicationOut)
def apply_for_job(application: JobApplicationCreate, db: Session = Depends(get_db)):
    # Check if job exists
    job = db.query(JobPosting).filter(JobPosting.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # Check if teacher already applied
    existing = db.query(JobApplication).filter(JobApplication.job_id == application.job_id, JobApplication.teacher_id == application.teacher_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    db_app = JobApplication(**application.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    # Create notification for school
    notif = Notification(
        recipient_user_id=job.school_id,  # Assuming school_id is user_id
        type="application_submitted",
        content=f"Teacher {application.teacher_id} applied for job {application.job_id}"
    )
    db.add(notif)
    db.commit()
    return db_app

@router.get("/{job_id}/applications", response_model=t.List[JobApplicationOut])
def get_job_applications(job_id: int, db: Session = Depends(get_db)):
    apps = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()
    result = []
    for a in apps:
        teacher = None
        teacher_name = None
        teacher_phone = None
        try:
            if hasattr(a, 'teacher') and a.teacher:
                teacher = a.teacher
                if hasattr(teacher, 'user') and teacher.user:
                    teacher_name = teacher.user.name
                teacher_phone = getattr(teacher, 'phone', None)
        except Exception:
            pass

        result.append({
            'id': a.id,
            'job_id': a.job_id,
            'teacher_id': a.teacher_id,
            'teacher_name': teacher_name or f'Teacher #{a.teacher_id}',
            'teacher_phone': teacher_phone,
            'status': a.status,
            'message': a.message,
            'created_at': a.created_at,
        })

    return result

@router.get("/schools/{school_id}/applications", response_model=t.List[JobApplicationOut])
def get_school_applications(school_id: int, db: Session = Depends(get_db)):
    jobs = db.query(JobPosting).filter(JobPosting.school_id == school_id).all()
    job_ids = [job.id for job in jobs]
    apps = db.query(JobApplication).filter(JobApplication.job_id.in_(job_ids)).all()
    result = []
    for a in apps:
        teacher_name = None
        teacher_phone = None
        try:
            if hasattr(a, 'teacher') and a.teacher:
                if hasattr(a.teacher, 'user') and a.teacher.user:
                    teacher_name = a.teacher.user.name
                teacher_phone = getattr(a.teacher, 'phone', None)
        except Exception:
            pass

        result.append({
            'id': a.id,
            'job_id': a.job_id,
            'teacher_id': a.teacher_id,
            'teacher_name': teacher_name or f'Teacher #{a.teacher_id}',
            'teacher_phone': teacher_phone,
            'status': a.status,
            'message': a.message,
            'created_at': a.created_at,
        })

    return result



# 2. Get all job postings
@router.get("/")
def get_all_jobs(db: Session = Depends(get_db)):
    """Get all active job postings"""
    jobs = db.query(JobPosting).filter(JobPosting.status == "Active").all()
    result = []
    for job in jobs:
        school_name = "Unknown School"
        try:
            if hasattr(job, 'school') and job.school:
                school_name = job.school.name
        except Exception:
            pass
        
        result.append({
            "id": job.id,
            "school_id": job.school_id,
            "school_name": school_name,
            "title": job.title,
            "subject": job.subject,
            "experience": job.experience,
            "description": job.description,
            "salary": job.salary,
            "status": job.status,
            "created_at": job.created_at,
            "updated_at": job.updated_at
        })
    
    return {"jobs": result}


# 3. Get job postings by school
@router.get("/school/{school_id}")
def get_school_jobs(school_id: int, db: Session = Depends(get_db)):
    """Get all job postings for a specific school"""
    jobs = db.query(JobPosting).filter(JobPosting.school_id == school_id).all()
    result = []
    for job in jobs:
        result.append({
            "id": job.id,
            "school_id": job.school_id,
            "title": job.title,
            "subject": job.subject,
            "experience": job.experience,
            "description": job.description,
            "salary": job.salary,
            "status": job.status,
            "created_at": job.created_at,
            "updated_at": job.updated_at
        })
    
    return {"jobs": result}


# 4. Get single job posting
@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job posting by ID"""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    school_name = "Unknown School"
    try:
        if hasattr(job, 'school') and job.school:
            school_name = job.school.name
    except Exception:
        pass
    
    return {
        "id": job.id,
        "school_id": job.school_id,
        "school_name": school_name,
        "title": job.title,
        "subject": job.subject,
        "experience": job.experience,
        "description": job.description,
        "salary": job.salary,
        "status": job.status,
        "created_at": job.created_at,
        "updated_at": job.updated_at
    }


# 5. Update job posting
@router.put("/{job_id}", response_model=JobPostingOut)
def update_job(job_id: int, job_data: JobPostingUpdate, db: Session = Depends(get_db)):
    """Update a job posting"""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    for key, value in job_data.dict(exclude_unset=True).items():
        setattr(job, key, value)
    
    db.commit()
    db.refresh(job)
    return job


# 6. Delete job posting
@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job posting"""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job posting deleted successfully"}
