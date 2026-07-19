import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CLIENT_KEY = os.environ.get("CLIENT_KEY")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")
if not CLIENT_KEY:
    raise ValueError("CLIENT_KEY environment variable not set!")
if not CLIENT_SECRET:
    raise ValueError("CLIENT_SECRET environment variable not set!")
