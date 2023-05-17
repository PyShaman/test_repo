import os

from dotenv import load_dotenv


load_dotenv()
URL = os.environ.get("URL")
ADMIN = os.environ.get("ADMIN")
USER1 = os.environ.get("USER1")
USER2 = os.environ.get("USER2")
PASSWORD = os.environ.get("PASSWORD")
