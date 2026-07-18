# -*- coding: utf-8 -*-
"""راه‌اندازی اتصال به پایگاه داده (SQLite / PostgreSQL / MySQL)"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base

# برای SQLite نیاز به یک آرگومان خاص است تا در برنامه‌های چندریسمانی/GUI مشکلی پیش نیاید
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    """ساخت تمام جداول در صورت عدم وجود"""
    Base.metadata.create_all(bind=engine)


def get_session():
    """گرفتن یک session جدید برای کار با دیتابیس"""
    return SessionLocal()
