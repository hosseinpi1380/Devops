# -*- coding: utf-8 -*-
"""مدل‌های پایگاه داده: کاربر، اتاق، رزرو و پرداخت"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    phone = Column(String(20))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reservations = relationship("Reservation", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String(20), unique=True, nullable=False)
    room_type = Column(String(50), nullable=False)   # مثلاً: تک‌نفره، دوتخته، سوئیت
    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, default=1)
    description = Column(Text, default="")
    is_active = Column(Boolean, default=True)  # آیا اتاق در دسترس فروش هست

    reservations = relationship("Reservation", back_populates="room")


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)

    status = Column(String(20), default="در انتظار پرداخت")
    # وضعیت‌ها: در انتظار پرداخت / تایید شده / لغو شده

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
    payment = relationship("Payment", back_populates="reservation", uselist=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), unique=True, nullable=False)

    amount = Column(Float, nullable=False)
    method = Column(String(30), default="کارت شبیه‌سازی‌شده")
    card_last4 = Column(String(4))
    transaction_id = Column(String(64), unique=True)
    status = Column(String(20), default="موفق")  # موفق / ناموفق
    paid_at = Column(DateTime, default=datetime.utcnow)

    reservation = relationship("Reservation", back_populates="payment")
