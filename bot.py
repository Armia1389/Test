import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

PASSWORD = "@NetliVPN"

CHANNEL_ID = -1001929829906

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Select location")

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text
    context.user_data['location'] = location

    await update.message.reply_text(
        f"✅ Location saved: {location}\n"
        f"🔑 Password: {PASSWORD}\n"
        "Now send the file or photo to forward to the channel."
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'location' not in context.user_data:
        await update.message.reply_text("❌ Please enter location first.\nExample: Finland🇫🇮")
        return

    document = update.message.document
    location = context.user_data['location']

    caption = (
        f"🔑Password:{PASSWORD}\n\n"
        f"🌐Location:{location}\n\n"
        f"📥دانلود اپلیکیشن مورد نیاز:"
    )

    keyboard = [
        [InlineKeyboardButton("📱 اندروید", url="https://play.google.com/store/apps/details?id=com.napsternetlabs.napsternetv")],
        [InlineKeyboardButton("🍏 آیفون و آیپد (iOS)", url="https://apps.apple.com/us/app/npv-tunnel/id1629465476")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_document(
        chat_id=CHANNEL_ID,
        document=document.file_id,
        caption=caption,
        reply_markup=reply_markup
    )

    await update.message.reply_text("✅ File sent to channel successfully.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'location' not in context.user_data:
        await update.message.reply_text("❌ Please enter location first.\nExample: Finland🇫🇮")
        return

    photo = update.message.photo[-1]
    location = context.user_data['location']

    caption = (
        f"🔑Password:{PASSWORD}\n\n"
        f"🌐Location:{location}\n\n"
        f"📥دانلود اپلیکیشن مورد نیاز:"
    )

    keyboard = [
        [InlineKeyboardButton("📱 اندروید", url="https://play.google.com/store/apps/details?id=com.napsternetlabs.napsternetv")],
        [InlineKeyboardButton("🍏 آیفون و آیپد (iOS)", url="https://apps.apple.com/us/app/npv-tunnel/id1629465476")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=photo.file_id,
        caption=caption,
        reply_markup=reply_markup
    )

    await update.message.reply_text("✅ Photo sent to channel successfully.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()