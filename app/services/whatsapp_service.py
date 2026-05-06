from twilio.rest import Client
from twilio.http.async_http_client import AsyncTwilioHttpClient
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER


async def send_message(to: str, response: str):
    # por si solo la funcion _client.messages.create_ no soporta asincronia
    async with AsyncTwilioHttpClient() as http_client:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, http_client=http_client)
        
        await client.messages.create_async(
            body=response,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=to,
        )