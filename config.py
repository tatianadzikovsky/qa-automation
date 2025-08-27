# config.py
import os
from dotenv import load_dotenv

load_dotenv()

APPIUM_URL       = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
DEVICE_NAME      = os.getenv("DEVICE_NAME", "Android Emulator")
APP_PACKAGE      = os.getenv("APP_PACKAGE", "com.android.settings")
APP_ACTIVITY     = os.getenv("APP_ACTIVITY", ".Settings")
IMPLICIT_WAIT    = int(os.getenv("IMPLICIT_WAIT_SEC", "5"))
