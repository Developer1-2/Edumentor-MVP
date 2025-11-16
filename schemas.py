from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)
    role: str  # teacher or school

    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TeacherCreate(BaseModel):
    subject: str
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    experience_years: Optional[int] = None
    user_id: Optional[int] = None

class PaymentCreate(BaseModel):
    user_id: int
    amount: float
    method: str

class TeacherBase(BaseModel):
    subject: str
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    experience_years: Optional[int] = None


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    subject: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    experience_years: Optional[int] = None

class SchoolBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None

class PaymentBase(BaseModel):
    teacher_id: int
    amount: float
    method: str

class PaymentCreate(PaymentBase):
    phone_number: str

class PaymentOut(BaseModel):
    id: int
    teacher_id: int
    amount: float
    method: str
    transaction_id: str
    status: str

    class Config:
        orm_mode = True


class JobPostingBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    subject: str = Field(..., min_length=1, max_length=255)
    experience: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    experience: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[str] = None


class JobPostingOut(JobPostingBase):
    id: int
    school_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Job Application Schemas
class JobApplicationBase(BaseModel):
    job_id: int
    teacher_id: int
    message: Optional[str] = None

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationOut(JobApplicationBase):
    id: int
    status: str
    created_at: datetime
    teacher_name: Optional[str] = None
    teacher_phone: Optional[str] = None
    class Config:
        orm_mode = True

# Notification Schemas
class NotificationBase(BaseModel):
    recipient_user_id: int
    type: str
    content: str

class NotificationCreate(NotificationBase):
    pass

class NotificationOut(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime
    class Config:
        orm_mode = True
