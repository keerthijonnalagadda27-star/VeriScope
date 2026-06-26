from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import verify
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

app.include_router(verify.router)
@app.get("/")
def home():
    return {
        "app":"VeriScope",
        "message":"AI-Powered Fake News Detector",
        "status":"running"
    }