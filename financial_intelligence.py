"""
Traveloop - Financial Intelligence & Logistics Module
Budget management, expense tracking, analytics, and automated cost breakdowns
"""

from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from models import Trip, Expense, Activity, BudgetBreakdown, get_session
from sqlalchemy import func
import json


class FinancialIntelligence:
    """
    Financial management engine for travel budgeting and expense tracking
    Provides automated calculations, alerts, and analytics
    """
    
    def __init__(self, database_url='sqlite:///travel_database.db'):
        """Initialize the financial intelligence module"""
        self.database_url = database_url
        self.session = get_session(database_url)
    
    # ==================== EXPENSE MANAGEMENT ====================
    
    def add_expense(self, trip_id: int, description: str, amount: float, 
                   category: str, expense_date: date = None, 
                   payment_method: str = "cash", paid_by: str = "", 
                   notes: str = "") -> Expense:
        """
        Add an expense to a trip
        
        Args:
            trip_id: ID of the trip
            description: Description of expense
            amount: Amount spent
            category: Category (accommodation, food, transport, activities, miscellaneous)
            expense_date: Date of expense
            payment_method: How it was paid (cash, card, online)
            paid_by: Name of person who paid
            notes: Additional notes
            
        Returns:
            Expense object
        """
        expense = Expense(
            trip_id=trip_id,
            description=description,
            amount=amount,
            category=category,
            expense_date=expense_date or date.today(),
            payment_method=payment_method,
            paid_by=paid_by,
            notes=notes,
            status='pending'
        )
        self.session.add(expense)
        self.session.commit()
        return expense
    
    def get_trip_expenses(self, trip_id: int) -> List[Expense]:
        """Get all expenses for a trip"""
        return self.session.query(Expense).filter(Expense.trip_id == trip_id).all()
    
    def get_expenses_by_category(self, trip_id: int) -> Dict[str, List[Expense]]:
        """Get expenses grouped by category"""
        expenses = self.get_trip_expenses(trip_id)
        grouped = {}
        
        for expense in expenses:
            if expense.category not in grouped:
                grouped[expense.category] = []
            grouped[expense.category].append(expense)
        
        return grouped
    
    def update_expense(self, expense_id: int, **kwargs) -> Optional[Expense]:
        """Update expense details"""
        expense = self.session.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            for key, value in kwargs.items():
                if hasattr(expense, key):
                    setattr(expense, key, value)
            expense.updated_at = datetime.utcnow()
            self.session.commit()
        return expense
    
    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense"""
        expense = self.session.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            self.session.delete(expense)
            self.session.commit()
            return True
        return False
    
    # ==================== BUDGET CALCULATIONS ====================
    
    def calculate_total_spent(self, trip_id: int) -> float:
        """Calculate total amount spent on a trip"""
        result = self.session.query(func.sum(Expense.amount)).filter(
            Expense.trip_id == trip_id,
            Expense.status != 'cancelled'
        ).scalar()
        return result or 0.0
    
    def calculate_budget_by_category(self, trip_id: int) -> Dict[str, float]:
        """
        Calculate total spending by category
        
        Returns:
            Dictionary with categories and their total spending
        """
        expenses = self.get_trip_expenses(trip_id)
        categories = {}
        
        for expense in expenses:
            if expense.status != 'cancelled':
                if expense.category not in categories:
                    categories[expense.category] = 0.0
                categories[expense.category] += expense.amount
        
        return categories
    
    def calculate_daily_average(self, trip_id: int) -> float:
        """Calculate average daily spending"""
        trip = self.session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            return 0.0
        
        total_spent = self.calculate_total_spent(trip_id)
        duration = (trip.end_date - trip.start_date).days + 1
        
        return total_spent / duration if duration > 0 else 0.0
    
    def calculate_budget_remaining(self, trip_id: int) -> float:
        """Calculate budget remaining for a trip"""
        trip = self.session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            return 0.0
        
        total_spent = self.calculate_total_spent(trip_id)
        return trip.budget - total_spent
    
    def get_budget_status(self, trip_id: int) -> Dict:
        """
        Get comprehensive budget status
        
        Returns:
            Dictionary with budget overview
        """
        trip = self.session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            return {}
        
        total_spent = self.calculate_total_spent(trip_id)
        remaining = trip.budget - total_spent
        percentage_used = (total_spent / trip.budget * 100) if trip.budget > 0 else 0
        
        return {
            'total_budget': trip.budget,
            'total_spent': total_spent,
            'remaining': remaining,
            'percentage_used': round(percentage_used, 2),
            'status': 'on_track' if percentage_used <= 80 else 'warning' if percentage_used <= 100 else 'exceeded'
        }
    
    # ==================== AUTOMATED BUDGET BREAKDOWN ====================
    
    def create_budget_breakdown(self, trip_id: int, category: str, 
                               planned_budget: float, alert_threshold: float = 80) -> BudgetBreakdown:
        """
        Create a budget breakdown for a specific category
        
        Args:
            trip_id: ID of the trip
            category: Budget category
            planned_budget: Planned budget for this category
            alert_threshold: Percentage at which to alert (default 80%)
            
        Returns:
            BudgetBreakdown object
        """
        breakdown = BudgetBreakdown(
            trip_id=trip_id,
            category=category,
            planned_budget=planned_budget,
            alert_threshold=alert_threshold
        )
        self.session.add(breakdown)
        self.session.commit()
        return breakdown
    
    def get_category_breakdown(self, trip_id: int) -> List[Dict]:
        """
        Get budget breakdown for all categories
        
        Returns:
            List of category breakdowns with spending info
        """
        breakdowns = self.session.query(BudgetBreakdown).filter(
            BudgetBreakdown.trip_id == trip_id
        ).all()
        
        category_spending = self.calculate_budget_by_category(trip_id)
        
        result = []
        for breakdown in breakdowns:
            actual_spent = category_spending.get(breakdown.category, 0.0)
            percentage = (actual_spent / breakdown.planned_budget * 100) if breakdown.planned_budget > 0 else 0
            alert_triggered = percentage >= breakdown.alert_threshold
            
            result.append({
                'category': breakdown.category,
                'planned_budget': breakdown.planned_budget,
                'actual_spent': actual_spent,
                'remaining': breakdown.planned_budget - actual_spent,
                'percentage_used': round(percentage, 2),
                'alert_threshold': breakdown.alert_threshold,
                'alert_triggered': alert_triggered
            })
        
        return result
    
    # ==================== COST ESTIMATION ====================
    
    def estimate_activity_cost(self, trip_id: int, activity_type: str) -> float:
        """
        Estimate cost for a specific activity type based on historical data
        
        Args:
            trip_id: ID of the trip
            activity_type: Type of activity
            
        Returns:
            Estimated cost
        """
        # Query activities of this type to get average cost
        activities = self.session.query(Activity).filter(
            Activity.trip_id == trip_id,
            Activity.activity_type == activity_type,
            Activity.cost > 0
        ).all()
        
        if not activities:
            # Default estimates
            defaults = {
                'hiking': 1500,
                'sightseeing': 2000,
                'dining': 1000,
                'shopping': 3000,
                'relaxation': 500,
                'adventure': 5000
            }
            return defaults.get(activity_type, 1000)
        
        total = sum(a.cost for a in activities)
        return total / len(activities)
    
    # ==================== FINANCIAL ANALYTICS ====================
    
    def get_spending_trend(self, trip_id: int) -> List[Dict]:
        """
        Get spending trend over days of the trip
        Useful for data visualization
        
        Returns:
            List of daily spending data
        """
        trip = self.session.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            return []
        
        expenses = self.get_trip_expenses(trip_id)
        
        # Group expenses by date
        daily_spending = {}
        current_date = trip.start_date
        
        while current_date <= trip.end_date:
            daily_spending[current_date] = 0.0
            current_date_str = str(current_date)
            
            for expense in expenses:
                if str(expense.expense_date) == current_date_str:
                    daily_spending[current_date] += expense.amount
            
            current_date += timedelta(days=1)
        
        return [
            {'date': date, 'amount': amount}
            for date, amount in sorted(daily_spending.items())
        ]
    
    def get_category_distribution(self, trip_id: int) -> List[Dict]:
        """
        Get pie chart data for budget distribution by category
        
        Returns:
            List of categories with spending amounts
        """
        category_spending = self.calculate_budget_by_category(trip_id)
        total = sum(category_spending.values())
        
        return [
            {
                'category': category,
                'amount': amount,
                'percentage': round((amount / total * 100), 2) if total > 0 else 0
            }
            for category, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
        ]
    
    # ==================== BUDGET ALERTS ====================
    
    def check_budget_alerts(self, trip_id: int) -> List[Dict]:
        """
        Check for budget alerts and warnings
        
        Returns:
            List of active alerts
        """
        alerts = []
        budget_status = self.get_budget_status(trip_id)
        
        # Overall budget alert
        if budget_status['status'] == 'warning':
            alerts.append({
                'type': 'budget_warning',
                'message': f"Budget usage at {budget_status['percentage_used']}%",
                'severity': 'medium'
            })
        elif budget_status['status'] == 'exceeded':
            alerts.append({
                'type': 'budget_exceeded',
                'message': f"Budget exceeded by ₹{abs(budget_status['remaining'])}",
                'severity': 'high'
            })
        
        # Category-level alerts
        breakdowns = self.get_category_breakdown(trip_id)
        for breakdown in breakdowns:
            if breakdown['alert_triggered']:
                alerts.append({
                    'type': 'category_alert',
                    'category': breakdown['category'],
                    'message': f"{breakdown['category']} spending at {breakdown['percentage_used']}%",
                    'severity': 'medium'
                })
        
        return alerts
    
    # ==================== MULTI-PERSON EXPENSE SPLITTING ====================
    
    def calculate_expense_split(self, trip_id: int, num_people: int) -> Dict[str, float]:
        """
        Calculate how expenses should be split among travelers
        
        Args:
            trip_id: ID of the trip
            num_people: Number of people sharing expenses
            
        Returns:
            Dictionary with split amounts
        """
        expenses = self.get_trip_expenses(trip_id)
        expenses_by_person = {}
        
        for expense in expenses:
            if expense.status != 'cancelled':
                per_person = expense.amount / num_people
                
                if expense.paid_by not in expenses_by_person:
                    expenses_by_person[expense.paid_by] = 0.0
                
                expenses_by_person[expense.paid_by] += expense.amount
        
        # Calculate who owes what
        total_spent = sum(expenses_by_person.values())
        per_person_share = total_spent / num_people
        
        settlements = {}
        for person, spent in expenses_by_person.items():
            difference = spent - per_person_share
            settlements[person] = {
                'spent': spent,
                'owes': abs(difference) if difference < 0 else 0,
                'owed': difference if difference > 0 else 0
            }
        
        return settlements


# ==================== USAGE EXAMPLE ====================

if __name__ == "__main__":
    from datetime import timedelta
    
    # Initialize module
    fi = FinancialIntelligence()
    
    # Example usage
    # fi.add_expense(trip_id=1, description="Hotel", amount=5000, category="accommodation")
    # fi.add_expense(trip_id=1, description="Flight", amount=15000, category="transport")
    # fi.add_expense(trip_id=1, description="Dinner", amount=2000, category="food")
    
    # print(f"Total spent: {fi.calculate_total_spent(1)}")
    # print(f"Daily average: {fi.calculate_daily_average(1)}")
    # print(f"Budget status: {fi.get_budget_status(1)}")
    # print(f"Alerts: {fi.check_budget_alerts(1)}")
    
    print("Financial Intelligence Module initialized!")
