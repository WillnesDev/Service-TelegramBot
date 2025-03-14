import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from pytube import YouTube
import instaloader
import requests

# Logging sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Instagram Reels yuklash
def download_instagram_reels(url: str) -> str:
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
    video_url = post.video_url
    response = requests.get(video_url)
    with open("reels.mp4", "wb") as file:
        file.write(response.content)
    return "reels.mp4"

# YouTube video yuklash
def download_youtube_video(url: str) -> str:
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(filename="youtube.mp4")
    return "youtube.mp4"

# Start komandasi
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Assalomu alaykum! Instagram Reels, YouTube video yoki YouTube Shorts havolasini yuboring.")

# Havolani qabul qilish
async def handle_message(update: Update, context: CallbackContext):
    url = update.message.text
    if "instagram.com/reel/" in url:
        try:
            file_path = download_instagram_reels(url)
            await update.message.reply_video(video=open(file_path, "rb"))
            os.remove(file_path)
        except Exception as e:
            await update.message.reply_text(f"Xatolik: {e}")
    elif "youtube.com/shorts/" in url or "youtube.com/watch" in url:
        try:
            file_path = download_youtube_video(url)
            await update.message.reply_video(video=open(file_path, "rb"))
            os.remove(file_path)
        except Exception as e:
            await update.message.reply_text(f"Xatolik: {e}")
    else:
        await update.message.reply_text("Noto'g'ri havola. Iltimos, Instagram Reels, YouTube video yoki YouTube Shorts havolasini yuboring.")

# Botni ishga tushirish
def main():
    application = ApplicationBuilder().token("7558561191:AAE4KBjYYpL3lgGAccRI-TY9OLesCQFRdbM").build()

    # Komandalarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
