# -*- coding: utf-8 -*-
"""درج داده‌های نمونه: اتاق‌ها و یک کاربر ادمین پیش‌فرض"""

from database import init_db, get_session
from models import Room, User
from auth import hash_password


def seed():
    init_db()
    session = get_session()
    try:
        if session.query(Room).count() == 0:
            rooms = [
                Room(room_number="101", room_type="تک‌نفره", price_per_night=850000,
                     capacity=1, description="اتاق تک‌نفره با چشم‌انداز شهر"),
                Room(room_number="102", room_type="دوتخته", price_per_night=1250000,
                     capacity=2, description="اتاق دوتخته استاندارد"),
                Room(room_number="201", room_type="سوئیت", price_per_night=2400000,
                     capacity=3, description="سوئیت لوکس با اتاق نشیمن جدا"),
                Room(room_number="202", room_type="دوتخته", price_per_night=1350000,
                     capacity=2, description="اتاق دوتخته با بالکن"),
                Room(room_number="301", room_type="خانوادگی", price_per_night=3100000,
                     capacity=4, description="اتاق خانوادگی بزرگ با دو اتاق‌خواب"),
            ]
            session.add_all(rooms)

        if session.query(User).filter_by(username="admin").first() is None:
            admin = User(
                full_name="مدیر سیستم",
                username="admin",
                password_hash=hash_password("admin123"),
                phone="00000000000",
                is_admin=True,
            )
            session.add(admin)

        session.commit()
        print("داده‌های اولیه با موفقیت درج شد.")
        print("کاربر ادمین -> نام کاربری: admin | رمز عبور: admin123")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
