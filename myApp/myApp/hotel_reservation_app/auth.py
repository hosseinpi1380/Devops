# -*- coding: utf-8 -*-
"""توابع ساده هش کردن و بررسی رمز عبور با hashlib (بدون وابستگی خارجی)"""

import hashlib
import os


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex()
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, digest = password_hash.split("$")
    except ValueError:
        return False
    check = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return check == digest
