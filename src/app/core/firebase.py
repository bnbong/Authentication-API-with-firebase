import os
import firebase_admin

from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()


if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIRE_BASE_KEY"))
    firebase_admin.initialize_app(cred)
