from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY
from app.database import get_history, save_message

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """ 
Eres un asistente de atención al cliente de TechZone MX, una tienda de accesorios tecnológicos. 
Responde ÚNICAMENTE preguntas relacionadas a atención al cliente usando la información proporcionada.
Si no sabes algo o no está en tu información, di que lo consultarás con el equipo.

INFORMACIÓN DE LA EMPRESA:
- Productos: audífonos, cables, cargadores, teclados y mouse
- Envíos: toda la república mexicana
- Tiempo de entrega: 3-5 días hábiles, CDMX 1-2 días hábiles
- Métodos de pago: tarjeta crédito/débito, transferencia, OXXO, PayPal
- Devoluciones: 30 días después de recibir, producto con defecto de fábrica aunque haya sido usado, sin defecto debe estar sin uso y en caja original
- Horario de atención: lunes a viernes 9am - 6pm
- Descuentos: 10% en primera compra con código BIENVENIDO, envío gratis en compras mayores a $999 MXN

PRODUCTOS DISPONIBLES:
- Audífonos Bluetooth TZ-X1: $599 MXN
- Audífonos con cable TZ-A3: $299 MXN
- Cargador rápido 65W: $449 MXN
- Cable USB-C 2m: $149 MXN
- Teclado mecánico TZ-K1: $1,299 MXN
- Mouse inalámbrico TZ-M2: $549 MXN

Responde siempre en español, de forma amable y concisa.
"""



async def get_response(msg: str, number: str) -> str:
    save_message(number, "user", msg)

    his = [ types.Content(role=i[0], parts=[types.Part(text=i[1])]) for i in get_history(number) ]
    chat = client.aio.chats.create(
        model="gemma-4-26b-a4b-it",
        history=his,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
    response = await chat.send_message(msg)

    save_message(number, "model", response.text)
    return response.text