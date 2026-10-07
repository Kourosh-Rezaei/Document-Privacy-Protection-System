from dotenv import load_dotenv

load_dotenv()

import os

token = os.getenv("BOT_TOKEN")

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from functions import (
    prepare_data,
    read_docx,
    remove_phone_numbers_docx,
    remove_phone_numbers_pdf,
    remove_phone_numbers_txt,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please send me a DOCX/TXT/PDF file.")


async def handle_documnet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if (document.file_name.lower().endswith(".docx") or 
        document.file_name.lower().endswith(".txt") or
        document.file_name.lower().endswith(".pdf")):


        file = await context.bot.get_file(document.file_id)

        file_path = f"input/{document.file_name}"
        await file.download_to_drive(file_path)

        content = read_docx(file_path)
        print(10 * "-", "CONTENT", 10 * "-")
        print(content)
    
        print()
        
        data = prepare_data(content)
        print(10 * "-", "DATA", 10 * "-")
        print(data)

        await update.message.reply_text("File received. Processing...")
    else:
        await update.message.reply_text(
            "Please send a DOCX/TXT/PDF file.")

  
def main():
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.Document.ALL,
handle_documnet))
    
    application.run_polling()



if __name__ == "__main__":
    main()