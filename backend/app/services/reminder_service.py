"""
Reminder service for EMI payment notifications
"""
from datetime import date, timedelta
from ..utils.whatsapp import whatsapp_service
from ..database import get_database
from ..config import settings


class ReminderService:
    """Reminder service for payment notifications"""
    
    def __init__(self):
        self.db = get_database()
        self.whatsapp = whatsapp_service
    
    async def send_emi_reminders(self) -> Dict[str, int]:
        """
        Send WhatsApp reminders for upcoming EMI payments
        This should be called daily by a scheduler
        
        Returns:
            Dictionary with statistics
        """
        today = date.today()
        reminder_date = today + timedelta(days=settings.REMINDER_DAYS_BEFORE)
        
        # Find EMIs due on the reminder date
        emis = await self.db.emis.find({
            "status": "Active",
            "reminder_enabled": True,
            "next_payment_date": reminder_date
        }).to_list(length=None)
        
        sent_count = 0
        failed_count = 0
        
        for emi in emis:
            # Get user details
            user = await self.db.users.find_one({"_id": emi["user_id"]})
            if not user:
                continue
            
            # Send WhatsApp reminder
            result = self.whatsapp.send_emi_reminder(
                name=user["name"],
                phone=user["phone"],
                loan_name=emi["loan_name"],
                amount=emi["emi_amount"],
                due_date=emi["next_payment_date"].strftime("%d %B %Y")
            )
            
            if result:
                sent_count += 1
            else:
                failed_count += 1
        
        return {
            "total_emis": len(emis),
            "sent": sent_count,
            "failed": failed_count
        }
