import os
from groq import Groq
from flask import Blueprint, render_template, request, session, redirect, url_for
from app.config import Config

chatbot = Blueprint('chatbot', __name__)

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@chatbot.route('/chatbot', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    response_text = ""
    user_input = ""

    if request.method == 'POST':
        user_input = request.form['message']

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are DisetechBot, a smart agricultural assistant. Provide accurate, helpful advice to farmers about crops, diseases, weather, soil management, and sustainable farming practices."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            response_text = response.choices[0].message.content
            
        except Exception as e:
            print(f"Groq API error: {e}")
            response_text = "Sorry, I'm experiencing technical difficulties. Please try again in a moment."

    return render_template("chatbot.html", response=response_text, user_input=user_input)
