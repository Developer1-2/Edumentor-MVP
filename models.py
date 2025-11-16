from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'teacher' or 'school'
    active = Column(Boolean, default=False)

    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    bio = Column(String)
    location = Column(String)
    phone = Column(String(20))
    experience_years = Column(Integer, nullable=True)

    user = relationship("User", back_populates="teacher_profile")


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    location = Column(String(255)) 
    description = Column(String, nullable=True)

    job_postings = relationship("JobPosting", back_populates="school")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    amount = Column(Float, nullable=False)
    method = Column(String(50))  # MTN, AIRTEL, CARD, etc.
    transaction_id = Column(String(255), unique=True)
    status = Column(String(50), default="PENDING")  # PENDING, SUCCESS, FAILED
    created_at = Column(DateTime(timezone=True), server_default=func.now())



class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    title = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    experience = Column(String(100))
    description = Column(Text)
    salary = Column(String(255))
    status = Column(String(50), default="Active")  # Active, Closed, Draft
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    school = relationship("School", back_populates="job_postings")


# Job Application Model
class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    status = Column(String(50), default="Submitted")  # Submitted, Reviewed, Accepted, Rejected
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("JobPosting")
    teacher = relationship("Teacher")

# Notification Model
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50))  # job_posted, application_submitted, etc.
    content = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recipient = relationship("User")
