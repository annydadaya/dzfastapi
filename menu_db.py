from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv('.env')

engine = create_engine(url=os.environ["DATABASE_URL"], echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

