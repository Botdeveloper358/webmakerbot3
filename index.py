import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

TELEGRAM_TOKEN = "7893147721:AAHH2aQRfU6ZgkfeTVj78EiHRZFqhcqODvo"

users = {}

# ✅ Auto Create Folder for Photos
if not os.path.exists("pfp"):
    os.makedirs("pfp")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send(update, "🚀 Welcome to WebmakerBot!\n\nCommands:\n/register - Register\n/get - Get Referral\n/website - Set Website\n/publish - Publish\n/pfp - Set Profile Pic\n/help - Help")

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users[user_id] = {}
    context.user_data["awaiting_email"] = True
    await safe_send(update, "📩 Please enter your email:")

async def get_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send(update, "🎁 Your Referral Code: ABC123")

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send(update, "🌐 Website command used!")

async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send(update, "📤 Your website has been published!")

async def pfp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send(update, "🖼️ Please send your profile picture now.")
    context.user_data["awaiting_pfp"] = True

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_pfp"):
        user_id = str(update.effective_user.id)
        photo = update.message.photo[-1]
        file = await photo.get_file()
        photo_path = f"pfp/{user_id}.jpg"
        await file.download_to_drive(photo_path)
        await update.message.reply_text("✅ Profile picture uploaded and saved successfully!")
        context.user_data["awaiting_pfp"] = False
    else:
        await update.message.reply_text("❌ Unexpected photo! Use /pfp to upload profile picture.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_send(update, "ℹ️ Help:\n/start - Start\n/register - Register\n/get - Get Referral\n/website - Set Website\n/publish - Publish\n/pfp - Set Profile Pic")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if context.user_data.get("awaiting_email"):
        email = update.message.text
        users[user_id] = {"email": email}
        context.user_data["awaiting_email"] = False
        context.user_data["awaiting_site"] = True
        await safe_send(update, "🌐 Please enter your website name:")
    elif context.user_data.get("awaiting_site"):
        site_name = update.message.text
        users[user_id]["website_name"] = site_name
        context.user_data["awaiting_site"] = False
        await safe_send(update, f"✅ Info Saved!\n📩 Email: {users[user_id]['email']}\n🌐 Website: {site_name}")
    else:
        await safe_send(update, "❌ Unrecognized Input!")

async def safe_send(update: Update, text: str):
    if update.message:
        await update.message.reply_text(text)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text)
    else:
        await update.effective_chat.send_message(text)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("register", register))
app.add_handler(CommandHandler("get", get_referral))
app.add_handler(CommandHandler("website", website))
app.add_handler(CommandHandler("publish", publish))
app.add_handler(CommandHandler("pfp", pfp))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

print("✅ Bot Started!")
app.run_polling()
