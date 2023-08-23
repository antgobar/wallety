import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    MONGO_URI = os.getenv("MONGO_URI")