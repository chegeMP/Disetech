import os

class Config:
    SECRET_KEY = 'disetech-secret-key'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:lifeisgood@localhost/Disetech'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    WEATHER_API_KEY = 'c665a58919b94bc9b5893015251507' 
    
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Example safe usage

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
