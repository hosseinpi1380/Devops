# -*- coding: utf-8 -*-
"""
درگاه پرداخت شبیه‌سازی‌شده (Mock Payment Gateway)
---------------------------------------------------
این ماژول یک پرداخت واقعی انجام نمی‌دهد و صرفاً برای تست و آموزش است.
منطق اعتبارسنجی ساده کارت (طول شماره کارت، تاریخ انقضا و CVV2) را شبیه‌سازی می‌کند
و در پایان یک شناسه تراکنش تصادفی تولید می‌کند.

نکته: برای اتصال به درگاه واقعی (زرین‌پال، Stripe و ...) کافیست این کلاس را
با پیاده‌سازی واقعی (فراخوانی API درگاه) جایگزین کنید؛ بقیه‌ی برنامه بدون تغییر
با آن کار خواهد کرد چون فقط متد charge() فراخوانی می‌شود.
"""

import random
import re
import string
import time


class PaymentError(Exception):
    pass


class MockPaymentGateway:
    """شبیه‌ساز درگاه پرداخت داخل برنامه"""

    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        card_number = card_number.replace(" ", "")
        return bool(re.fullmatch(r"\d{16}", card_number))

    @staticmethod
    def validate_expiry(expiry: str) -> bool:
        # فرمت MM/YY
        return bool(re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", expiry))

    @staticmethod
    def validate_cvv(cvv: str) -> bool:
        return bool(re.fullmatch(r"\d{3,4}", cvv))

    @classmethod
    def charge(cls, card_number: str, expiry: str, cvv: str, amount: float):
        """
        شبیه‌سازی پرداخت. در صورت موفقیت، دیکشنری شامل transaction_id و card_last4
        برمی‌گرداند؛ در غیر این صورت PaymentError راه می‌اندازد.
        """
        card_number_clean = card_number.replace(" ", "")

        if not cls.validate_card_number(card_number_clean):
            raise PaymentError("شماره کارت باید ۱۶ رقم باشد.")
        if not cls.validate_expiry(expiry):
            raise PaymentError("تاریخ انقضا باید به فرمت MM/YY باشد.")
        if not cls.validate_cvv(cvv):
            raise PaymentError("CVV2 نامعتبر است.")
        if amount <= 0:
            raise PaymentError("مبلغ پرداخت نامعتبر است.")

        # شبیه‌سازی تاخیر شبکه
        time.sleep(0.4)

        # شبیه‌سازی احتمال شکست تراکنش (کارت‌هایی که با 0000 شروع می‌شوند رد می‌شوند)
        if card_number_clean.startswith("0000"):
            raise PaymentError("تراکنش توسط بانک رد شد (کارت آزمایشی ناموفق).")

        transaction_id = "TXN-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=12)
        )

        return {
            "transaction_id": transaction_id,
            "card_last4": card_number_clean[-4:],
            "status": "موفق",
        }
