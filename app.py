from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "8780269796:AAEFSTBAB45yJqINu3oTRKaNtkwaF3WozPI"
CHAT_ID = "168007098"

@app.route("/freekassa", methods=["POST"])
def freekassa():
    data = request.form.to_dict()
    # Здесь проверь подпись (по желанию)
    amount = data.get("AMOUNT")
    order_id = data.get("MERCHANT_ORDER_ID")
    
    text = f"✅ Оплачено!\nСумма: {amount}\nЗаказ: {order_id}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
