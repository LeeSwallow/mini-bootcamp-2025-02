from sqlmodel import SQLModel, create_engine, Session
import os
DB_URL = os.getenv("POSTGRE_DB_URL")
if not DB_URL:
  raise Exception("DB_URL environment variable is not set")

engine = create_engine(DB_URL)

def get_session():
  with Session(engine) as session:
      yield session

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
  SQLModel.metadata.drop_all(engine)