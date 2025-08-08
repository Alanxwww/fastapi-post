# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<passoword>@<ip-address>/<database_name>"
SQLALCHEMY_DATABASE_URL= (
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Dependency to get the database session
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost", database="fastapi",
#             user="postgres", password="1019",
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error:", error)
#         time.sleep(2)  # wait for 2 seconds before retrying

# # simulating a database
# my_posts = [{"title": "title of post 1", "content": "content of post 1" , "id": 1}, 
#             {"title": "title of post 2", "content": "content of post 2" , "id": 2}]