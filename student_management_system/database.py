from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:bhanu2004@localhost:3305/student"

# Create engine
engine = create_engine(DATABASE_URL)

# Create Session class
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()

# Student table model
class StudentDB(Base):
    __tablename__ = "student"   # MySQL table name
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    age = Column(Integer)
    grade = Column(String(10))
    email = Column(String(255))
    courses = Column(String(255))

# Create tables
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
