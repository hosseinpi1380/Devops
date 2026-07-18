# -*- coding: utf-8 -*-
"""صفحه اصلی: لیست اتاق‌ها، جستجو و دسترسی به تاریخچه رزرو"""

import tkinter as tk
from tkinter import ttk, messagebox

from database import get_session
from models import Room
from config import CURRENCY


class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        top_bar = ttk.Frame(self)
        top_bar.pack(fill="x", pady=(0, 10))

        self.welcome_label = ttk.Label(top_bar, text="", font=("Tahoma", 14, "bold"))
        self.welcome_label.pack(side="right")

        ttk.Button(top_bar, text="تاریخچه رزروهای من",
                   command=lambda: controller.show_frame("HistoryFrame")).pack(side="left", padx=4)
        self.admin_btn = ttk.Button(top_bar, text="پنل مدیریت اتاق‌ها",
                                     command=lambda: controller.show_frame("AdminFrame"))
        ttk.Button(top_bar, text="خروج", command=self.logout).pack(side="left", padx=4)

        # جستجو
        search_bar = ttk.Frame(self)
        search_bar.pack(fill="x", pady=10)
        ttk.Label(search_bar, text="جستجو بر اساس نوع اتاق:").pack(side="right", padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_bar, textvariable=self.search_var, width=25)
        search_entry.pack(side="right", padx=5)
        ttk.Button(search_bar, text="جستجو", command=self.load_rooms).pack(side="right", padx=5)
        ttk.Button(search_bar, text="نمایش همه", command=self.clear_search).pack(side="right", padx=5)

        # جدول اتاق‌ها
        columns = ("id", "room_number", "room_type", "capacity", "price", "description")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=14)
        headings = {
            "id": "شناسه", "room_number": "شماره اتاق", "room_type": "نوع اتاق",
            "capacity": "ظرفیت", "price": f"قیمت هر شب ({CURRENCY})", "description": "توضیحات",
        }
        widths = {"id": 50, "room_number": 90, "room_type": 100, "capacity": 70,
                  "price": 140, "description": 300}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)

        ttk.Button(self, text="رزرو اتاق انتخاب‌شده",
                   command=self.go_to_booking).pack(pady=10)

    def on_show(self):
        """هر بار که این صفحه نمایش داده می‌شود فراخوانی می‌شود"""
        self.welcome_label.config(
            text=f"خوش آمدید، {self.controller.current_user_name}"
        )
        if self.controller.current_user_is_admin:
            self.admin_btn.pack(side="left", padx=4)
        else:
            self.admin_btn.pack_forget()
        self.clear_search()

    def clear_search(self):
        self.search_var.set("")
        self.load_rooms()

    def load_rooms(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        session = get_session()
        try:
            query = session.query(Room).filter_by(is_active=True)
            keyword = self.search_var.get().strip()
            if keyword:
                query = query.filter(Room.room_type.contains(keyword))
            rooms = query.all()
            for room in rooms:
                self.tree.insert("", "end", values=(
                    room.id, room.room_number, room.room_type,
                    room.capacity, f"{room.price_per_night:,.0f}", room.description
                ))
        finally:
            session.close()

    def go_to_booking(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("خطا", "لطفاً یک اتاق را از جدول انتخاب کنید.")
            return
        room_id = self.tree.item(selected[0])["values"][0]
        self.controller.selected_room_id = int(room_id)
        self.controller.show_frame("BookingFrame")

    def logout(self):
        self.controller.current_user_id = None
        self.controller.current_user_name = None
        self.controller.current_user_is_admin = False
        self.controller.show_frame("LoginFrame")
