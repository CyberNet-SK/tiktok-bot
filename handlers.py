import os
import logging
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from utils import TikTokAPI

logger = logging.getLogger(__name__)
tiktok_api = TikTokAPI()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🎯 **হ্যালো {user.first_name}!**\n\n"
        "আমি TikTok ডাউনলোডার ও ইউজার ইনফো বট।\n"
        "📌 **কীভাবে ব্যবহার করবেন:**\n"
        "• ইউজার ইনফো: `@username` পাঠান\n"
        "• ভিডিও ডাউনলোড: TikTok লিংক পাঠান\n\n"
        "🔹 **উদাহরণ:**\n"
        "`@elonmusk`\n"
        "`https://www.tiktok.com/@username/video/123456789`",
        parse_mode='Markdown'
    )

async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    username = text.replace('@', '').strip()

    try:
        chat = await context.bot.get_chat(f"@{username}")
        user_id = chat.id

        photos = await context.bot.get_user_profile_photos(user_id, limit=1)
        latest_photo = photos.photos[0][-1].file_id if photos.photos else None

        try:
            member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            member_status = member.status
            custom_title = member.custom_title
        except:
            member_status = "N/A"
            custom_title = None

        info_text = (
            f"👤 **সম্পূর্ণ ইউজার ইনফো**\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"👤 **ইউজারনেম:** @{chat.username or 'N/A'}\n"
            f"📛 **নাম:** {chat.first_name or ''} {chat.last_name or ''}\n"
            f"⭐ **প্রিমিয়াম:** {'হ্যাঁ ✅' if getattr(chat, 'is_premium', False) else 'না ❌'}\n"
            f"📝 **বায়ো:** {chat.bio or 'N/A'}\n"
            f"🖼️ **প্রোফাইল ফটো:** {photos.total_count} টি\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 **গ্রুপ স্ট্যাটাস:** {member_status}\n"
            f"🏷️ **কাস্টম টাইটেল:** {custom_title or 'N/A'}\n"
            f"🔗 **ডিপ লিংক:** `tg://user?id={user_id}`\n"
        )
        if chat.username:
            info_text += f"🌐 **লিংক:** [t.me/{chat.username}](https://t.me/{chat.username})"

        if latest_photo:
            file = await context.bot.get_file(latest_photo)
            file_path = f"profile_{user_id}.jpg"
            await file.download_to_drive(file_path)
            with open(file_path, 'rb') as photo_file:
                await update.message.reply_photo(
                    photo=InputFile(photo_file),
                    caption=info_text,
                    parse_mode='Markdown'
                )
            os.remove(file_path)
        else:
            await update.message.reply_text(info_text, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"❌ ডেটা আনতে ব্যর্থ: {str(e)}")

async def handle_tiktok_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if 'tiktok.com' not in url:
        return

    processing_msg = await update.message.reply_text("⏳ **ভিডিও ডাউনলোড হচ্ছে...**", parse_mode='Markdown')

    try:
        result = tiktok_api.get_video_data(url)
        if result['success'] and result.get('video_url'):
            video_url = result['video_url']
            if tiktok_api.download_video_file(video_url, 'temp_video.mp4'):
                caption = f"🎬 **ভিডিও ডাউনলোড সম্পন্ন!**\n"
                if result.get('author'):
                    caption += f"👤 **ক্রিয়েটর:** {result['author']}\n"
                if result.get('description'):
                    caption += f"📝 **বিবরণ:** {result['description'][:200]}..."
                await processing_msg.delete()
                with open('temp_video.mp4', 'rb') as video_file:
                    await update.message.reply_video(
                        video=InputFile(video_file),
                        caption=caption,
                        parse_mode='Markdown'
                    )
                os.remove('temp_video.mp4')
            else:
                await processing_msg.edit_text("❌ ভিডিও ডাউনলোড করতে ব্যর্থ।")
        else:
            await processing_msg.edit_text(f"❌ {result.get('error', 'অজানা ত্রুটি')}")

    except Exception as e:
        await processing_msg.edit_text(f"❌ ত্রুটি: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **হেল্প মেনু**\n\n"
        "• ইউজার ইনফো: `@username` টাইপ করুন\n"
        "• ভিডিও ডাউনলোড: TikTok লিংক পেস্ট করুন\n"
        "• কমান্ড: /start, /help, /about",
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **TikTok ডাউনলোডার বট v3.0**\n"
        "⚡ অফিসিয়াল TikTok API + ব্যাকআপ\n"
        "👨‍💻 ডেভেলপার: আপনার কমান্ডার",
        parse_mode='Markdown'
    )
