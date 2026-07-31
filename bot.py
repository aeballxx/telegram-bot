import os
import random
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")

ADMIN_USERNAME = "@x_aebal"


# =====================
# BAYARAN
# =====================

PAYMENT = """
💳 BAYARAN

Bank: 
No Akaun:

Nama:

Sila buat bayaran dan hantar bukti pembayaran.
"""


# =====================
# PRODUK
# =====================

PRODUCTS = {

    "netflix_private": {
        "name": "Netflix Private",
        "price": 12,
        "detail": True,
        "type": "name_pin"
    },

    "netflix_share": {
        "name": "Netflix Sharing",
        "price": 6,
        "detail": False
    },

    "youtube_private": {
        "name": "YouTube Private",
        "price": 5,
        "detail": True,
        "type": "email"
    },

    "youtube_share": {
        "name": "YouTube Sharing",
        "price": 3,
        "detail": True,
        "type": "email"
    },

    "hbo_private": {
        "name": "HBO Max Private",
        "price": 5,
        "detail": True,
        "type": "name_pin"
    },

    "prime_private": {
        "name": "Prime Video Private",
        "price": 5,
        "detail": True,
        "type": "name_pin"
    }

}


ORDERS = {}

USER_STATE = {}

ORDER_NUMBER = 1000


# =====================
# START
# =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Order Produk",
                callback_data="products"
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Selamat datang ke Premium Store\n\n"
        "Tekan butang untuk buat order.",
        reply_markup=InlineKeyboardMarkup(keyboard)

        # =====================
# BUTTON PRODUK
# =====================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global ORDER_NUMBER

    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user


    # PAPAR PRODUK

    if data == "products":

        keyboard = []

        for key, item in PRODUCTS.items():

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

        return



    # PILIH PRODUK

    if data in PRODUCTS:

        product = PRODUCTS[data]

        order_id = ORDER_NUMBER
        ORDER_NUMBER += 1


        ORDERS[order_id] = {
            "user_id": user.id,
            "username": user.username,
            "product": product["name"],
            "price": product["price"],
            "detail": {}
        }


        USER_STATE[user.id] = {
            "order_id": order_id,
            "step": "detail"
        }


        if product["detail"]:

            if product["type"] == "name_pin":

                await query.edit_message_text(
                    f"🧾 Order #{order_id}\n\n"
                    f"Produk: {product['name']}\n"
                    f"Harga: RM{product['price']}\n\n"
                    "Sila masukkan nama pendek:"
                )

            elif product["type"] == "email":

                await query.edit_message_text(
                    f"🧾 Order #{order_id}\n\n"
                    f"Produk: {product['name']}\n"
                    f"Harga: RM{product['price']}\n\n"
                    "Sila masukkan email:"
                )

        else:

            await query.edit_message_text(
                f"🧾 Order #{order_id}\n\n"
                f"Produk: {product['name']}\n"
                f"Harga: RM{product['price']}\n\n"
                f"{PAYMENT}"
            )

            USER_STATE[user.id]["step"] = "payment"


        return



# =====================
# INPUT CUSTOMER
# =====================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    uid = user.id

    if uid not in USER_STATE:
        return


    state = USER_STATE[uid]
    order_id = state["order_id"]

    order = ORDERS[order_id]


    if state["step"] == "detail":

        product = order["product"]


        if "nama" not in order["detail"]:

            order["detail"]["nama"] = update.message.text


            if "Netflix" in product or "HBO" in product or "Prime" in product:

                await update.message.reply_text(
                    "Sila masukkan PIN 4 digit:"
                )

            else:

                await update.message.reply_text(
                    "Sila buat bayaran.\n\n"
                    f"{PAYMENT}"
                )

                state["step"] = "payment"


        else:

            order["detail"]["pin"] = update.message.text


            await update.message.reply_text(
                "Detail diterima.\n\n"
                f"{PAYMENT}"
            )

            state["step"] = "payment"


        return

# =====================
# BUKTI BAYARAN
# =====================

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.message.from_user.id

    if uid not in USER_STATE:
        return

    order_id = USER_STATE[uid]["order_id"]
    order = ORDERS[order_id]


    now = datetime.now()

    text = (
        "🔔 ORDER BARU\n\n"
        f"ID: #{order_id}\n"
        f"Produk: {order['product']}\n"
        f"Harga: RM{order['price']}\n\n"
        f"Nama: {order['detail'].get('nama','-')}\n"
        f"PIN/Email: {order['detail'].get('pin','-')}\n\n"
        f"Tarikh: {now.strftime('%d/%m/%Y')}\n"
        f"Masa: {now.strftime('%H:%M')}\n\n"
        f"Customer: @{order['username']}"
    )


    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Detail Dah Diberi",
                callback_data=f"done_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Tolak",
                callback_data=f"reject_{order_id}"
            )
        ]
    ]


    await context.bot.send_photo(
        chat_id=ADMIN_USERNAME,
        photo=update.message.photo[-1].file_id,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


    await update.message.reply_text(
        "✅ Bukti bayaran diterima.\n"
        "Sila tunggu pengesahan admin."
    )



# =====================
# ADMIN BUTTON
# =====================

async def admin_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data.startswith("done_"):

        order_id = query.data.split("_")[1]

        order = ORDERS[int(order_id)]


        await context.bot.send_message(
            chat_id=order["user_id"],
            text=(
                "✅ ORDER SELESAI\n\n"
                "Terima kasih kerana membeli bersama kami 🙏\n\n"
                "Detail order anda telah diberikan."
            )
        )


        await query.edit_message_caption(
            caption="✅ Selesai. Customer telah dimaklumkan."
        )


    elif query.data.startswith("reject_"):

        order_id = query.data.split("_")[1]

        order = ORDERS[int(order_id)]


        await context.bot.send_message(
            chat_id=order["user_id"],
            text=(
                "❌ Order ditolak.\n"
                "Sila hubungi admin."
            )
        )


        await query.edit_message_caption(
            caption="❌ Order ditolak."
        )



# =====================
# RUN BOT
# =====================

app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(buttons)
)

app.add_handler(
    CallbackQueryHandler(admin_button)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message
    )
)

app.add_handler(
    MessageHandler(
        filters.PHOTO,
        photo
    )
)


print("BOT ONLINE")

app.run_polling()


    
