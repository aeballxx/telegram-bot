import os
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
OWNER_ID = 7413570612

ORDER_NUMBER = 1000


PRODUCTS = {
    "netflix_private": {
        "name": "Netflix Private",
        "price": 12,
        "detail": "pin"
    },
    "netflix_sharing": {
        "name": "Netflix Sharing",
        "price": 6,
        "detail": "none"
    },
    "youtube_private": {
        "name": "YouTube Private",
        "price": 5,
        "detail": "email"
    },
    "youtube_sharing": {
        "name": "YouTube Sharing",
        "price": 3,
        "detail": "email"
    },
    "hbo_private": {
        "name": "HBO Max Private",
        "price": 5,
        "detail": "pin"
    },
    "prime_private": {
        "name": "Prime Video Private",
        "price": 5,
        "detail": "pin"
    }
}


USER_DATA = {}


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
    )


async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = []

    for key, item in PRODUCTS.items():

        keyboard.append([
            InlineKeyboardButton(
                f"{item['name']} RM{item['price']}",
                callback_data=key
            )
        ])


    await query.message.reply_text(
        "📦 Pilih produk:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def choose_product(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global ORDER_NUMBER

    query = update.callback_query
    await query.answer()

    product_id = query.data
    product = PRODUCTS[product_id]

    user_id = query.from_user.id

    ORDER_NUMBER += 1

    USER_DATA[user_id] = {
        "order": ORDER_NUMBER,
        "product": product["name"],
        "price": product["price"],
        "detail_type": product["detail"]
    }


    await query.message.reply_text(
        f"🧾 Order #{ORDER_NUMBER}\n\n"
        f"Produk: {product['name']}\n"
        f"Harga: RM{product['price']}\n"
    )


    if product["detail"] == "pin":

        await query.message.reply_text(
            "Sila masukkan nama pendek:"
        )

        USER_DATA[user_id]["step"] = "name"


    elif product["detail"] == "email":

        await query.message.reply_text(
            "Sila masukkan email:"
        )

        USER_DATA[user_id]["step"] = "email"


    else:

        await show_payment(query.message)

async def show_payment(message):

    keyboard = [
        [
            InlineKeyboardButton(
                "🏦 Bank",
                callback_data="bank"
            )
        ],
        [
            InlineKeyboardButton(
                "🟩 QR Touch 'n Go",
                callback_data="tng"
            )
        ],
        [
            InlineKeyboardButton(
                "🟦 QR Bisnes",
                callback_data="bisnes"
            )
        ]
    ]

    await message.reply_text(
        "💳 Pilih cara bayaran:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def payment_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "bank":

        await query.message.reply_text(
            """
🏦 BAYARAN BANK

Bank:
No Akaun:
Nama:

Sila buat bayaran dan hantar bukti pembayaran 📸
"""
        )


    elif query.data == "tng":

        await query.message.reply_text(
            "🟩 QR Touch 'n Go\n"
            "Sila scan QR di bawah."
        )

        # letak file_id gambar QR TNG nanti di sini
        # await query.message.reply_photo("QR_TNG_FILE_ID")


    elif query.data == "bisnes":

        await query.message.reply_text(
            "🟦 QR Bisnes\n"
            "Sila scan QR di bawah."
        )

        # letak file_id gambar QR Bisnes nanti di sini
        # await query.message.reply_photo("QR_BISNES_FILE_ID")



async def user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in USER_DATA:
        return


    step = USER_DATA[user_id].get("step")


    if step == "name":
    USER_DATA[user_id]["name"] = update.message.text

    await update.message.reply_text(
        "Sila masukkan PIN 4 digit:"
    )

    USER_DATA[user_id]["step"] = "pin"

    elif step == "pin":

        USER_DATA[user_id]["pin"] = update.message.text

        USER_DATA[user_id]["step"] = "payment"

        await update.message.reply_text(
            "Detail diterima ✅"
        )

        await show_payment(update.message)



    elif step == "email":

        USER_DATA[user_id]["email"] = update.message.text

        USER_DATA[user_id]["step"] = "payment"

        await update.message.reply_text(
            "Email diterima ✅"
        )

        await show_payment(update.message)

async def payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in USER_DATA:
        return


    data = USER_DATA[user_id]


    text = f"""
🔔 ORDER BARU

🧾 ID Order: #{data['order']}

Produk: {data['product']}
Harga: RM{data['price']}

Nama: {data.get('name','-')}
PIN: {data.get('pin','-')}
Email: {data.get('email','-')}

Customer ID:
{user_id}

Status:
Menunggu semakan bayaran
"""


    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=text
    )


    await update.message.reply_text(
        "✅ Bukti bayaran diterima.\n\n"
        "Order sedang disemak oleh admin."
    )



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            products,
            pattern="products"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            choose_product
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            payment_choice,
            pattern="bank|tng|bisnes"
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            user_text
        )
    )


    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            payment_proof
        )
    )


    print("BOT ONLINE")

    await app.run_polling()



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
