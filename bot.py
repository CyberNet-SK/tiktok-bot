import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import start, help_command, about, get_user_info, handle_tiktok_link

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # কমান্ড
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))

    # মেসেজ হ্যান্ডলার
    app.add_handler(MessageHandler(filters.Regex(r'^@\w+$'), get_user_info))          # @username
    app.add_handler(MessageHandler(filters.Regex(r'tiktok\.com'), handle_tiktok_link)) # TikTok লিংক

    print("🚀 বট চালু হচ্ছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
