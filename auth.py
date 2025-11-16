from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin
from models import Notification
from schemas import NotificationOut
import bcrypt


router = APIRouter(prefix="/auth", tags=["Auth"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    # --- Notification Endpoint for Teachers ---
@router.get("/notifications/{user_id}", response_model=list[NotificationOut])
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    notifs = db.query(Notification).filter(Notification.recipient_user_id == user_id).order_by(Notification.created_at.desc()).all()
    return notifs
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Server-side validation
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    if len(user.name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password before storing
    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,  # Store hashed password
        role=user.role.lower(),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registration successful", "user_id": new_user.id}


@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # For UI routing we return the user's activation status instead of blocking login.
    # Frontend will redirect teachers who are not active to the payment page.
    return {
        "message": "Login successful",
        "user": {"id": user.id, "name": user.name, "role": user.role},
        "active": bool(getattr(user, 'active', False))
    }
