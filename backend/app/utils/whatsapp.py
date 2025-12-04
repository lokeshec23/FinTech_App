"""
WhatsApp integration using Twilio
"""
from typing import Optional
from twilio.rest import Client
from ..config import settings


class WhatsAppService:
    """WhatsApp messaging service using Twilio"""
    
    def __init__(self):
        self.enabled = all([
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
            settings.TWILIO_WHATSAPP_FROM
        ])
        
        if self.enabled:
            self.client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )
        else:
            self.client = None
            print("⚠️  WhatsApp reminders disabled: Twilio credentials not configured")
    
    def send_message(self, to_phone: str, message: str) -> Optional[str]:
        """
        Send WhatsApp message
        
        Args:
            to_phone: Phone number with country code (e.g., +919876543210)
            message: Message content
            
        Returns:
            Message SID if successful, None otherwise
        """
        if not self.enabled:
            print(f"WhatsApp not configured. Would send to {to_phone}: {message}")
            return None
        
        try:
            # Ensure phone number is in WhatsApp format
            if not to_phone.startswith("whatsapp:"):
                to_phone = f"whatsapp:{to_phone}"
            
            message_obj = self.client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM,
                to=to_phone,
                body=message
            )
            
            print(f"✅ WhatsApp sent to {to_phone}: {message_obj.sid}")
            return message_obj.sid
            
        except Exception as e:
            print(f"❌ Failed to send WhatsApp to {to_phone}: {str(e)}")
            return None
    
    def send_emi_reminder(self, name: str, phone: str, loan_name: str, 
                          amount: float, due_date: str) -> Optional[str]:
        """
        Send EMI payment reminder
        
        Args:
            name: User's name
            phone: User's phone number
            loan_name: Name of the loan/EMI
            amount: EMI amount
            due_date: Due date (formatted string)
            
        Returns:
            Message SID if successful
        """
        from .formatters import format_indian_currency
        
        formatted_amount = format_indian_currency(amount)
        message = (
            f"Hi {name}! 📅\n\n"
            f"Reminder: Your {loan_name} EMI of {formatted_amount} "
            f"is due on {due_date}.\n\n"
            f"Don't forget to pay on time! 💰"
        )
        
        return self.send_message(phone, message)


# Global instance
whatsapp_service = WhatsAppService()
