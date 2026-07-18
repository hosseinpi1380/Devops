# -*- coding: utf-8 -*-
"""صفحات ورود و ثبت‌نام کاربر"""

import tkinter as tk
from tkinter import ttk, messagebox

from database import get_session
from models import User
from auth import hash_password, verify_password


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        ttk.Label(self, text="ورود به سیستم رزرو هتل", font=("Tahoma", 18, "bold")).pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="نام کاربری:").grid(row=0, column=0, sticky="e", padx=5, pady=8)
        self.username_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.username_var, width=30).grid(row=0, column=1, pady=8)

        ttk.Label(form, text="رمز عبور:").grid(row=1, column=0, sticky="e", padx=5, pady=8)
        self.password_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1, pady=8)

        ttk.Button(self, text="ورود", command=self.login).pack(pady=15)
        ttk.Button(self, text="حساب کاربری ندارید؟ ثبت‌نام کنید",
                   command=lambda: controller.show_frame("RegisterFrame")).pack()

        ttk.Label(self, text="کاربر ادمین پیش‌فرض: admin / admin123",
                  foreground="gray").pack(pady=10)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showwarning("خطا", "لطفاً نام کاربری و رمز عبور را وارد کنید.")
            return

        session = get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user is None or not verify_password(password, user.password_hash):
                messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است.")
                return

            self.controller.current_user_id = user.id
            self.controller.current_user_name = user.full_name
            self.controller.current_user_is_admin = user.is_admin
            self.username_var.set("")
            self.password_var.set("")
            self.controller.show_frame("DashboardFrame")
        finally:
            session.close()


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        ttk.Label(self, text="ثبت‌نام کاربر جدید", font=("Tahoma", 18, "bold")).pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        self.full_name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.password_var = tk.StringVar()

        fields = [
            ("نام و نام‌خانوادگی:", self.full_name_var, False),
            ("نام کاربری:", self.username_var, False),
            ("شماره تماس:", self.phone_var, False),
            ("رمز عبور:", self.password_var, True),
        ]

        for i, (label, var, is_password) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=8)
            ttk.Entry(form, textvariable=var, width=30,
                      show="*" if is_password else "").grid(row=i, column=1, pady=8)

        ttk.Button(self, text="ثبت‌نام", command=self.register).pack(pady=15)
        ttk.Button(self, text="بازگشت به ورود",
                   command=lambda: controller.show_frame("LoginFrame")).pack()

    def register(self):
        full_name = self.full_name_var.get().strip()
        username = self.username_var.get().strip()
        phone = self.phone_var.get().strip()
        password = self.password_var.get()

        if not all([full_name, username, password]):
            messagebox.showwarning("خطا", "نام، نام کاربری و رمز عبور اجباری هستند.")
            return

        session = get_session()
        try:
            if session.query(User).filter_by(username=username).first():
                messagebox.showerror("خطا", "این نام کاربری قبلاً استفاده شده است.")
                return

            user = User(
                full_name=full_name,
                username=username,
                phone=phone,
                password_hash=hash_password(password),
                is_admin=False,
            )
            session.add(user)
            session.commit()
            messagebox.showinfo("موفق", "ثبت‌نام با موفقیت انجام شد. اکنون وارد شوید.")

            self.full_name_var.set("")
            self.username_var.set("")
            self.phone_var.set("")
            self.password_var.set("")

            self.controller.show_frame("LoginFrame")
        finally:
            session.close()
