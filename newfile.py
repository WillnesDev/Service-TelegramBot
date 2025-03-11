import os
import yt_dlp
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "7558561191:AAE4KBjYYpL3lgGAccRI-TY9OLesCQFRdbM"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Menga YouTube yoki Instagram havolasini yuboring, men videoni yuklab beraman.")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        await message.reply("⏳ Yuklab olinmoqda...")

        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await message.reply_video(video=open("video.mp4", "rb"))
        os.remove("video.mp4")
    
    elif "instagram.com/reel" in url:
        await message.reply("⏳ Instagram Reels yuklab olinmoqda...")
        
        loader = instaloader.Instaloader()
        shortcode = url.split("/")[-2]  # Instagram Reels URL-dan shortcode ajratib olish
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target="downloads")
        
        for file in os.listdir("downloads"):
            if file.endswith(".mp4"):
                await message.reply_video(video=open(f"downloads/{file}", "rb"))
                os.remove(f"downloads/{file}")
                break
    else:
        await message.reply("❌ Bu havola qo‘llab-quvvatlanmaydi!")

executor.start_polling(dp)