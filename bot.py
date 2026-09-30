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

<<<<<<< HEAD
    if (document.file_name.lower().endswith(".docx") or 
        document.file_name.lower().endswith("txt")):
        await update.message.reply_text(
            "File received.")
    
    else:
        await update.message.reply_text(
            "Please send a DOCX/TXT file.")
=======
    if document.file_name.lower().endswith(".docx"):
        await update.message.reply_text(
            "DOCX file received.")

    else:
        await update.message.reply_text(
            "Please send a DOCX file.")
>>>>>>> 11de35f889a27f44bd19352725eb372cf4a79e4f
    

def main():
    application = Application.builder().token(
        "8628833548:AAEt1CC8MaPhMQq6pkpoDyyvx2aSuvSfAE8").build()
    
    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        MessageHandler(filters.Document.ALL, handle_documnet)
        )
    
    application.run_polling()


<<<<<<< HEAD

if __name__ == "__main__":
=======
if name == "main":
>>>>>>> 11de35f889a27f44bd19352725eb372cf4a79e4f
    main()