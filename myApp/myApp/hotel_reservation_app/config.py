# -*- coding: utf-8 -*-
"""
تنظیمات کلی برنامه رزرو هتل
--------------------------------
برای اتصال به PostgreSQL یا MySQL کافیست متغیر محیطی HOTEL_DB_URL را ست کنید
یا مقدار DATABASE_URL زیر را مستقیماً تغییر دهید.

نمونه‌ها:
  PostgreSQL:  postgresql+psycopg2://user:password@localhost:5432/hotel_db
  MySQL:       mysql+pymysql://user:password@localhost:3306/hotel_db
  SQLite (پیش‌فرض تست سریع بدون نیاز به سرور):
               sqlite:///hotel.db
"""

import os

# اگر پکیج python-dotenv نصب باشد، مقادیر فایل .env را در متغیرهای محیطی بارگذاری می‌کند
# (این کار برای اجرای برنامه خارج از داکر و خواندن رمزهای دیتابیس از .env لازم است)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# اگر متغیر محیطی تنظیم نشده باشد، به‌صورت پیش‌فرض از SQLite محلی استفاده می‌شود
# تا برنامه بدون نیاز به نصب سرور دیتابیس قابل اجرا باشد.
# برای استفاده واقعی از PostgreSQL یا MySQL، خط زیر را جایگزین کنید یا
# متغیر محیطی HOTEL_DB_URL را تنظیم نمایید.
DATABASE_URL = os.environ.get(
    "HOTEL_DB_URL",
    "sqlite:///hotel.db"
)

# مثال برای PostgreSQL (نیاز به: pip install psycopg2-binary):
# DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/hotel_db"

# مثال برای MySQL (نیاز به: pip install pymysql):
# DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/hotel_db"

APP_TITLE = "سیستم رزرو هتل"
APP_WIDTH = 1000
APP_HEIGHT = 650

CURRENCY = "تومان"
