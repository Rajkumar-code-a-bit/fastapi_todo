from sqlalchemy import create_engine;
from sqlalchemy.orm import sessionmaker, declarative_base;
from dotenv import load_dotenv;
import os;
load_dotenv()
DATABASE_URl= os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URl)
SessionLocal=sessionmaker(bind=engine,autoflush=False)
Base= declarative_base()

