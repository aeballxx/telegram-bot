import os
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 7413570612


PAYMENT = """
💳 BAYARAN

Bank:
No Akaun:
Nama:

Sila buat bayaran dan hantar bukti pembayaran.
"""


products = {
    "np": {
        "name": "Netflix Private",
        "price": 12,
        "need": "namepin"
    },
    "ns": {
        "name": "Netflix Sharing",
        "price": 6,
        "need": "none"
    },
    "yp": {
        "name": "YouTube Private",
        "price": 5,
        "need": "email"
    },
    "ys": {
        "name": "YouTube Sharing",
        "price": 3,
        "need": "email"
    },
    "hbo": {
        "name": "HBO Max Private",
        "price": 5,
        "need": "namepin"
    },
    "prime": {
        "name": "Prime Video Private",
        "price": 5,
        "need": "namepin"
    }
}


orders = {}
users = {}

order_number = 1000


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Beli Produk",
                callback_data="shop"
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Premium Store\n\n"
        "Selamat datang.\n"
        "Tekan butang untuk beli.",
        reply_markup=InlineKeyboardMarkup(keyboard)

        async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = []

    for key, item in products.items():
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{item['name']} RM{item['price']}",
                    callback_data=key
                )
            ]
        )

    await query.edit_message_text(
        "🛒 Pilih produk:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def product_select(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global order_number

    query = update.callback_query
    await query.answer()

    key = query.data
    user = query.from_user

    product = products[key]

    order_id = order_number
    order_number += 1


    orders[order_id] = {
        "user_id": user.id,
        "username": user.username,
        "product": product["name"],
        "price": product["price"],
        "detail": {}
    }


    users[user.id] = {
        "order": order_id,
        "step": "detail"
    }


    if product["need"] == "none":

        users[user.id]["step"] = "payment"

        await query.edit_message_text(
            f"🧾 ORDER #{order_id}\n\n"
            f"Produk: {product['name']}\n"
            f"Harga: RM{product['price']}\n\n"
            f"{PAYMENT}"
        )


    elif product["need"] == "email":

        await query.edit_message_text(
            f"🧾 ORDER #{order_id}\n\n"
            f"Produk: {product['name']}\n"
            f"Harga: RM{product['price']}\n\n"
            "Sila masukkan email:"
        )


    else:

        await query.edit_message_text(
            f"🧾 ORDER #{order_id}\n\n"
            f"Produk: {product['name']}\n"
            f"Harga: RM{product['price']}\n\n"
            "Sila masukkan nama:"
        )



async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.message.from_user.id

    if uid not in users:
        return

    order_id = users[uid]["order"]
    order = orders[order_id]

    step = users[uid]["step"]


    if step == "detail":

        if "nama" not in order["detail"]:

            order["detail"]["nama"] = update.message.text

            if "YouTube" in order["product"]:

                await update.message.reply_text(
                    "Sila buat bayaran.\n\n"
                    f"{PAYMENT}"
                )

                users[uid]["step"] = "payment"

            else:

                await update.message.reply_text(
                    "Sila masukkan PIN 4 digit:"
                )


        else:

            order["detail"]["pin"] = update.message.text

            users[uid]["step"] = "payment"

            await update.message.reply_text(
                "Detail diterima.\n\n"
                f"{PAYMENT}"
            )

    async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = []

    for key, item in products.items():
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{item['name']} RM{item['price']}",
                    callback_data=key
                )
            ]
        )

    await query.edit_message_text(
        "🛒 Pilih produk:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def product_select(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global order_number

    query = update.callback_query
    await query.answer()

    key = query.data
    user = query.from_user

    product = products[key]

    order_id = order_number
    order_number += 1


    orders[order_id] = {
        "user_id": user.id,
        "username": user.username,
        "product": product["name"],
        "price": product["price"],
        "detail": {}
    }


    users[user.id] = {
        "order": order_id,
        "step": "detail"
    }


    if product["need"] == "none":

        users[user.id]["step"] = "payment"

        await query.edit_message_text(
            f"🧾 ORDER #{order_id}\n\n"
            f"Produk: {product['name']}\n"
            f"Harga: RM{product['price']}\n\n"
            f"{PAYMENT}"
        )


    elif product["need"] == "email":

        await query.edit_message_text(
            f"🧾 ORDER #{order_id}\n\n"
            f"Produk: {product['name']}\n"
            f"Harga: RM{product['price']}\n\n"
            "Sila masukkan email:"
        )


    else:

        await query.edit_message_text(
            f"🧾 ORDER #{order_id}\n\n"
            f"Produk: {product['name']}\n"
            f"Harga: RM{product['price']}\n\n"
            "Sila masukkan nama:"
        )



async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.message.from_user.id

    if uid not in users:
        return

    order_id = users[uid]["order"]
    order = orders[order_id]

    step = users[uid]["step"]


    if step == "detail":

        if "nama" not in order["detail"]:

            order["detail"]["nama"] = update.message.text

            if "YouTube" in order["product"]:

                await update.message.reply_text(
                    "Sila buat bayaran.\n\n"
                    f"{PAYMENT}"
                )

                users[uid]["step"] = "payment"

            else:

                await update.message.reply_text(
                    "Sila masukkan PIN 4 digit:"
                )


        else:

            order["detail"]["pin"] = update.message.text

            users[uid]["step"] = "payment"

            await update.message.reply_text(
                "Detail diterima.\n\n"
                f"{PAYMENT}"
            )
    )
