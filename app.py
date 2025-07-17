from flask import Flask, render_template, request
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Initialize Flask
app = Flask(__name__)

# Load Firebase credentials
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Replace this with your OpenWeatherMap API key
API_KEY = "1e4d4911229f583d7e8ab60c597d3c74"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") == 200:
                weather_data = {
                    "city": city.title(),
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"].title(),
                    "humidity": data["main"]["humidity"],
                    "country": data["sys"]["country"],
                    "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                # Save to Firestore
                db.collection("weather_history").add(weather_data)
            else:
                weather_data = {"error": "City not found!"}
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
