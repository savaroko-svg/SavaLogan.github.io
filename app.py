import json
import hmac
import hashlib
import os
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

SECRET_KEY = "208a5ce262a536851476153d1e96ff19263e6353"

@app.post("/webhook")
async def lava_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Signature")
    
    # Проверяем подпись
    if signature:
        expected = hmac.new(
            SECRET_KEY.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected):
            print(f"Подпись не совпадает! Ожидалось: {expected}, Получено: {signature}")
            raise HTTPException(status_code=403, detail="Invalid signature")
    
    data = await request.json()
    print(f"Получен webhook: {json.dumps(data, indent=2)}")
    
    if data.get("status") == "success":
        order_id = data.get("order_id")
        amount = data.get("sum")
        print(f"✅ УСПЕШНАЯ ОПЛАТА! order_id: {order_id}, сумма: {amount} руб")
        
        # Здесь ваш код: обновить баланс пользователя в БД или вызвать Telegram бота
    
    return {"status": "success"}

@app.get("/")
def root():
    return {"status": "ok", "message": "Lava webhook работает"}
