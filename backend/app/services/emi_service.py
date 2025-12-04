"""
EMI (Equated Monthly Installment) service with calculation logic
"""
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from bson import ObjectId
from fastapi import HTTPException, status
from typing import List
from ..models.emi import (
    EMICreate, EMIUpdate, EMIResponse, EMIStatus, EMIPaymentSchedule
)
from ..database import get_database


class EMIService:
    """EMI management service"""
    
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.emis
    
    def calculate_emi(self, principal: float, annual_rate: float, tenure: int) -> float:
        """
        Calculate EMI amount using the formula:
        EMI = [P x R x (1+R)^N]/[(1+R)^N-1]
        
        Args:
            principal: Principal loan amount
            annual_rate: Annual interest rate in percentage
            tenure: Tenure in months
        
        Returns:
            EMI amount
        """
        if annual_rate == 0:
            return principal / tenure
        
        # Convert annual rate to monthly rate
        monthly_rate = annual_rate / (12 * 100)
        
        # Apply EMI formula
        emi = (principal * monthly_rate * pow(1 + monthly_rate, tenure)) / \
              (pow(1 + monthly_rate, tenure) - 1)
        
        return round(emi, 2)
    
    def generate_payment_schedule(self, principal: float, annual_rate: float, 
                                   tenure: int, start_date: date) -> List[EMIPaymentSchedule]:
        """
        Generate complete amortization schedule
        
        Returns:
            List of payment schedule items
        """
        emi_amount = self.calculate_emi(principal, annual_rate, tenure)
        monthly_rate = annual_rate / (12 * 100)
        
        schedule = []
        balance = principal
        current_date = start_date
        
        for month in range(1, tenure + 1):
            interest = round(balance * monthly_rate, 2)
            principal_payment = round(emi_amount - interest, 2)
            balance = round(balance - principal_payment, 2)
            
            # Ensure balance doesn't go negative due to rounding
            if balance < 0:
                balance = 0
            
            schedule.append(EMIPaymentSchedule(
                month=month,
                payment_date=current_date,
                emi_amount=emi_amount,
                principal=principal_payment,
                interest=interest,
                balance=balance
            ))
            
            current_date += relativedelta(months=1)
        
        return schedule
    
    async def create_emi(self, user_id: str, emi_data: EMICreate) -> EMIResponse:
        """Create a new EMI"""
        # Calculate EMI amount
        emi_amount = self.calculate_emi(
            emi_data.principal_amount,
            emi_data.interest_rate,
            emi_data.tenure
        )
        
        # Create EMI document
        emi_dict = emi_data.dict()
        emi_dict["user_id"] = user_id
        emi_dict["emi_amount"] = emi_amount
        emi_dict["next_payment_date"] = emi_data.start_date
        emi_dict["remaining_tenure"] = emi_data.tenure
        emi_dict["total_interest_paid"] = 0
        emi_dict["principal_outstanding"] = emi_data.principal_amount
        emi_dict["status"] = EMIStatus.ACTIVE
        emi_dict["created_at"] = datetime.utcnow()
        emi_dict["updated_at"] = datetime.utcnow()
        
        # Insert into database
        result = await self.collection.insert_one(emi_dict)
        emi_dict["_id"] = str(result.inserted_id)
        
        return EMIResponse(**emi_dict, id=str(result.inserted_id))
    
    async def get_emis(self, user_id: str) -> List[EMIResponse]:
        """Get all EMIs for a user"""
        emis = []
        cursor = self.collection.find({"user_id": user_id})
        
        async for emi in cursor:
            emi["_id"] = str(emi["_id"])
            emis.append(EMIResponse(**emi, id=emi["_id"]))
        
        return emis
    
    async def get_emi_by_id(self, user_id: str, emi_id: str) -> EMIResponse:
        """Get specific EMI"""
        emi = await self.collection.find_one({
            "_id": ObjectId(emi_id),
            "user_id": user_id
        })
        
        if not emi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EMI not found"
            )
        
        return EMIResponse(**emi, id=str(emi["_id"]))
    
    async def update_emi(self, user_id: str, emi_id: str, 
                        emi_update: EMIUpdate) -> EMIResponse:
        """Update EMI"""
        update_data = {k: v for k, v in emi_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(emi_id), "user_id": user_id},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EMI not found"
            )
        
        return EMIResponse(**result, id=str(result["_id"]))
    
    async def delete_emi(self, user_id: str, emi_id: str) -> dict:
        """Delete EMI"""
        result = await self.collection.delete_one({
            "_id": ObjectId(emi_id),
            "user_id": user_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="EMI not found"
            )
        
        return {"message": "EMI deleted successfully"}
    
    async def get_payment_schedule(self, user_id: str, emi_id: str) -> List[EMIPaymentSchedule]:
        """Get payment schedule for an EMI"""
        emi = await self.get_emi_by_id(user_id, emi_id)
        
        return self.generate_payment_schedule(
            emi.principal_amount,
            emi.interest_rate,
            emi.tenure,
            emi.start_date
        )
    
    async def get_upcoming_payments(self, user_id: str, days: int = 7) -> List[EMIResponse]:
        """Get EMIs with payments due in next N days"""
        today = date.today()
        end_date = today + timedelta(days=days)
        
        emis = []
        cursor = self.collection.find({
            "user_id": user_id,
            "status": EMIStatus.ACTIVE,
            "next_payment_date": {
                "$gte": today,
                "$lte": end_date
            }
        })
        
        async for emi in cursor:
            emi["_id"] = str(emi["_id"])
            emis.append(EMIResponse(**emi, id=emi["_id"]))
        
        return emis
