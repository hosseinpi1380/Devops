# -*- coding: utf-8 -*-
"""صفحه پرداخت درون‌برنامه‌ای (شبیه‌سازی‌شده)"""

import tkinter as tk
from tkinter import ttk, messagebox

from database import get_session
from models import Reservation, Payment
from payment_service import MockPaymentGateway, PaymentError
from config import CURRENCY


class PaymentFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        ttk.Label(self, text="پرداخت رزرو", font=("Tahoma", 18, "bold")).pack(pady=15)
        ttk.Label(self, text="⚠ این یک درگاه پرداخت شبیه‌سازی‌شده برای تست است، پرداخت واقعی انجام نمی‌شود.",
                  foreground="orange").pack(pady=5)

        self.summary_label = ttk.Label(self, text="", font=("Tahoma", 12, "bold"))
        self.summary_label.pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="شماره کارت (۱۶ رقم):").grid(row=0, column=0, sticky="e", padx=5, pady=8)
        self.card_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.card_var, width=25).grid(row=0, column=1, pady=8)

        ttk.Label(form, text="تاریخ انقضا (MM/YY):").grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.expiry_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.expiry_var, width=25).grid(row=1, column=1, pady=8)

        ttk.Label(form, text="CVV2:").grid(row=2, column=0, sticky="e", padx=5, pady=8)
        self.cvv_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.cvv_var, show="*", width=25).grid(row=2, column=1, pady=8)

        ttk.Button(self, text="پرداخت", command=self.pay).pack(pady=15)
        ttk.Button(self, text="انصراف و بازگشت",
                   command=lambda: controller.show_frame("DashboardFrame")).pack()

        ttk.Label(self, text="نکته آزمایشی: کارتی که با 0000 شروع شود، تراکنش ناموفق شبیه‌سازی می‌کند.",
                  foreground="gray").pack(pady=10)

        self.reservation = None

    def on_show(self):
        session = get_session()
        try:
            reservation = session.query(Reservation).get(self.controller.pending_reservation_id)
            self.reservation = {
                "id": reservation.id,
                "total_price": reservation.total_price,
                "room_number": reservation.room.room_number,
            }
            self.summary_label.config(
                text=(f"اتاق {self.reservation['room_number']} | "
                      f"مبلغ قابل پرداخت: {self.reservation['total_price']:,.0f} {CURRENCY}")
            )
        finally:
            session.close()

        self.card_var.set("")
        self.expiry_var.set("")
        self.cvv_var.set("")

    def pay(self):
        try:
            result = MockPaymentGateway.charge(
                card_number=self.card_var.get(),
                expiry=self.expiry_var.get(),
                cvv=self.cvv_var.get(),
                amount=self.reservation["total_price"],
            )
        except PaymentError as e:
            messagebox.showerror("پرداخت ناموفق", str(e))
            return

        session = get_session()
        try:
            reservation = session.query(Reservation).get(self.reservation["id"])
            reservation.status = "تایید شده"

            payment = Payment(
                reservation_id=reservation.id,
                amount=reservation.total_price,
                method="کارت شبیه‌سازی‌شده",
                card_last4=result["card_last4"],
                transaction_id=result["transaction_id"],
                status=result["status"],
            )
            session.add(payment)
            session.commit()
        finally:
            session.close()

        messagebox.showinfo(
            "پرداخت موفق",
            f"رزرو شما با موفقیت تایید شد.\nشناسه تراکنش: {result['transaction_id']}"
        )
        self.controller.show_frame("HistoryFrame")
