import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
