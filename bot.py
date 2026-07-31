async def choose_product(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global order_id

    query = update.callback_query
    await query.answer()

    product_id = query.data

    if product_id not in PRODUCTS:
        return

    product = PRODUCTS[product_id]

    user_id = query.from_user.id

    order_id += 1

    orders[order_id] = {
        "user_id": user_id,
        "product": product["name"],
        "price": product["price"],
        "detail": {}
    }

    users[user_id] = {
        "order": order_id,
        "step": product["type"]
    }

    await query.message.reply_text(
        f"🧾 ORDER #{order_id}\n\n"
        f"Produk: {product['name']}\n"
        f"Harga: RM{product['price']}"
    )

    if product["type"] == "pin":

        await query.message.reply_text(
            "Sila masukkan nama pendek:"
        )

        users[user_id]["step"] = "name"

    elif product["type"] == "email":

        await query.message.reply_text(
            "Sila masukkan email:"
        )

        users[user_id]["step"] = "email"

    else:

        await payment_menu(query.message)

async def payment_menu(message):

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

async def choose_product(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global order_id

    query = update.callback_query
    await query.answer()

    product_id = query.data

    if product_id not in PRODUCTS:
        return

    product = PRODUCTS[product_id]

    user_id = query.from_user.id

    order_id += 1

    orders[order_id] = {
        "user_id": user_id,
        "product": product["name"],
        "price": product["price"],
        "detail": {}
    }

    users[user_id] = {
        "order": order_id,
        "step": product["type"]
    }

    await query.message.reply_text(
        f"🧾 ORDER #{order_id}\n\n"
        f"Produk: {product['name']}\n"
        f"Harga: RM{product['price']}"
    )

    if product["type"] == "pin":

        await query.message.reply_text(
            "Sila masukkan nama pendek:"
        )

        users[user_id]["step"] = "name"

    elif product["type"] == "email":

        await query.message.reply_text(
            "Sila masukkan email:"
        )

        users[user_id]["step"] = "email"

    else:

        await payment_menu(query.message)

async def payment_menu(message):

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
            BANK_INFO
        )

    elif query.data == "tng":

        await query.message.reply_text(
            "🟩 QR Touch 'n Go\n\n"
            "Sila scan QR dan hantar bukti bayaran."
        )

        # Nanti letak gambar QR TNG di sini

    elif query.data == "bisnes":

        await query.message.reply_text(
            "🟦 QR Bisnes\n\n"
            "Sila scan QR dan hantar bukti bayaran."
        )

        # Nanti letak gambar QR Bisnes di sini

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in users:
        return

    step = users[user_id]["step"]

    order = orders[users[user_id]["order"]]

    if step == "name":

        order["detail"]["name"] = update.message.text

        users[user_id]["step"] = "pin"

        await update.message.reply_text(
            "Sila masukkan PIN 4 digit:"
        )

    elif step == "pin":

        order["detail"]["pin"] = update.message.text

        users[user_id]["step"] = "payment"

        await update.message.reply_text(
            "Detail diterima ✅"
        )

        await payment_menu(update.message)

    elif step == "email":

        order["detail"]["email"] = update.message.text

        users[user_id]["step"] = "payment"

        await update.message.reply_text(
            "Email diterima ✅"
        )

        await payment_menu(update.message)

async def proof_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in users:
        return

    order_no = users[user_id]["order"]

    order = orders[order_no]

    detail = order["detail"]

    msg = f"""
🔔 ORDER BARU

🧾 Order ID: #{order_no}

Produk:
{order['product']}

Harga:
RM{order['price']}

Detail:
Nama: {detail.get('name','-')}
PIN: {detail.get('pin','-')}
Email: {detail.get('email','-')}

Customer ID:
{user_id}

Status:
Menunggu semakan bayaran
"""

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=msg
    )

    await update.message.reply_text(
        "✅ Bukti bayaran diterima.\n\n"
        "Admin akan semak order anda."
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
            shop,
            pattern="shop"
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
            text_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            proof_payment
        )
    )

    print("BOT ONLINE")

    app.run_polling()

if __name__ == "__main__":
    main()
