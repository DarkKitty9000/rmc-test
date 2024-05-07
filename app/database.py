from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

db_password = os.getenv("POSTGRES_PASS")
db_user = os.getenv("POSTGRES_USER")
db_base = os.getenv("POSTGRES_DB")
db_address = os.getenv("POSTGRES_ADDRESS")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_address}/{db_base}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
