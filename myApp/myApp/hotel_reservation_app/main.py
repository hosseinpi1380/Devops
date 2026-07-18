# -*- coding: utf-8 -*-
"""
سیستم رزرو هتل با پرداخت درون‌برنامه‌ای شبیه‌سازی‌شده
--------------------------------------------------------
اجرای برنامه:  python main.py

پیش‌نیاز: قبل از اولین اجرا یکبار seed.py را اجرا کنید تا جداول ساخته
و داده‌های نمونه درج شوند:  python seed.py
"""

import tkinter as tk
from tkinter import ttk

from config import APP_TITLE, APP_WIDTH, APP_HEIGHT
from database import init_db

from gui.auth_frames import LoginFrame, RegisterFrame
from gui.dashboard_frame import DashboardFrame
from gui.booking_frame import BookingFrame
from gui.payment_frame import PaymentFrame
from gui.history_frame import HistoryFrame
from gui.admin_frame import AdminFrame


class HotelApp(tk.Tk):
    """کنترلر اصلی برنامه که بین صفحات مختلف جابه‌جا می‌شود"""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(800, 550)

        # وضعیت مشترک بین صفحات
        self.current_user_id = None
        self.current_user_name = None
        self.current_user_is_admin = False
        self.selected_room_id = None
        self.pending_reservation_id = None

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        frame_classes = (
            LoginFrame, RegisterFrame, DashboardFrame,
            BookingFrame, PaymentFrame, HistoryFrame, AdminFrame,
        )
        for FrameClass in frame_classes:
            frame = FrameClass(container, self)
            self.frames[FrameClass.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("LoginFrame")

    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()


def main():
    init_db()
    app = HotelApp()
    app.mainloop()


if __name__ == "__main__":
    main()
