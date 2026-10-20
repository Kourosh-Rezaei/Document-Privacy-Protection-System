const form = document.getElementById("upload-form");
const fileInput = document.getElementById("document");
const fileName = document.getElementById("file-name");
const submitBtn = document.getElementById("submit-btn");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const resultSummary = document.getElementById("result-summary");
const excelLink = document.getElementById("excel-link");
const cleanedLink = document.getElementById("cleaned-link");
const dropzone = document.getElementById("dropzone");

const allowed = [".docx", ".txt", ".pdf"];
const maxSize = 10 * 1024 * 1024;

function extensionOf(name) {
    const index = name.lastIndexOf(".");
    return index === -1 ? "" : name.slice(index).toLowerCase();
}

function showStatus(message, type) {
    statusEl.hidden = false;
    statusEl.textContent = message;
    statusEl.className = `status ${type || ""}`.trim();
}

function hideResult() {
    resultEl.hidden = true;
}

function assignFile(file) {
    if (!file) {
        return;
    }

    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
    fileInput.dispatchEvent(new Event("change"));
}

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    fileName.textContent = file ? file.name : "هنوز فایلی انتخاب نشده است.";
    hideResult();
    statusEl.hidden = true;
});

console.log("dropzone:", dropzone);
console.log("form:", form);
console.log("fileInput =", fileInput);

if (dropzone) {
    ["dragenter", "dragover"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.add("is-dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.remove("is-dragover");
        });
    });
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    hideResult();

    const file = fileInput.files[0];
    if (!file) {
        showStatus("لطفاً یک فایل انتخاب کنید.", "error");
        return;
    }

    if (!allowed.includes(extensionOf(file.name))) {
        showStatus("فقط فایل‌های DOCX، TXT و PDF پذیرفته می‌شوند.", "error");
        return;
    }

    if (file.size > maxSize) {
        showStatus("حجم فایل بیشتر از ۱۰ مگابایت است.", "error");
        return;
    }

    const data = new FormData();
    data.append("document", file);

    submitBtn.disabled = true;
    showStatus("در حال پردازش فایل...", "");

    try {
        const response = await fetch("/process", {
            method: "POST",
            body: data,
        });

        let payload = {};
        try {
            payload = await response.json();
        } catch (_error) {
            payload = {};
        }

        if (!response.ok || !payload.ok) {
            showStatus(payload.error || "پردازش فایل انجام نشد.", "error");
            return;
        }

        const count = payload.record_count || 0;
        resultSummary.textContent = count
            ? `${count} مورد نام و شماره تلفن استخراج شد.`
            : "موردی مطابق الگوی فعلی پیدا نشد. فایل Excel و نسخهٔ پاک‌سازی‌شده آماده هستند.";

        excelLink.href = payload.excel_url;
        excelLink.setAttribute("download", payload.excel_name);
        cleanedLink.href = payload.cleaned_url;
        cleanedLink.setAttribute("download", payload.cleaned_name);

        resultEl.hidden = false;
        showStatus("پردازش با موفقیت انجام شد.", "success");
    } catch (_error) {
        showStatus("ارتباط با سرور برقرار نشد.", "error");
    } finally {
        submitBtn.disabled = false;
    }
});
