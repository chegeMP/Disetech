from flask import Blueprint, request
from app.services.ussdservice import process_ussd_request

ussd = Blueprint('ussd', __name__)

@ussd.route('/ussd', methods=['POST'])
def ussd_callback():
    # Get the USSD input from Africa's Talking
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")
    
    # Process the USSD request
    response = process_ussd_request(session_id, phone_number, text)
    
    return response
