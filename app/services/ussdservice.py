import africastalking
from app.config import Config
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash
import re

# Initialize Africa's Talking
africastalking.initialize(Config.AT_USERNAME, Config.AT_API_KEY)
sms = africastalking.SMS

class USSDSession:
    def __init__(self):
        self.sessions = {}
    
    def get_session(self, session_id):
        return self.sessions.get(session_id, {})
    
    def update_session(self, session_id, data):
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        self.sessions[session_id].update(data)
    
    def clear_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

ussd_sessions = USSDSession()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    # Remove any spaces, dashes, or plus signs
    phone = re.sub(r'[\s\-\+]', '', phone)
    # Check if it's a valid phone number (8-15 digits)
    return re.match(r'^\d{8,15}$', phone) is not None

def send_confirmation_sms(phone_number, name, email):
    message = f"Welcome to Disetech, {name}! Your account has been created successfully. Email: {email}. You can now access our services."
    try:
        response = sms.send(message, [phone_number])
        return True
    except Exception as e:
        print(f"SMS Error: {e}")
        return False

def process_ussd_request(session_id, phone_number, text):
    session_data = ussd_sessions.get_session(session_id)
    
    if text == "":
        # First interaction
        response = "CON Welcome to Disetech!\n"
        response += "1. Create Account\n"
        response += "2. Get Weather Info\n"
        response += "3. Crop Disease Help\n"
        response += "4. Contact Support"
        return response
    
    elif text == "1":
        # Start account creation
        ussd_sessions.update_session(session_id, {'step': 'name'})
        response = "CON Create Your Account\n"
        response += "Enter your full name:"
        return response
    
    elif session_data.get('step') == 'name':
        # Collect name
        name = text.split("*")[-1].strip()
        if len(name) < 2:
            response = "CON Invalid name. Please enter your full name:"
            return response
        
        ussd_sessions.update_session(session_id, {'name': name, 'step': 'email'})
        response = "CON Enter your email address:"
        return response
    
    elif session_data.get('step') == 'email':
        # Collect email
        email = text.split("*")[-1].strip()
        if not validate_email(email):
            response = "CON Invalid email format. Please enter a valid email:"
            return response
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            response = "END Email already registered. Please use a different email or login through the website."
            ussd_sessions.clear_session(session_id)
            return response
        
        ussd_sessions.update_session(session_id, {'email': email, 'step': 'password'})
        response = "CON Enter a password (min 6 characters):"
        return response
    
    elif session_data.get('step') == 'password':
        # Collect password
        password = text.split("*")[-1].strip()
        if len(password) < 6:
            response = "CON Password too short. Enter at least 6 characters:"
            return response
        
        ussd_sessions.update_session(session_id, {'password': password, 'step': 'confirm'})
        response = "CON Confirm your details:\n"
        response += f"Name: {session_data['name']}\n"
        response += f"Email: {session_data['email']}\n"
        response += f"Phone: {phone_number}\n"
        response += "1. Confirm\n"
        response += "2. Start Over"
        return response
    
    elif session_data.get('step') == 'confirm':
        choice = text.split("*")[-1].strip()
        if choice == "1":
            # Create account
            try:
                name = session_data['name']
                email = session_data['email']
                password = generate_password_hash(session_data['password'])
                
                user = User(
                    name=name,
                    email=email,
                    password=password,
                    phone=phone_number
                )
                
                db.session.add(user)
                db.session.commit()
                
                # Send confirmation SMS
                send_confirmation_sms(phone_number, name, email)
                
                ussd_sessions.clear_session(session_id)
                response = f"END Account created successfully!\n"
                response += f"Welcome {name}!\n"
                response += "Check your SMS for confirmation."
                return response
                
            except Exception as e:
                ussd_sessions.clear_session(session_id)
                response = "END Error creating account. Please try again later."
                return response
        
        elif choice == "2":
            # Start over
            ussd_sessions.clear_session(session_id)
            return process_ussd_request(session_id, phone_number, "1")
    
    elif text == "2":
        # Weather info
        response = "END Weather service coming soon! Visit our website for current weather information."
        return response
    
    elif text == "3":
        # Crop disease help
        response = "END For crop disease detection, please visit our website or call our support line."
        return response
    
    elif text == "4":
        # Contact support
        response = "END Contact Support:\n"
        response += "Email: support@disetech.com\n"
        response += "Phone: +254712345678"
        return response
    
    else:
        # Invalid option
        response = "END Invalid option. Please dial the USSD code again."
        return response
    