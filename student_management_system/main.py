from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, Session, StudentDB
from models import Student  # Pydantic model

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS setup
# CORS setup
origins = [
    "http://127.0.0.1:5500",  # Your current front-end origin
    "http://localhost:5500",  # Add localhost for robustness
    # Add any other origins (e.g., a production domain) here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)
# DB dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/students")
def read_students(db: Session = Depends(get_db)):
    return db.query(StudentDB).all()

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.post("/students")
def create_student(student: Student, db: Session = Depends(get_db)):
    db_student = StudentDB(**student.dict(exclude={"id"}))

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in updated_student.dict(exclude={"id"}).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"detail": "Student deleted successfully"}
