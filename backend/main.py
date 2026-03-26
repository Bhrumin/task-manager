from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= USER =================

@app.post("/register")
def register(data: dict, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data["email"]).first():
        raise HTTPException(400, "User exists")

    user = models.User(
        email=data["email"],
        password=auth.hash_password(data["password"])
    )
    db.add(user)
    db.commit()
    return {"message": "User created"}


@app.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data["email"]).first()

    if not user or not auth.verify_password(data["password"], user.password):
        raise HTTPException(401, "Invalid credentials")

    token = auth.create_token({"user_id": user.id})
    return {"access_token": token}


# ================= AUTH =================

def get_user(token: str, db):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")

    user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
    return user


# ================= TASK =================

@app.post("/tasks")
def create_task(data: dict, db: Session = Depends(get_db), authorization: str = Header()):
    user = get_user(authorization, db)

    task = models.Task(title=data["title"], owner_id=user.id)
    db.add(task)
    db.commit()
    return {"message": "Task created"}


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db), authorization: str = Header()):
    user = get_user(authorization, db)
    return db.query(models.Task).filter(models.Task.owner_id == user.id).all()


@app.put("/tasks/{id}")
def toggle_task(id: int, db: Session = Depends(get_db), authorization: str = Header()):
    user = get_user(authorization, db)

    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user.id).first()
    if not task:
        raise HTTPException(404, "Not found")

    task.completed = not task.completed
    db.commit()
    return {"message": "Updated"}


@app.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db), authorization: str = Header()):
    user = get_user(authorization, db)

    task = db.query(models.Task).filter(models.Task.id == id, models.Task.owner_id == user.id).first()
    if not task:
        raise HTTPException(404, "Not found")

    db.delete(task)
    db.commit()
    return {"message": "Deleted"}