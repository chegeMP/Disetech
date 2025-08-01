from flask import Blueprint, request, make_response

ussd = Blueprint('ussd', __name__)

# Simulated session store (replace with real session management or DB in production)
active_sessions = set()

@ussd.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.form.get("sessionId", "")
    service_code = request.form.get("serviceCode", "")
    phone_number = request.form.get("phoneNumber", "")
    text = request.form.get("text", "").strip()

    inputs = text.split("*")
    user_key = phone_number

    # Start Menu
    if text == "":
        response = (
            "CON Welcome to Disetech\n"
            "1. Login\n"
            "2. Crop Disease Diagnosis\n"
            "3. Personal AI Assistant\n"
            "4. Farm Insights\n"
            "5. Weather Updates\n"
            "6. Market Prices\n"
            "7. Logout"
        )

    # Login
    elif text == "1":
        # Simulate login (just add session_id to active_sessions)
        active_sessions.add(user_key)
        response = "END You have successfully logged in to Disetech."

    # Crop Disease Diagnosis
    elif text == "2":
        if user_key not in active_sessions:
            response = "END Please login first using option 1."
        else:
            response = "CON Enter crop and symptoms (e.g., 2*Maize*Yellowing leaves)"

    elif inputs[0] == "2" and len(inputs) >= 3:
        if user_key not in active_sessions:
            response = "END Please login first."
        else:
            crop = inputs[1]
            symptoms = "*".join(inputs[2:])
            response = f"END Diagnosis for {crop} with symptoms '{symptoms}' sent."

    # Personal AI Assistant
    elif text == "3":
        if user_key not in active_sessions:
            response = "END Please login first using option 1."
        else:
            response = "CON Ask a question (e.g., 3*When to plant tomatoes?)"

    elif inputs[0] == "3" and len(inputs) >= 2:
        if user_key not in active_sessions:
            response = "END Please login first."
        else:
            question = "*".join(inputs[1:])
            response = f"END AI response to: '{question}'\nCheck app for full answer."

    # Farm Insights
    elif text == "4":
        if user_key not in active_sessions:
            response = "END Please login first."
        else:
            response = "END Farm Insights:\n- Soil Health: Good\n- Moisture: Moderate"

    # Weather
    elif text == "5":
        if user_key not in active_sessions:
            response = "END Please login first."
        else:
            response = "END Weather:\n- Temp: 24°C\n- Rain: 30%\n- Wind: Mild"

    # Market Prices
    elif text == "6":
        if user_key not in active_sessions:
            response = "END Please login first."
        else:
            response = "END Market Prices:\n- Maize: KES 45/kg\n- Beans: KES 90/kg"

    # Logout
    elif text == "7":
        active_sessions.discard(user_key)
        response = "END You have been logged out of Disetech."

    else:
        response = "END Invalid input. Please try again."

    return make_response(response, 200, {'Content-Type': 'text/plain'})
