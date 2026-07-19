from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth
from routers import verify
from database import Base,engine

Base.metadata.create_all(bind=engine)

#ee line endukante..it creates all tables in database if okkati kuda lekapothe yet..ee line lekapothe signup endpoint crashes- no users table



app=FastAPI(
    title="VeriScope",
    description="AI-Powered Fake News Detector",
    version="1.0.0"
)


app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth.router)
app.include_router(verify.router)
@app.get("/")
def home():
    return {
        "app":"VeriScope",
        "message":"AI-Powered Fake News Detector",
        "status":"running"
    }




