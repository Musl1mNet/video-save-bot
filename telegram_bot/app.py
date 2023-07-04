from telegram.ext import ApplicationBuilder

from telegram_bot.handlers import handlers

app = ApplicationBuilder().token("6303739111:AAHAUwoDDOANFT3E1nQ3eA96TcT93iafPMY").build()

app.add_handlers(handlers)
