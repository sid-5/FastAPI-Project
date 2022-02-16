from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#ORM for creating database
SQLAL_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLAL_URL)

#request for a session
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

#Connecting to database using psycopg driver which uses SQL statements instead of and ORM like sqlachemy
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastAPI', user="postgres",
#         password = '123456', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error was: ", error)
#         time.sleep(2)