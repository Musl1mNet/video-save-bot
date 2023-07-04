import json
import html_to_json
import requests
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from instagram_downloader.methods import download


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(text="Xush kelibsiz {}\n botimizdan foydalanish uchun instagramdan link jo'nating!".format(update.effective_user.first_name))


async def download_images_or_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message.text
    is_url = msg.split(":")[0] == "http" or msg.split(":")[0] == "https"
    if is_url:
        if msg.find("instagram"):
            url = msg
        else:
            text = "Iltimos instagramdagi postning linklarini jo'nating\n boshqa saytni hozircha qo'llab quvvatlamaymiz"
            await update.edited_message.reply_text(text=text)
        response = requests.get(url)
        r = html_to_json.convert(response.text)
        resp = r["html"][0]["head"][0]["script"][0]["_value"]
        resp = json.loads(resp)
        if resp.get("video", False):
            for item in resp["video"]:
                vurl = item.get("contentUrl")
                if vurl:
                    await download(vurl, update)
                else:
                    text = "So‘rov bajarilmadi. Hisob shaxsiy emasligiga ishonch hosil qiling. \nAgar u ommaviy bo‘lsa, qayta urinib ko‘ring."
                    await update.effective_message.reply_text(text)
        elif resp.get("image", False):
            for item in resp["image"]:
                vurl = item.get("url")
                if vurl:
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
