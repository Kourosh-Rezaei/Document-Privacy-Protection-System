from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please send me a DOCX/TXT file.")


async def handle_documnet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if (document.file_name.lower().endswith(".docx") or 
        document.file_name.lower().endswith("txt")):
        await update.message.reply_text(
            "File received.")
    
    else:
        await update.message.reply_text(
            "Please send a DOCX/TXT file.")
    

def main():
    application = Application.builder().token(
        "8628833548:AAEt1CC8MaPhMQq6pkpoDyyvx2aSuvSfAE8").build()
    
    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        MessageHandler(filters.Document.ALL, handle_documnet)
        )
    
    application.run_polling()



if __name__ == "__main__":
    main()