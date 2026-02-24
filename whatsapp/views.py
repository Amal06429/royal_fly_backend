try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests module not installed. WhatsApp functionality disabled.")

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

@api_view(["POST"])
def send_ticket_whatsapp(request):
    if not REQUESTS_AVAILABLE:
        return Response({
            "success": False,
            "error": "WhatsApp functionality is disabled. Please install 'requests' module."
        }, status=503)
    
    data = request.data

    # Build WhatsApp message
    message = f"""
✈️ *Royal Fly – Ticket Details*

Customer: {data.get('customer_name')}
Route: {data.get('from_city')} → {data.get('to_city')}

💰 Price: ₹{data.get('ticket_price')}
🛫 Airline: {data.get('airline')}
📅 Travel Date: {data.get('travel_date')}

📝 Notes:
{data.get('notes', 'N/A')}

Reply YES to confirm this booking.
"""

    url = "https://app.dxing.in/api/send/whatsapp"

    params = {
        "secret": settings.WHATSAPP_SECRET,
        "account": settings.WHATSAPP_ACCOUNT,
        "recipient": data.get("phone"),
        "type": "text",
        "message": message,
        "priority": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        return Response({
            "success": True,
            "provider_response": response.json()
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
