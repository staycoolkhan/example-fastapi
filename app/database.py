from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
import time


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# # # Regular SQL
# while True:
        
#     try:
#         conn = psycopg2.connect(host={settings.database_hostname}, database={settings.database_name}, user={settings.database_username}, 
#                             password= {settings.database_password}, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connectiong to the databse failed")
#         print("Error: ", error)
#         time.sleep(2)

# my_posts = [{"title": "title of post 1", "content": "content of the post 1", "id": 1}, 
#             {"title": "favourite foods", "content": "I like pizza", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i