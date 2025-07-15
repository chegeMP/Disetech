from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime
import requests
from app.config import Config

insights = Blueprint('insights', __name__)

@insights.route('/insights')
def show_insights():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    city = "Nairobi"  # Later use actual user data
    api_key = Config.WEATHER_API_KEY
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        res = requests.get(url)
        weather_data = res.json()
        condition = weather_data["current"]["condition"]["text"]
        temp = weather_data["current"]["temp_c"]

        tips = [
            {"title": "Local Weather", "body": f"The current condition in {city} is {condition}, {temp}°C."},
        ]

        if "Rain" in condition:
            tips.append({"title": "Rain Advisory", "body": "Avoid spraying pesticides during rain — they may wash off."})
        if temp > 30:
            tips.append({"title": "High Temp Warning", "body": "Irrigate crops early morning or evening to reduce stress."})
        tips.extend([
            {"title": "Rotate Crops", "body": "Rotating crops every season prevents soil depletion and pest buildup."},
            {"title": "Mulching", "body": "Use organic mulch to retain moisture and reduce weeds."}
        ])
    except Exception as e:
        print("Weather fetch error:", e)
        tips = [{"title": "Insight Load Error", "body": "Could not load dynamic insights. Showing defaults."}]

    return render_template('insights.html', tips=tips)
