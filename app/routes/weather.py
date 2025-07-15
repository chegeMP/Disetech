import requests
from flask import Blueprint, render_template, session, redirect, url_for
from app.config import Config

weather = Blueprint('weather', __name__)

@weather.route('/weather')
def weather_forecast():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    city = "Nairobi"
    api_key = Config.WEATHER_API_KEY
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3&aqi=no&alerts=no"

    response = requests.get(url)

    print("Weather API URL:", url)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    data = response.json()

    if "error" in data:
        return render_template("weather.html", error=data["error"]["message"])

    forecasts = []
    for day in data["forecast"]["forecastday"]:
        forecasts.append({
            "date": day["date"],
            "condition": day["day"]["condition"]["text"],
            "icon": day["day"]["condition"]["icon"],
            "avg_temp": day["day"]["avgtemp_c"],
            "max_temp": day["day"]["maxtemp_c"],
            "min_temp": day["day"]["mintemp_c"]
        })

    return render_template("weather.html", city=city, forecasts=forecasts)
