# -*- coding: utf-8 -*-
"""پنل مدیریت اتاق‌ها (فقط برای کاربر ادمین)"""

import tkinter as tk
from tkinter import ttk, messagebox

from database import get_session
from models import Room
from config import CURRENCY


class AdminFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        ttk.Label(self, text="پنل مدیریت اتاق‌ها", font=("Tahoma", 18, "bold")).pack(pady=15)

        form = ttk.LabelFrame(self, text="افزودن / ویرایش اتاق", padding=15)
        form.pack(fill="x", pady=10)

        self.room_number_var = tk.StringVar()
        self.room_type_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.capacity_var = tk.StringVar()
        self.description_var = tk.StringVar()

        fields = [
            ("شماره اتاق:", self.room_number_var),
            ("نوع اتاق:", self.room_type_var),
            (f"قیمت هر شب ({CURRENCY}):", self.price_var),
            ("ظرفیت:", self.capacity_var),
            ("توضیحات:", self.description_var),
        ]
        for i, (label, var) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=i // 2, column=(i % 2) * 2, sticky="e", padx=5, pady=5)
            ttk.Entry(form, textvariable=var, width=25).grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=5)

        btn_bar = ttk.Frame(form)
        btn_bar.grid(row=3, column=0, columnspan=4, pady=10)
        ttk.Button(btn_bar, text="افزودن اتاق جدید", command=self.add_room).pack(side="right", padx=5)
        ttk.Button(btn_bar, text="ویرایش اتاق انتخاب‌شده", command=self.update_room).pack(side="right", padx=5)
        ttk.Button(btn_bar, text="غیرفعال‌سازی اتاق", command=self.deactivate_room).pack(side="right", padx=5)
        ttk.Button(btn_bar, text="پاک کردن فرم", command=self.clear_form).pack(side="right", padx=5)

        columns = ("id", "room_number", "room_type", "capacity", "price", "active")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        headings = {
            "id": "شناسه", "room_number": "شماره اتاق", "room_type": "نوع",
            "capacity": "ظرفیت", "price": "قیمت", "active": "فعال",
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=110, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

        ttk.Button(self, text="بازگشت به صفحه اصلی",
                   command=lambda: controller.show_frame("DashboardFrame")).pack(pady=5)

    def on_show(self):
        if not self.controller.current_user_is_admin:
            messagebox.showerror("دسترسی غیرمجاز", "فقط کاربر ادمین به این صفحه دسترسی دارد.")
            self.controller.show_frame("DashboardFrame")
            return
        self.clear_form()
        self.load_rooms()

    def load_rooms(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        session = get_session()
        try:
            for room in session.query(Room).all():
                self.tree.insert("", "end", values=(
                    room.id, room.room_number, room.room_type, room.capacity,
                    f"{room.price_per_night:,.0f}", "بله" if room.is_active else "خیر"
                ))
        finally:
            session.close()

    def on_select_row(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        session = get_session()
        try:
            room = session.query(Room).get(int(values[0]))
            self.room_number_var.set(room.room_number)
            self.room_type_var.set(room.room_type)
            self.price_var.set(str(room.price_per_night))
            self.capacity_var.set(str(room.capacity))
            self.description_var.set(room.description)
            self._selected_room_id = room.id
        finally:
            session.close()

    def clear_form(self):
        self.room_number_var.set("")
        self.room_type_var.set("")
        self.price_var.set("")
        self.capacity_var.set("")
        self.description_var.set("")
        self._selected_room_id = None

    def _validate_form(self):
        if not self.room_number_var.get().strip() or not self.room_type_var.get().strip():
            messagebox.showwarning("خطا", "شماره اتاق و نوع اتاق الزامی است.")
            return False
        try:
            float(self.price_var.get())
            int(self.capacity_var.get())
        except ValueError:
            messagebox.showwarning("خطا", "قیمت و ظرفیت باید عددی باشند.")
            return False
        return True

    def add_room(self):
        if not self._validate_form():
            return
        session = get_session()
        try:
            if session.query(Room).filter_by(room_number=self.room_number_var.get().strip()).first():
                messagebox.showerror("خطا", "اتاقی با این شماره از قبل وجود دارد.")
                return
            room = Room(
                room_number=self.room_number_var.get().strip(),
                room_type=self.room_type_var.get().strip(),
                price_per_night=float(self.price_var.get()),
                capacity=int(self.capacity_var.get()),
                description=self.description_var.get().strip(),
            )
            session.add(room)
            session.commit()
        finally:
            session.close()
        self.clear_form()
        self.load_rooms()

    def update_room(self):
        if not getattr(self, "_selected_room_id", None):
            messagebox.showwarning("خطا", "لطفاً ابتدا یک اتاق را از جدول انتخاب کنید.")
            return
        if not self._validate_form():
            return
        session = get_session()
        try:
            room = session.query(Room).get(self._selected_room_id)
            room.room_number = self.room_number_var.get().strip()
            room.room_type = self.room_type_var.get().strip()
            room.price_per_night = float(self.price_var.get())
            room.capacity = int(self.capacity_var.get())
            room.description = self.description_var.get().strip()
            session.commit()
        finally:
            session.close()
        self.clear_form()
        self.load_rooms()

    def deactivate_room(self):
        if not getattr(self, "_selected_room_id", None):
            messagebox.showwarning("خطا", "لطفاً ابتدا یک اتاق را از جدول انتخاب کنید.")
            return
        session = get_session()
        try:
            room = session.query(Room).get(self._selected_room_id)
            room.is_active = False
            session.commit()
        finally:
            session.close()
        self.clear_form()
        self.load_rooms()
