# -*- coding: utf-8 -*-
"""صفحه انتخاب تاریخ ورود و خروج برای رزرو اتاق"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import get_session
from models import Room, Reservation
from config import CURRENCY


class BookingFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        ttk.Label(self, text="ثبت رزرو", font=("Tahoma", 18, "bold")).pack(pady=15)

        self.room_info_label = ttk.Label(self, text="", font=("Tahoma", 12))
        self.room_info_label.pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="تاریخ ورود (YYYY-MM-DD):").grid(row=0, column=0, sticky="e", padx=5, pady=8)
        self.checkin_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.checkin_var, width=20).grid(row=0, column=1, pady=8)

        ttk.Label(form, text="تاریخ خروج (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.checkout_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.checkout_var, width=20).grid(row=1, column=1, pady=8)

        self.total_label = ttk.Label(self, text="", font=("Tahoma", 13, "bold"), foreground="darkgreen")
        self.total_label.pack(pady=10)

        ttk.Button(self, text="محاسبه مبلغ", command=self.calculate_total).pack(pady=5)
        ttk.Button(self, text="ادامه و پرداخت", command=self.proceed_to_payment).pack(pady=10)
        ttk.Button(self, text="بازگشت", command=lambda: controller.show_frame("DashboardFrame")).pack()

        self.current_room = None
        self.total_price = 0

    def on_show(self):
        session = get_session()
        try:
            room = session.query(Room).get(self.controller.selected_room_id)
            if room is None:
                messagebox.showerror("خطا", "اتاق انتخاب‌شده یافت نشد.")
                self.controller.show_frame("DashboardFrame")
                return
            self.current_room = {
                "id": room.id, "room_number": room.room_number,
                "room_type": room.room_type, "price": room.price_per_night,
            }
            self.room_info_label.config(
                text=(f"اتاق {room.room_number} - {room.room_type} - "
                      f"{room.price_per_night:,.0f} {CURRENCY} در هر شب")
            )
        finally:
            session.close()

        self.checkin_var.set("")
        self.checkout_var.set("")
        self.total_label.config(text="")
        self.total_price = 0

    def _parse_dates(self):
        try:
            check_in = datetime.strptime(self.checkin_var.get().strip(), "%Y-%m-%d")
            check_out = datetime.strptime(self.checkout_var.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("خطا", "فرمت تاریخ باید به‌صورت YYYY-MM-DD باشد.")
            return None, None

        if check_out <= check_in:
            messagebox.showwarning("خطا", "تاریخ خروج باید بعد از تاریخ ورود باشد.")
            return None, None

        return check_in, check_out

    def calculate_total(self):
        check_in, check_out = self._parse_dates()
        if not check_in:
            return
        nights = (check_out - check_in).days
        self.total_price = nights * self.current_room["price"]
        self.total_label.config(
            text=f"تعداد شب‌ها: {nights} | مبلغ کل: {self.total_price:,.0f} {CURRENCY}"
        )

    def proceed_to_payment(self):
        check_in, check_out = self._parse_dates()
        if not check_in:
            return

        if self.total_price == 0:
            self.calculate_total()
            if self.total_price == 0:
                return

        session = get_session()
        try:
            # بررسی تداخل تاریخ با رزروهای تایید شده همان اتاق
            overlapping = session.query(Reservation).filter(
                Reservation.room_id == self.current_room["id"],
                Reservation.status != "لغو شده",
                Reservation.check_in < check_out,
                Reservation.check_out > check_in,
            ).first()
            if overlapping:
                messagebox.showerror("خطا", "این اتاق در بازه تاریخی انتخاب‌شده قبلاً رزرو شده است.")
                return

            reservation = Reservation(
                user_id=self.controller.current_user_id,
                room_id=self.current_room["id"],
                check_in=check_in,
                check_out=check_out,
                total_price=self.total_price,
                status="در انتظار پرداخت",
            )
            session.add(reservation)
            session.commit()
            self.controller.pending_reservation_id = reservation.id
        finally:
            session.close()

        self.controller.show_frame("PaymentFrame")
