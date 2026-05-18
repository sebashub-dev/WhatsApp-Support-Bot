from fastapi import APIRouter, Form
from app.services import ai_service, whatsapp_service


router = APIRouter()

@router.post("/webhook")
async def webhook(Body: str = Form(), From: str = Form()):
    try:
        response = await ai_service.get_response(Body, From)
        print(response)
        await whatsapp_service.send_message(From, response)
    except Exception as e:
        print(f"Error: {e}")
        
    return {"status": "ok"}