import json
import logging
import re
import shutil
import time
import uuid
from io import BytesIO
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_file
from werkzeug.exceptions import RequestEntityTooLarge

from functions import (
    open_excel,
    prepare_data,
    read_docx,
    read_pdf,
    read_txt,
    remove_phone_numbers_docx,
    remove_phone_numbers_pdf,
    remove_phone_numbers_txt,
)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

ALLOWED_EXTENSIONS = {".docx", ".txt", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024
JOB_TTL_SECONDS = 30 * 60
JOB_ID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def ensure_directories() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_expired_jobs() -> None:
    now = time.time()

    for folder in (UPLOAD_DIR, OUTPUT_DIR):
        if not folder.exists():
            continue

        for item in folder.iterdir():
            try:
                if now - item.stat().st_mtime > JOB_TTL_SECONDS:
                    if item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                    else:
                        item.unlink(missing_ok=True)
            except OSError:
                logger.warning("Could not clean expired item %s", item.name)


def is_allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def safe_download_stem(filename: str) -> str:
    stem = Path(filename).stem
    cleaned = re.sub(r"[^\w\-]+", "_", stem, flags=re.UNICODE).strip("._")
    return cleaned[:80] or "document"


def job_dir(job_id: str) -> Path:
    return (OUTPUT_DIR / job_id).resolve()


def validate_job_id(job_id: str) -> None:
    if not JOB_ID_PATTERN.fullmatch(job_id):
        abort(404)


def is_inside(parent: Path, child: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def read_job_meta(directory: Path) -> dict:
    meta_path = directory / "meta.json"
    if not meta_path.is_file():
        abort(404)

    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        abort(404)


def write_job_meta(directory: Path, meta: dict) -> None:
    (directory / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False),
        encoding="utf-8",
    )


def delete_upload(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        logger.warning("Could not delete upload %s", path.name)


def delete_job_if_empty(directory: Path) -> None:
    if not directory.is_dir():
        return

    remaining = [item for item in directory.iterdir() if item.name != "meta.json"]
    if remaining:
        return

    shutil.rmtree(directory, ignore_errors=True)


def extract_text(file_path: Path, suffix: str) -> str:
    if suffix == ".docx":
        return read_docx(str(file_path))
    if suffix == ".txt":
        return read_txt(str(file_path))
    return read_pdf(str(file_path))


def remove_phone_numbers(file_path: Path, output_path: Path, suffix: str) -> None:
    if suffix == ".docx":
        remove_phone_numbers_docx(str(file_path), str(output_path))
    elif suffix == ".txt":
        result = remove_phone_numbers_txt(str(file_path), str(output_path))
        if isinstance(result, str) and result.startswith("error:"):
            raise RuntimeError("unreadable file")
    else:
        result = remove_phone_numbers_pdf(str(file_path), str(output_path))
        if isinstance(result, str) and result.startswith("error:"):
            raise RuntimeError("unreadable file")


@app.before_request
def before_request() -> None:
    ensure_directories()
    cleanup_expired_jobs()


@app.errorhandler(RequestEntityTooLarge)
def too_large(_error):
    return jsonify({"ok": False, "error": "حجم فایل بیشتر از ۱۰ مگابایت است."}), 413


@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/download/") or request.path == "/process":
        return jsonify({"ok": False, "error": "فایل درخواستی پیدا نشد."}), 404
    return render_template("index.html"), 404


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    uploaded = request.files.get("document")
    if uploaded is None or not uploaded.filename:
        return jsonify({"ok": False, "error": "لطفاً یک فایل انتخاب کنید."}), 400

    original_name = uploaded.filename
    if not is_allowed_file(original_name):
        return jsonify({
            "ok": False,
            "error": "فقط فایل‌های DOCX، TXT و PDF پذیرفته می‌شوند.",
        }), 400

    suffix = Path(original_name).suffix.lower()
    job_id = str(uuid.uuid4())
    upload_path = UPLOAD_DIR / f"{job_id}{suffix}"
    output_folder = job_dir(job_id)

    logger.info("Processing job %s (%s)", job_id, suffix)

    try:
        uploaded.save(str(upload_path))

        if not upload_path.is_file() or upload_path.stat().st_size == 0:
            return jsonify({"ok": False, "error": "فایل خالی یا نامعتبر است."}), 400

        content = extract_text(upload_path, suffix)
        if not isinstance(content, str) or content.startswith("error:"):
            return jsonify({
                "ok": False,
                "error": "فایل خراب است یا قابل پردازش نیست.",
            }), 400

        data = prepare_data(content)

        output_folder.mkdir(parents=True, exist_ok=True)
        excel_path = output_folder / "extracted.xlsx"
        cleaned_path = output_folder / f"cleaned{suffix}"

        open_excel(str(excel_path), data)
        remove_phone_numbers(upload_path, cleaned_path, suffix)

        if not excel_path.is_file() or not cleaned_path.is_file():
            raise RuntimeError("output missing")

        stem = safe_download_stem(original_name)
        meta = {
            "ext": suffix,
            "excel_name": f"{stem}_extracted.xlsx",
            "cleaned_name": f"{stem}_without_phone{suffix}",
        }
        write_job_meta(output_folder, meta)

        return jsonify({
            "ok": True,
            "job_id": job_id,
            "record_count": len(data),
            "excel_url": f"/download/{job_id}/excel",
            "cleaned_url": f"/download/{job_id}/cleaned",
            "excel_name": meta["excel_name"],
            "cleaned_name": meta["cleaned_name"],
        })

    except Exception:
        logger.exception("Processing failed for job %s", job_id)
        if output_folder.exists():
            shutil.rmtree(output_folder, ignore_errors=True)
        return jsonify({
            "ok": False,
            "error": "فایل خراب است یا قابل پردازش نیست.",
        }), 400

    finally:
        delete_upload(upload_path)


@app.route("/download/<job_id>/<kind>")
def download(job_id: str, kind: str):
    validate_job_id(job_id)

    if kind not in {"excel", "cleaned"}:
        abort(404)

    directory = job_dir(job_id)
    if not is_inside(OUTPUT_DIR, directory) or not directory.is_dir():
        abort(404)

    meta = read_job_meta(directory)

    if kind == "excel":
        file_path = directory / "extracted.xlsx"
        download_name = meta.get("excel_name", "extracted.xlsx")
    else:
        suffix = meta.get("ext", "")
        if suffix not in ALLOWED_EXTENSIONS:
            abort(404)
        file_path = directory / f"cleaned{suffix}"
        download_name = meta.get("cleaned_name", f"cleaned{suffix}")

    file_path = file_path.resolve()
    if not is_inside(directory, file_path) or not file_path.is_file():
        abort(404)

    payload = BytesIO(file_path.read_bytes())

    try:
        file_path.unlink(missing_ok=True)
    except OSError:
        logger.warning("Could not delete download %s", file_path.name)

    delete_job_if_empty(directory)

    return send_file(
        payload,
        as_attachment=True,
        download_name=download_name,
    )


if __name__ == "__main__":
    ensure_directories()
    app.run(host="127.0.0.1", port=5000, debug=False)
