# -*- coding: utf-8 -*-
"""صفحه تاریخچه رزروهای کاربر جاری"""

from tkinter import ttk, messagebox

from database import get_session
from models import Reservation
from config import CURRENCY


class HistoryFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="تاریخچه رزروهای من", font=("Tahoma", 18, "bold")).pack(pady=15)

        columns = ("id", "room_number", "check_in", "check_out", "total_price", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=14)
        headings = {
            "id": "شناسه رزرو", "room_number": "شماره اتاق", "check_in": "ورود",
            "check_out": "خروج", "total_price": f"مبلغ ({CURRENCY})", "status": "وضعیت",
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=140, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)

        btn_bar = ttk.Frame(self)
        btn_bar.pack(pady=10)
        ttk.Button(btn_bar, text="لغو رزرو انتخاب‌شده", command=self.cancel_reservation).pack(side="right", padx=5)
        ttk.Button(btn_bar, text="بازگشت به صفحه اصلی",
                   command=lambda: controller.show_frame("DashboardFrame")).pack(side="right", padx=5)

    def on_show(self):
        self.load_history()

    def load_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        session = get_session()
        try:
            reservations = session.query(Reservation).filter_by(
                user_id=self.controller.current_user_id
            ).order_by(Reservation.created_at.desc()).all()

            for r in reservations:
                self.tree.insert("", "end", values=(
                    r.id, r.room.room_number,
                    r.check_in.strftime("%Y-%m-%d"),
                    r.check_out.strftime("%Y-%m-%d"),
                    f"{r.total_price:,.0f}", r.status
                ))
        finally:
            session.close()

    def cancel_reservation(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("خطا", "لطفاً یک رزرو را انتخاب کنید.")
            return

        reservation_id = self.tree.item(selected[0])["values"][0]
        status = self.tree.item(selected[0])["values"][5]

        if status == "لغو شده":
            messagebox.showinfo("توجه", "این رزرو قبلاً لغو شده است.")
            return

        if not messagebox.askyesno("تایید لغو", "آیا از لغو این رزرو مطمئن هستید؟"):
            return

        session = get_session()
        try:
            reservation = session.query(Reservation).get(int(reservation_id))
            reservation.status = "لغو شده"
            session.commit()
        finally:
            session.close()

        self.load_history()
