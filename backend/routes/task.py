from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter()

def get_current_user(token: str, db):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
    return user

@router.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), authorization: str = Header()):
    user = get_current_user(authorization, db)

    new_task = models.Task(title=task.title, owner_id=user.id)
    db.add(new_task)
    db.commit()
    return {"message": "Task created"}

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db), authorization: str = Header()):
    user = get_current_user(authorization, db)
    return db.query(models.Task).filter(models.Task.owner_id == user.id).all()

@router.put("/tasks/{id}")
def update_task(id: int, db: Session = Depends(get_db), authorization: str = Header()):
    user = get_current_user(authorization, db)
    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    db.commit()
    return {"message": "Updated"}

@router.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db), authorization: str = Header()):
    user = get_current_user(authorization, db)
    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Deleted"}