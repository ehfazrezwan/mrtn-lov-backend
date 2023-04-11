import uuid
import json
from fastapi import APIRouter, HTTPException, status, WebSocket
from io import BytesIO
import base64

from services.google_sheets import GoogleSheets
from services.repository import PromptRepository
from services.banana_client import start_image_generation, check_image_generation, paste_overlay

from db.database import SessionLocal

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action")

            if action == "start":
                prompt = message["prompt"]
                gs = GoogleSheets()
                db = SessionLocal()
                pr = PromptRepository(db)
                data = {
                    "uuid": str(uuid.uuid4()),
                    "prompt": prompt
                }
                pr.create(data["prompt"])
                # gs.append_row(data)
                call_id = await create_prompt(prompt)
                if call_id is None:
                    start_response = {"status": "error", "message": "Failed to start image generation"}
                    await websocket.send_json(start_response)
                    await websocket.close()
                    break
                else:
                    start_response = {"status": "started", "callID": call_id}
                await websocket.send_json(start_response)

            elif action == "check":
                call_id = message["callID"]
                image_base64 = await check_prompt(call_id)

                if image_base64 is None:
                    check_response = {"status": "running"}
                    await websocket.send_json(check_response)
                    continue

                check_response = {"status": "completed", "image_base64": image_base64}
                await websocket.send_json(check_response)
                await websocket.close()
                break

            else:
                error_response = {"status": "error", "message": "Invalid action"}
                await websocket.send_json(error_response)
                await websocket.close()
                break
        except Exception as e:
            error_response = {"status": "error", "message": f"Unexpected error: {str(e)}"}
            await websocket.send_json(error_response)
            await websocket.close()
            break


async def create_prompt(prompt):
    try:
        call_id = await start_image_generation(prompt)
        return call_id
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def check_prompt(call_id):
    try:
        ai_image = await check_image_generation(call_id)
        ai_image = paste_overlay(ai_image)
        
        buffered = BytesIO()
        ai_image.save(buffered,format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return image_base64
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))