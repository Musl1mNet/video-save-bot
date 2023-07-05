import json
from bs4 import BeautifulSoup
import requests
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from instagram_downloader.methods import download


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(text="Xush kelibsiz {}\nbotimizdan foydalanish uchun instagramdan link jo'nating!".format(update.effective_user.first_name))


async def download_images_or_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message.text
    is_url = msg.split(":")[0] == "http" or msg.split(":")[0] == "https"
    if is_url:
        if msg.find("instagram"):
            url = msg
        else:
            text = "Iltimos instagramdagi postning linklarini jo'nating\nboshqa saytni hozircha qo'llab quvvatlamaymiz"
            await update.edited_message.reply_text(text=text)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup = soup.find_all("script", type="application/ld+json")

        if soup:
            resp = json.loads(soup[0].text)
            if resp.get("video", False):
                for item in resp["video"]:
                    vurl = item.get("contentUrl")
                    await download(vurl, update)
            elif resp.get("image", False):
                for item in resp["image"]:
                    vurl = item.get("url")
                    await download(vurl, update)
        else:
            text = "So‘rov bajarilmadi. Hisob shaxsiy emasligiga ishonch hosil qiling. \nAgar u ommaviy bo‘lsa, qayta urinib ko‘ring."
            await update.effective_message.reply_text(text)

    else:
        await update.effective_message.reply_text(text="Iltimos tekshirib qaytadan jo'nating\nLink ligiga ishinch hosil qiling")

handlers = [
    CommandHandler("start", start),
    MessageHandler(filters.TEXT, download_images_or_video),
]
