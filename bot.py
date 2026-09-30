from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please send me a DOCX file.")


def main():
    application = Application.builder().token(
        "8628833548:AAEaLIYROEyeZPcWdMZAtQbalV41q1Xp94s").build()
    
    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == "__main__":
    main()