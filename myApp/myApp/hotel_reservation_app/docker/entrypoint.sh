#!/bin/sh
set -e

echo "در حال بررسی اتصال به دیتابیس..."

python3 - << 'PYEOF'
import time
from sqlalchemy import create_engine, text
from config import DATABASE_URL

for attempt in range(30):
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("اتصال به دیتابیس برقرار شد.")
        break
    except Exception as e:
        print(f"دیتابیس هنوز آماده نیست، تلاش {attempt + 1}/30 ...")
        time.sleep(2)
else:
    raise SystemExit("اتصال به دیتابیس برقرار نشد.")
PYEOF

echo "ساخت جداول و درج داده اولیه (در صورت نیاز)..."
python3 seed.py

echo "اجرای برنامه..."
exec python3 main.py
