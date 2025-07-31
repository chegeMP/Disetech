import os

from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from app.routes.landing import landing
from app.routes.auth import auth
from app.config import Config
from app.extensions import db, migrate
from app.routes.insights import insights 
from app.routes.weather import weather
from app.routes.detect import detect
from app.routes.soil import soil
from app.routes.blog import blog
from app.routes.advisor import advisor
from app.routes.chatbot import chatbot

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.landing import landing
    from app.routes.auth import auth
    from app.routes.weather import weather
    from app.routes.soil import soil
    from app.routes.detect import detect
    from app.routes.blog import blog
    from app.routes.chatbot import chatbot
    from app.routes.advisor import advisor
    from app.routes.insights import insights
    from app.routes.ussdroute import ussd

    app.register_blueprint(landing)
    app.register_blueprint(auth)
    app.register_blueprint(weather)
    app.register_blueprint(detect)
    app.register_blueprint(insights)
    app.register_blueprint(soil)
    app.register_blueprint(blog)
    app.register_blueprint(advisor)
    app.register_blueprint(chatbot)
    app.register_blueprint(ussd)

    return app
