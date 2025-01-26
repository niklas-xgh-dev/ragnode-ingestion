from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_ENDPOINT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(engine)
Base = declarative_base()

def get_session():
    with Session() as session:
        yield session