import uuid
import json
from fastapi import APIRouter, HTTPException, status
from services.google_sheets import GoogleSheets
from services.repository import PromptRepository
from services.banana_client import generate_image
from pydantic import BaseModel

from db.database import SessionLocal

router = APIRouter()

class PromptInput(BaseModel):
    prompt: str

class PromptOutput(BaseModel):
    message: str
    response: str

@router.post("/prompt", response_model=PromptOutput, status_code=status.HTTP_201_CREATED)
async def create_prompt(prompt_input: PromptInput):
    gs = GoogleSheets()
    db = SessionLocal()
    pr = PromptRepository(db)
    data = {
        "uuid": str(uuid.uuid4()),
        "prompt": prompt_input.prompt
    }
    try:
        pr.create(data["prompt"])
        # gs.append_row(data)
        banana_response = generate_image(data["prompt"])
        image_data = banana_response["modelOutputs"][0]["image_base64"]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()

    return {"message": "Prompt created successfully", "response": image_data.encode('utf-8')}
