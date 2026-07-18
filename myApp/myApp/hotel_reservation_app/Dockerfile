FROM python:3.11-slim-bookworm

# نصب کتابخانه‌های اجرایی Tk/Tcl (لازم برای import tkinter) و ابزار انتظار برای دیتابیس
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-tk \
        tk \
        libx11-6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
