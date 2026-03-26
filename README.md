# task-manager# 🚀 Task Manager (Full Stack)

A simple full-stack Task Manager application built using **FastAPI (Backend)** and **React (Frontend)**.

---

## 📌 Features

* User Login (JWT Authentication)
* Create Tasks
* View Tasks
* Mark Tasks as Complete/Incomplete
* Delete Tasks
* Clean and simple UI

---

## 🛠️ Tech Stack

* **Frontend:** React.js
* **Backend:** FastAPI (Python)
* **Database:** SQLite
* **Auth:** JWT
* **Password Hashing:** Passlib

---

## 📁 Project Structure

```
task-manager/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   └── requirements.txt
│
└── frontend/
    └── src/
        └── App.js
```

---

## ⚙️ How to Run the Project

### 🔹 1. Clone Repository

```
git clone <your-repo-link>
cd task-manager
```

---

## ▶️ Backend Setup

### Step 1: Go to backend folder

```
cd backend
```

### Step 2: Create virtual environment

```
python -m venv venv
```

### Step 3: Activate venv (Windows)

```
venv\Scripts\activate
```

### Step 4: Install dependencies

```
pip install -r requirements.txt
```

### Step 5: Run server

```
uvicorn main:app --reload
```

👉 Backend will run on:
http://127.0.0.1:8000

---

## ▶️ Frontend Setup

### Step 1: Open new terminal

### Step 2: Go to frontend folder

```
cd frontend
```

### Step 3: Install dependencies

```
npm install
```

### Step 4: Run React app

```
npm start
```

👉 Frontend will run on:
http://localhost:3000

---

## 🧪 How to Use

1. Open the frontend in browser
2. Login using your credentials
3. Add new tasks
4. Mark tasks as complete
5. Delete tasks
6. Logout when done

---

## ⚠️ Notes

* Make sure backend is running before frontend
* JWT token is stored in browser localStorage
* CORS is enabled in backend

---

## 🎯 Future Improvements

* User Registration UI
* Better UI (Tailwind / Material UI)
* Task filtering (completed / pending)
* Deployment (Render / Vercel)

---




⭐ If you like this project, give it a star!
