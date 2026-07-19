import os
import threading
from flask import Flask
from bot import main as start_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running on Render!"

@app.route('/health')
def health():
    return "OK"

def run_bot():
    start_bot()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
