import africastalking
from app.config import Config
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
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
    
    def set_previous_menu(self, session_id, menu_step):
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        if 'menu_history' not in self.sessions[session_id]:
            self.sessions[session_id]['menu_history'] = []
        self.sessions[session_id]['menu_history'].append(menu_step)
    
    def get_previous_menu(self, session_id):
        if session_id in self.sessions and 'menu_history' in self.sessions[session_id]:
            history = self.sessions[session_id]['menu_history']
            if len(history) > 1:
                # Remove current menu and return previous
                history.pop()
                return history[-1]
        return None

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

def send_login_sms(phone_number, name):
    message = f"Hello {name}! You have successfully logged into Disetech via USSD. Access more features on our website."
    try:
        response = sms.send(message, [phone_number])
        return True
    except Exception as e:
        print(f"SMS Error: {e}")
        return False

def process_ussd_request(session_id, phone_number, text):
    session_data = ussd_sessions.get_session(session_id)
    
    # Handle back navigation
    if text.endswith("*0") and session_data.get('step') != 'main_menu':
        previous_menu = ussd_sessions.get_previous_menu(session_id)
        if previous_menu:
            ussd_sessions.update_session(session_id, {'step': previous_menu})
            return process_ussd_request(session_id, phone_number, "")
        else:
            # Go back to main menu if no previous menu
            ussd_sessions.update_session(session_id, {'step': 'main_menu'})
            return process_ussd_request(session_id, phone_number, "")
    
    if text == "":
        # First interaction - Main Menu
        ussd_sessions.set_previous_menu(session_id, 'main_menu')
        response = "CON Welcome to Disetech!\n"
        response += "1. Create Account\n"
        response += "2. Login\n"
        response += "3. What We Offer\n"
        response += "4. Get Weather Info\n"
        response += "5. Crop Disease Help\n"
        response += "6. Contact Support"
        return response
    
    elif text == "1":
        # Start account creation
        ussd_sessions.set_previous_menu(session_id, 'name')
        ussd_sessions.update_session(session_id, {'step': 'name'})
        response = "CON Create Your Account\n"
        response += "Enter your full name:\n\n"
        response += "Type 0 to go back"
        return response
    
    elif session_data.get('step') == 'name':
        # Collect name
        name = text.split("*")[-1].strip()
        if name == "0":
            return process_ussd_request(session_id, phone_number, "")
        if len(name) < 2:
            response = "CON Invalid name. Please enter your full name:\n\n"
            response += "Type 0 to go back"
            return response
        
        ussd_sessions.set_previous_menu(session_id, 'email')
        ussd_sessions.update_session(session_id, {'name': name, 'step': 'email'})
        response = "CON Enter your email address:\n\n"
        response += "Type 0 to go back"
        return response
    
    elif session_data.get('step') == 'email':
        # Collect email
        email = text.split("*")[-1].strip()
        if email == "0":
            ussd_sessions.update_session(session_id, {'step': 'name'})
            response = "CON Create Your Account\n"
            response += "Enter your full name:\n\n"
            response += "Type 0 to go back"
            return response
        if not validate_email(email):
            response = "CON Invalid email format. Please enter a valid email:\n\n"
            response += "Type 0 to go back"
            return response
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            response = "END Email already registered. Please use a different email or login through the website."
            ussd_sessions.clear_session(session_id)
            return response
        
        ussd_sessions.set_previous_menu(session_id, 'password')
        ussd_sessions.update_session(session_id, {'email': email, 'step': 'password'})
        response = "CON Enter a password (min 6 characters):\n\n"
        response += "Type 0 to go back"
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
        # Start login process
        ussd_sessions.set_previous_menu(session_id, 'login_email')
        ussd_sessions.update_session(session_id, {'step': 'login_email'})
        response = "CON Login to Your Account\n"
        response += "Enter your email address:\n\n"
        response += "Type 0 to go back"
        return response
    
    elif text == "3":
        # What We Offer
        ussd_sessions.set_previous_menu(session_id, 'what_we_offer')
        ussd_sessions.update_session(session_id, {'step': 'what_we_offer'})
        response = "CON What We Offer:\n\n"
        response += "1. Weather Forecast\n"
        response += "2. Disease Detection\n"
        response += "3. Farm Insights\n"
        response += "4. Smart Adviser (AI Chat)\n\n"
        response += "0. Back to Main Menu"
        return response
    
    elif session_data.get('step') == 'what_we_offer':
        choice = text.split("*")[-1].strip()
        
        if choice == "1":
            # Weather Forecast
            response = "END Weather Forecast:\n\n"
            response += "Get real-time weather updates, forecasts, and agricultural weather alerts.\n\n"
            response += "Features:\n"
            response += "• 7-day weather forecast\n"
            response += "• Rainfall predictions\n"
            response += "• Temperature trends\n"
            response += "• Farming recommendations\n\n"
            response += "Visit our website or create an account to access!"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "2":
            # Disease Detection
            response = "END Disease Detection:\n\n"
            response += "AI-powered crop disease identification and treatment recommendations.\n\n"
            response += "Features:\n"
            response += "• Photo-based disease analysis\n"
            response += "• Treatment suggestions\n"
            response += "• Prevention tips\n"
            response += "• Expert consultation\n\n"
            response += "Visit our website to upload crop photos!"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "3":
            # Farm Insights
            response = "END Farm Insights:\n\n"
            response += "Data-driven insights to optimize your farming operations.\n\n"
            response += "Features:\n"
            response += "• Soil analysis reports\n"
            response += "• Crop yield predictions\n"
            response += "• Market price trends\n"
            response += "• Farming calendar\n\n"
            response += "Create an account to access personalized insights!"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "4":
            # Smart Adviser (AI Chat)
            response = "END Smart Adviser:\n\n"
            response += "Chat with our AI farming expert for personalized advice.\n\n"
            response += "Get help with:\n"
            response += "• Crop selection\n"
            response += "• Planting schedules\n"
            response += "• Pest management\n"
            response += "• General farming tips\n\n"
            response += "Visit our website to start chatting!"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "0":
            # Back to main menu
            return process_ussd_request(session_id, phone_number, "")
        
        else:
            response = "CON Invalid option. Please try again:\n\n"
            response += "1. Weather Forecast\n"
            response += "2. Disease Detection\n"
            response += "3. Farm Insights\n"
            response += "4. Smart Adviser (AI Chat)\n\n"
            response += "0. Back to Main Menu"
            return response

    elif session_data.get('step') == 'login_email':
        # Collect email for login
        email = text.split("*")[-1].strip()
        if email == "0":
            return process_ussd_request(session_id, phone_number, "")
        if not validate_email(email):
            response = "CON Invalid email format. Please enter a valid email:\n\n"
            response += "Type 0 to go back"
            return response
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            response = "END Email not found. Please create an account first or check your email."
            ussd_sessions.clear_session(session_id)
            return response
        
        ussd_sessions.set_previous_menu(session_id, 'login_password')
        ussd_sessions.update_session(session_id, {'login_email': email, 'step': 'login_password'})
        response = "CON Enter your password:\n\n"
        response += "Type 0 to go back"
        return response
    
    elif session_data.get('step') == 'login_password':
        # Verify password
        password = text.split("*")[-1].strip()
        if password == "0":
            ussd_sessions.update_session(session_id, {'step': 'login_email'})
            response = "CON Login to Your Account\n"
            response += "Enter your email address:\n\n"
            response += "Type 0 to go back"
            return response
            
        email = session_data['login_email']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            # Successful login
            send_login_sms(phone_number, user.name)
            
            response = "CON Login Successful!\n"
            response += f"Welcome back, {user.name}!\n\n"
            response += "Choose an option:\n"
            response += "1. View Profile\n"
            response += "2. Weather Info\n"
            response += "3. Crop Disease Help\n"
            response += "4. Farm Insights\n"
            response += "5. Smart Adviser\n"
            response += "6. Logout\n\n"
            response += "0. Back"
            
            # Store logged in user info for this session
            ussd_sessions.set_previous_menu(session_id, 'logged_in_menu')
            ussd_sessions.update_session(session_id, {
                'logged_in': True, 
                'user_id': user.id, 
                'user_name': user.name,
                'user_email': user.email,
                'step': 'logged_in_menu'
            })
            return response
        else:
            # Invalid password
            response = "END Invalid password. Please try again or reset your password on our website."
            ussd_sessions.clear_session(session_id)
            return response
    
    elif session_data.get('step') == 'logged_in_menu':
        # Handle logged in user menu
        choice = text.split("*")[-1].strip()
        user_name = session_data.get('user_name', 'User')
        
        if choice == "0":
            # Back option - logout and go to main menu
            ussd_sessions.clear_session(session_id)
            return process_ussd_request(session_id, phone_number, "")
        
        elif choice == "1":
            # View Profile
            response = f"END Profile Information:\n\n"
            response += f"Name: {session_data.get('user_name', 'N/A')}\n"
            response += f"Email: {session_data.get('user_email', 'N/A')}\n"
            response += f"Phone: {phone_number}\n\n"
            response += "Visit our website for more profile options."
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "2":
            # Weather info for logged in user
            response = f"END Weather Service\n\n"
            response += f"Hello {user_name}!\n"
            response += "Get personalized weather forecasts for your location.\n\n"
            response += "Visit our website for:\n"
            response += "• Current weather conditions\n"
            response += "• 7-day forecasts\n"
            response += "• Agricultural weather alerts\n"
            response += "• Planting recommendations"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "3":
            # Crop disease help for logged in user
            response = f"END Disease Detection\n\n"
            response += f"Hello {user_name}!\n"
            response += "Upload photos of your crops for AI-powered disease analysis.\n\n"
            response += "Visit our website to:\n"
            response += "• Upload crop photos\n"
            response += "• Get instant diagnosis\n"
            response += "• Receive treatment recommendations\n"
            response += "• Access expert advice"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "4":
            # Farm Insights
            response = f"END Farm Insights\n\n"
            response += f"Hello {user_name}!\n"
            response += "Access personalized farming insights and analytics.\n\n"
            response += "Visit our website for:\n"
            response += "• Soil analysis reports\n"
            response += "• Crop yield predictions\n"
            response += "• Market price trends\n"
            response += "• Customized farming calendar"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "5":
            # Smart Adviser
            response = f"END Smart Adviser\n\n"
            response += f"Hello {user_name}!\n"
            response += "Chat with our AI farming expert for personalized advice.\n\n"
            response += "Visit our website to:\n"
            response += "• Ask farming questions\n"
            response += "• Get crop recommendations\n"
            response += "• Learn best practices\n"
            response += "• Access 24/7 AI support"
            ussd_sessions.clear_session(session_id)
            return response
        
        elif choice == "6":
            # Logout
            response = f"END Goodbye {user_name}!\n\n"
            response += "You have been logged out successfully.\n"
            response += "Thank you for using Disetech!"
            ussd_sessions.clear_session(session_id)
            return response
        
        else:
            response = "CON Invalid option. Please try again:\n\n"
            response += "1. View Profile\n"
            response += "2. Weather Info\n"
            response += "3. Crop Disease Help\n"
            response += "4. Farm Insights\n"
            response += "5. Smart Adviser\n"
            response += "6. Logout\n\n"
            response += "0. Back"
            return response

    elif text == "4":
        # Weather info
        response = "END Weather Service\n\n"
        response += "Get real-time weather information for your farming needs.\n\n"
        response += "Create an account or visit our website for:\n"
        response += "• Current weather conditions\n"
        response += "• 7-day forecasts\n"
        response += "• Agricultural alerts\n"
        response += "• Planting recommendations"
        return response
    
    elif text == "5":
        # Crop disease help
        response = "END Disease Detection Service\n\n"
        response += "AI-powered crop disease identification and treatment.\n\n"
        response += "Visit our website to:\n"
        response += "• Upload crop photos\n"
        response += "• Get instant diagnosis\n"
        response += "• Receive treatment plans\n"
        response += "• Contact agricultural experts"
        return response
    
    elif text == "6":
        # Contact support
        response = "END Contact Support:\n\n"
        response += "📧 Email: support@disetech.com\n"
        response += "📞 Phone: +254712345678\n"
        response += "🌐 Website: www.disetech.com\n\n"
        response += "Office Hours: Mon-Fri 8AM-6PM"
        return response
    
    else:
        # Invalid option
        response = "END Invalid option. Please dial the USSD code again."
        return response
    