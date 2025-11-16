from fastapi import APIRouter, Depends, HTTPException, Request
import os
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Payment, Teacher
from schemas import PaymentCreate
from eversend_client import initiate_mobile_money

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Initiate payment
@router.post("/initiate")
def create_payment(payment: PaymentCreate, request: Request, db: Session = Depends(get_db)):
    # Determine callback URL from environment or request base URL
    base = os.environ.get('BASE_URL') or str(request.base_url).rstrip('/')
    callback_url = f"{base}/payments/webhook/eversend"

    teacher = db.query(Teacher).filter(Teacher.id == payment.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    try:
        response = initiate_mobile_money(
            amount=payment.amount,
            currency="UGX",
            phone_number=payment.phone_number,
            method=payment.method,
            callback_url=callback_url,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eversend error: {e}")

    txn_id = response.get("transaction_id") or response.get("id", "unknown")

    new_payment = Payment(
        teacher_id=teacher.id,
        amount=payment.amount,
        method=payment.method,
        transaction_id=txn_id,
        status="PENDING",
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {"message": "Payment initiated", "transaction_id": txn_id}


# 2. Webhook for Eversend
@router.post("/webhook/eversend")
async def eversend_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    txn_id = payload.get("transaction_id")
    status = payload.get("status")

    if not txn_id:
        return {"message": "Missing transaction_id"}

    payment = db.query(Payment).filter(Payment.transaction_id == txn_id).first()
    if not payment:
        return {"message": "Payment not found"}

    payment.status = status
    db.commit()

    # Activate user account when payment successful
    if status and status.lower() == "success":
        teacher = db.query(Teacher).filter(Teacher.id == payment.teacher_id).first()
        if teacher:
            # If Teacher is linked to a User, activate the User
            try:
                if hasattr(teacher, 'user') and teacher.user:
                    teacher.user.active = True
                    db.commit()
                else:
                    # Fallback: try to set a field on teacher if exists
                    if hasattr(teacher, 'active'):
                        teacher.active = True
                        db.commit()
            except Exception:
                db.rollback()
                # swallow errors but return payment updated

    return {"message": "Payment updated successfully"}
