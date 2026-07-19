import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, help_command, about, get_user_info, handle_tiktok_link

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.Regex(r'^@\w+$'), get_user_info))
    app.add_handler(MessageHandler(filters.Regex(r'tiktok\.com'), handle_tiktok_link))
    print("🚀 বট চালু হচ্ছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
