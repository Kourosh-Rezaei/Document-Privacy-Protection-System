import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import os

token = os.getenv("BOT_TOKEN")

import pymupdf
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.request import HTTPXRequest

from functions import (
    open_excel,
    prepare_data,
    read_docx,
    remove_phone_numbers_docx,
    remove_phone_numbers_pdf,
    remove_phone_numbers_txt,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please send me a DOCX/TXT/PDF file.")


async def handle_documnet(update: Update,context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    print("\n[STEP 1] File received")
    print(f"[INFO] Filename: {document.file_name}")

    if not document.file_name.lower().endswith((".docx", ".txt", ".pdf")):
        print("[ERROR] Unsupported file format")
        await update.message.reply_text("Please send a DOCX/TXT/PDF file.")
        return

    print("\n[STEP 2] Creating directories...")

    input_dir = Path("input")
    output_dir = Path("output")

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid.uuid4().hex
    file_path = input_dir / f"{file_id}_{document.file_name}"
    excel_path = output_dir / f"{file_id}_{document.file_name}.xlsx"
    clean_file_path = output_dir / f"{file_id}_{document.file_name}"

    print("[DONE] Directories ready")
    print("\n[STEP 3] Downloading file...")

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(str(file_path))

    print(f"[DONE] File saved: {file_path}")

    await update.message.reply_text(
        "File received. Processing...")

    print("\n[STEP 4] Extracting content...")

    suffix = Path(document.file_name).suffix.lower()

    if suffix == ".docx":
        content = read_docx(str(file_path))

    elif suffix == ".txt":
        content = Path(file_path).read_text(encoding="utf-8")

    elif suffix == ".pdf":
        with pymupdf.open(str(file_path)) as pdf: 
            content = "\n".join(page.get_text()for page in pdf)

    print("[DONE] Content extracted")
    print()
    print("-" * 10, "CONTENT", "-" * 10)
    print(content)

    print("\n[STEP 5] Preparing data...")
    data = prepare_data(content)

    print("[DONE] Data prepared")
    print()
    print("-" * 10, "DATA", "-" * 10)
    print(data)

    print("\n[STEP 6] Creating Excel file...")
    open_excel(str(excel_path), data)

    print(f"[DONE] Excel saved: {excel_path}")

    print("\n[STEP 7] Removing phone numbers...")

    if suffix == ".docx":
        remove_phone_numbers_docx(
            str(file_path),
            str(clean_file_path))
        
    elif suffix == ".txt":
        remove_phone_numbers_txt(
            str(file_path),
            str(clean_file_path))
        
    elif suffix == ".pdf":
        remove_phone_numbers_pdf(
            str(file_path),
            str(clean_file_path))

    print(f"[DONE] Clean file saved: {clean_file_path}")

    print("\n[STEP 8] Sending files to Telegram...")

    await update.message.reply_text(
    "✅ Your file has been processed successfully!\n\n"
    "📊 The Excel file containing the extracted data is ready.\n"
    "🛡️ The cleaned version of your file is also ready.\n\n"
    "I will send both files to you now.")

    await update.message.reply_document(
    document=str(excel_path),
    caption="📊 Excel file containing the extracted data")

    await update.message.reply_document(
    document=str(clean_file_path),
    caption="🛡️ Cleaned file — phone numbers have been removed.")

    await update.message.reply_text(
    "🎉 Both files have been sent successfully!\n\n"
    "To process another file, simply send it to me.")

    print("[DONE] All steps completed successfully")


def main():
    if not token:
        raise RuntimeError("BOT_TOKEN is not set in .env")

    print("Waiting for user input...")

    request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=20,
        media_write_timeout=120)

    updates_request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=20)

    application = (
        Application.builder()
        .token(token)
        .request(request)
        .get_updates_request(updates_request)
        .build())

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_documnet))

    print("Bot is starting...")

    application.run_polling(
        timeout=20,
        bootstrap_retries=3)


if __name__ == "__main__":
    main()
