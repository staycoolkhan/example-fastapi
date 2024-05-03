from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.database import get_db
from app.main import app
from app import schemas
from app.models import Base
from alembic import config, command
# from alembic.config import Config

# SQLALCHEMY_DATABASE_URL = 'postgresql://testpostgres:testpassword@localhost:5432/fastapi_test'


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




# # Dependency
# def overrid_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# app.dependency_overrides[get_db] = overrid_get_db
        
# # One way -  using 'sqlalchemy'    
# @pytest.fixture
# def client():
#     #run our code to drop tables before runing any test
#     Base.metadata.drop_all(bind=engine)
#     # run our code before we run out test
#     Base.metadata.create_all(bind=engine)
    
#     yield TestClient(app)
    
#     # #run our code after our test finishes
#     # Base.metadata.drop_all(bind=engine)
    
# # another way -  using 'alembic'  this is giving me error at the moment  
# @pytest.fixture
# def client():
   
#     # Upgrade to the specified revision
#     command.upgrade("head")

#     yield TestClient(app)
    
#     command.downgrade("base")
    

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)
    
    