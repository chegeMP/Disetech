import os
import openai
from flask import Blueprint, render_template, request, session, redirect, url_for
from app.config import Config

chatbot = Blueprint('chatbot', __name__)

# Use Groq’s OpenAI-compatible endpoint
openai.api_key = os.getenv('GROQ_API_KEY')
openai.api_base = "https://api.groq.com/openai/v1"

@chatbot.route('/chatbot', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    response_text = ""
    user_input = ""

    if request.method == 'POST':
        user_input = request.form['message']

        try:
            response = openai.ChatCompletion.create(
                model="llama3-70b-8192",  # You can use gemma or llama3
                messages=[
                    {"role": "system", "content": "You are a smart agricultural assistant called DisetechBot. Provide accurate, helpful advice to farmers."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            response_text = response['choices'][0]['message']['content']
        except Exception as e:
            print("Chat error:", e)
            response_text = "There was a problem processing your message."

    return render_template("chatbot.html", response=response_text, user_input=user_input)
