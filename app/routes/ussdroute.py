from flask import Blueprint, request, Response
from app.services.ussdservice import process_ussd_request
import logging

ussd = Blueprint('ussd', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@ussd.route('/ussd', methods=['POST'])
def ussd_callback():
    try:
        # Log incoming request for debugging
        logger.info(f"USSD Request: {dict(request.values)}")
        
        # Get the USSD input from Africa's Talking
        session_id = request.values.get("sessionId", None)
        service_code = request.values.get("serviceCode", None)
        phone_number = request.values.get("phoneNumber", None)
        text = request.values.get("text", "")
        
        # Process the USSD request
        response_text = process_ussd_request(session_id, phone_number, text)
        
        logger.info(f"USSD Response: {response_text}")
        
        # Return with proper headers
        response = Response(
            response_text,
            mimetype='text/plain',
            headers={
                'Content-Type': 'text/plain; charset=utf-8',
                'Cache-Control': 'no-cache',
                'Connection': 'close'
            }
        )
        return response
        
    except Exception as e:
        logger.error(f"USSD Error: {str(e)}")
        return Response(
            "END Service temporarily unavailable. Please try again later.",
            mimetype='text/plain',
            status=500
        )

@ussd.route('/health', methods=['GET'])
def health_check():
    return Response("OK", mimetype='text/plain')
