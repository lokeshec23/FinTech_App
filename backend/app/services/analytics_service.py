"""
Analytics service for financial insights
"""
from datetime import datetime, date, timedelta
from typing import Dict, List, Any
from ..database import get_database
from ..models.expense import ExpenseCategory


class AnalyticsService:
    """Analytics and reporting service"""
    
    def __init__(self):
        self.db = get_database()
    
    async def get_monthly_spending(self, user_id: str, month: int, year: int) -> float:
        """Get total spending for a specific month"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "date": {"$gte": start_date, "$lt": end_date}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"}
                }
            }
        ]
        
        result = await self.db.expenses.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0
    
    async def get_category_breakdown(self, user_id: str, month: int, year: int) -> Dict[str, float]:
        """Get spending by category for a month"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "date": {"$gte": start_date, "$lt": end_date}
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "total": {"$sum": "$amount"}
                }
            }
        ]
        
        result = await self.db.expenses.aggregate(pipeline).to_list(length=None)
        return {item["_id"]: item["total"] for item in result}
    
    async def get_spending_trend(self, user_id: str, months: int = 6) -> List[Dict[str, Any]]:
        """Get spending trend for last N months"""
        today = datetime.now()
        trends = []
        
        for i in range(months):
            month_date = today - timedelta(days=30 * i)
            month = month_date.month
            year = month_date.year
            
            total = await self.get_monthly_spending(user_id, month, year)
            
            trends.append({
                "month": month,
                "year": year,
                "month_name": month_date.strftime("%B"),
                "total": total
            })
        
        return list(reversed(trends))
    
    async def get_total_balances(self, user_id: str) -> float:
        """Get total balance across all bank accounts"""
        pipeline = [
            {
                "$match": {"user_id": user_id}
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$balance"}
                }
            }
        ]
        
        result = await self.db.bank_accounts.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0
    
    async def get_total_assets(self, user_id: str) -> float:
        """Get total value of all assets"""
        pipeline = [
            {
                "$match": {"user_id": user_id}
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$current_value"}
                }
            }
        ]
        
        result = await self.db.assets.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0
    
    async def get_total_liabilities(self, user_id: str) -> float:
        """Get total liabilities"""
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "status": "Active"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"}
                }
            }
        ]
        
        result = await self.db.liabilities.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0
    
    async def get_emi_burden_percentage(self, user_id: str) -> float:
        """Calculate EMI burden as percentage of monthly spending"""
        # Get total EMI amount
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "status": "Active"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$emi_amount"}
                }
            }
        ]
        
        result = await self.db.emis.aggregate(pipeline).to_list(length=1)
        total_emi = result[0]["total"] if result else 0
        
        # Get current month spending
        now = datetime.now()
        monthly_spending = await self.get_monthly_spending(user_id, now.month, now.year)
        
        if monthly_spending == 0:
            return 0
        
        return round((total_emi / monthly_spending) * 100, 2)
    
    async def get_asset_liability_ratio(self, user_id: str) -> float:
        """Calculate asset to liability ratio"""
        total_assets = await self.get_total_assets(user_id)
        total_liabilities = await self.get_total_liabilities(user_id)
        
        if total_liabilities == 0:
            return float('inf') if total_assets > 0 else 0
        
        return round(total_assets / total_liabilities, 2)
    
    async def get_dashboard_summary(self, user_id: str) -> Dict[str, Any]:
        """Get complete dashboard summary"""
        now = datetime.now()
        
        return {
            "total_balance": await self.get_total_balances(user_id),
            "total_assets": await self.get_total_assets(user_id),
            "total_liabilities": await self.get_total_liabilities(user_id),
            "monthly_spending": await self.get_monthly_spending(user_id, now.month, now.year),
            "category_breakdown": await self.get_category_breakdown(user_id, now.month, now.year),
            "spending_trend": await self.get_spending_trend(user_id, 6),
            "emi_burden_percentage": await self.get_emi_burden_percentage(user_id),
            "asset_liability_ratio": await self.get_asset_liability_ratio(user_id)
        }
