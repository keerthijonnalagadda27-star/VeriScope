from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL","sqlite:///./veriscope.db")

#sqlite anedi good for development and zero setup and just oka file laga.. postgreSql aithe better for production and concurrent files ni kuda handles well..manaki deeniki sqlite chalu..
#railway postgreSQL URLs postgres:// ala start avthai..but sqlalchemy needs postgresql:// sooo andukani..writing thhis line..

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL=DATABASE_URL.replace("postgres://","postgresql://")


if "sqlite" in DATABASE_URL:
    engine=create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread":False}

        #actually ee check same thread false anedhi only sqlite ki specific ga untundi..as sqqlite okkasarilo oka thread ney allow chestundi for connection..but fastapi uses multiple threads so idi false set cheyalii ..postgresql aithe concurrently handle cheyagaladu..

    )
else:
    engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

# Base is the parent class all our models inherit from
# SQLAlchemy uses it to track which classes are database tables

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()