from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel

from services.ml_service import predict
from services.llm_service import explain

class TextRequest(BaseModel):
    text:str


router=APIRouter(
    prefix="/verify",
    tags=["Verify"]
)

@router.post("/text")
def verify_text(request:TextRequest):
    if len(request.text.strip())<50:
        raise HTTPException(status_code=400,detail="Text too short to analyze-minimum 50 characters")
    ml_result=predict(request.text)
    llm_result=explain(request.text,ml_result["verdict"],ml_result["confidence"])


    return {
        "input_type":"text",
        "verdict":ml_result["verdict"],
        "confidence":ml_result["confidence"],
        "fake_probability":ml_result["fake_probability"],
        "real_probability": ml_result["real_probability"],
        "explanation": llm_result["explanation"],
        "red_flags": llm_result["red_flags"],
        "recommendation": llm_result["recommendation"]

    }
