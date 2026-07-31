import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🛒 Order Produk"],
        ["📦 Senarai Produk"],
        ["📞 Hubungi Admin"]
    ]

    reply = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Selamat datang ke Supply Auto Order 🤖\n\nPilih menu:",
        reply_markup=reply
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 Senarai Produk":
        await update.message.reply_text(
            "📦 Produk tersedia:\n\n"
            "1. Produk A - RM10\n"
            "2. Produk B - RM20"
        )

    elif text == "🛒 Order Produk":
        await update.message.reply_text(
            "🛒 Sila taip produk yang ingin order."
        )

    elif text == "📞 Hubungi Admin":
        await update.message.reply_text(
            "Admin: @usernameanda"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, menu))

app.run_polling()
