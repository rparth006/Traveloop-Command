"""
Traveloop - Admin Analytics Dashboard
Platform analytics, user engagement metrics, and business intelligence
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from models import (User, Trip, Stop, Activity, Expense, SharedTrip, 
                   AnalyticsEvent, PopularDestination, get_session)
from sqlalchemy import func, extract
import json


class AdminAnalyticsDashboard:
    """
    Comprehensive analytics for platform administrators
    Tracks user engagement, popular destinations, usage patterns, and business metrics
    """
    
    def __init__(self, database_url='sqlite:///travel_database.db'):
        """Initialize the analytics dashboard"""
        self.database_url = database_url
        self.session = get_session(database_url)
    
    # ==================== USER ANALYTICS ====================
    
    def get_user_stats(self) -> Dict:
        """Get comprehensive user statistics"""
        total_users = self.session.query(func.count(User.id)).scalar() or 0
        
        # Users by registration date (last 30 days)
        last_month = datetime.utcnow() - timedelta(days=30)
        new_users_month = self.session.query(func.count(User.id)).filter(
            User.created_at >= last_month
        ).scalar() or 0
        
        # Active users (those with trips)
        active_users = self.session.query(func.count(User.id)).filter(
            User.trips.any()
        ).scalar() or 0
        
        return {
            'total_users': total_users,
            'new_users_last_month': new_users_month,
            'active_users': active_users,
            'activation_rate': round((active_users / total_users * 100) if total_users > 0 else 0, 2)
        }
    
    def get_user_growth_trend(self, days: int = 30) -> List[Dict]:
        """
        Get user growth trend over specified days
        
        Returns:
            Daily user count for the specified period
        """
        trend = []
        start_date = datetime.utcnow() - timedelta(days=days)
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            count = self.session.query(func.count(User.id)).filter(
                User.created_at <= current_date
            ).scalar() or 0
            
            trend.append({
                'date': current_date.date(),
                'total_users': count
            })
        
        return trend
    
    def get_most_active_users(self, limit: int = 10) -> List[Dict]:
        """Get most active users by number of trips"""
        active_users = self.session.query(
            User.id,
            User.name,
            User.email,
            func.count(Trip.id).label('trip_count')
        ).outerjoin(Trip).group_by(User.id).order_by(
            func.count(Trip.id).desc()
        ).limit(limit).all()
        
        return [
            {
                'user_id': user[0],
                'name': user[1],
                'email': user[2],
                'trip_count': user[3] or 0
            }
            for user in active_users
        ]
    
    # ==================== TRIP & ITINERARY ANALYTICS ====================
    
    def get_trip_stats(self) -> Dict:
        """Get comprehensive trip statistics"""
        total_trips = self.session.query(func.count(Trip.id)).scalar() or 0
        
        # Average trip duration
        trips = self.session.query(Trip).all()
        if trips:
            total_duration = sum((trip.end_date - trip.start_date).days + 1 for trip in trips)
            avg_duration = total_duration / len(trips)
        else:
            avg_duration = 0
        
        # Total stops and activities
        total_stops = self.session.query(func.count(Stop.id)).scalar() or 0
        total_activities = self.session.query(func.count(Activity.id)).scalar() or 0
        
        # Average budget
        avg_budget = self.session.query(func.avg(Trip.budget)).scalar() or 0
        
        return {
            'total_trips': total_trips,
            'average_trip_duration': round(avg_duration, 1),
            'total_stops': total_stops,
            'total_activities': total_activities,
            'average_stops_per_trip': round(total_stops / total_trips, 1) if total_trips > 0 else 0,
            'average_activities_per_trip': round(total_activities / total_trips, 1) if total_trips > 0 else 0,
            'average_budget': round(avg_budget, 2)
        }
    
    def get_trip_creation_trend(self, days: int = 30) -> List[Dict]:
        """Get daily trip creation trend"""
        trend = []
        start_date = datetime.utcnow() - timedelta(days=days)
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            next_date = current_date + timedelta(days=1)
            
            count = self.session.query(func.count(Trip.id)).filter(
                Trip.created_at >= current_date,
                Trip.created_at < next_date
            ).scalar() or 0
            
            trend.append({
                'date': current_date.date(),
                'trips_created': count
            })
        
        return trend
    
    def get_trips_by_destination(self, limit: int = 20) -> List[Dict]:
        """Get most visited destinations"""
        results = self.session.query(
            Trip.destination,
            func.count(Trip.id).label('count')
        ).group_by(Trip.destination).order_by(
            func.count(Trip.id).desc()
        ).limit(limit).all()
        
        return [
            {'destination': dest, 'trip_count': count}
            for dest, count in results
        ]
    
    # ==================== FINANCIAL ANALYTICS ====================
    
    def get_financial_stats(self) -> Dict:
        """Get financial metrics"""
        total_expenses = self.session.query(func.sum(Expense.amount)).scalar() or 0
        
        avg_trip_budget = self.session.query(func.avg(Trip.budget)).scalar() or 0
        
        # Expense breakdown by category
        category_totals = self.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total')
        ).filter(Expense.status != 'cancelled').group_by(
            Expense.category
        ).all()
        
        category_breakdown = {cat: total for cat, total in category_totals}
        
        return {
            'total_expenses': round(total_expenses, 2),
            'average_trip_budget': round(avg_trip_budget, 2),
            'average_daily_spending': round(total_expenses / 30, 2),  # Simplified
            'category_breakdown': {cat: round(amt, 2) for cat, amt in category_breakdown.items()}
        }
    
    def get_spending_by_category(self) -> List[Dict]:
        """Get spending distribution across categories"""
        results = self.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).filter(Expense.status != 'cancelled').group_by(
            Expense.category
        ).order_by(
            func.sum(Expense.amount).desc()
        ).all()
        
        total = sum(amt for _, amt, _ in results)
        
        return [
            {
                'category': cat,
                'total_amount': round(amt, 2),
                'count': count,
                'percentage': round((amt / total * 100) if total > 0 else 0, 2),
                'average_per_expense': round(amt / count, 2) if count > 0 else 0
            }
            for cat, amt, count in results
        ]
    
    # ==================== SOCIAL & ENGAGEMENT ANALYTICS ====================
    
    def get_social_stats(self) -> Dict:
        """Get social engagement metrics"""
        total_shares = self.session.query(func.count(SharedTrip.id)).scalar() or 0
        
        total_clones = self.session.query(func.sum(SharedTrip.copy_count)).scalar() or 0
        
        active_shares = self.session.query(func.count(SharedTrip.id)).filter(
            (SharedTrip.expires_at.is_(None)) | (SharedTrip.expires_at > datetime.utcnow())
        ).scalar() or 0
        
        avg_clones = self.session.query(func.avg(SharedTrip.copy_count)).scalar() or 0
        
        return {
            'total_shares': total_shares,
            'active_shares': active_shares,
            'total_clones': int(total_clones),
            'average_clones_per_share': round(avg_clones, 2),
            'sharing_adoption_rate': round((total_shares / self.session.query(func.count(Trip.id)).scalar() * 100) if self.session.query(func.count(Trip.id)).scalar() > 0 else 0, 2)
        }
    
    # ==================== ACTIVITY ANALYTICS ====================
    
    def get_popular_activities(self, limit: int = 15) -> List[Dict]:
        """Get most popular activity types"""
        results = self.session.query(
            Activity.activity_type,
            func.count(Activity.id).label('count'),
            func.avg(Activity.cost).label('avg_cost')
        ).filter(Activity.activity_type.isnot(None)).group_by(
            Activity.activity_type
        ).order_by(
            func.count(Activity.id).desc()
        ).limit(limit).all()
        
        return [
            {
                'activity_type': act_type,
                'count': count,
                'average_cost': round(avg_cost, 2) if avg_cost else 0
            }
            for act_type, count, avg_cost in results
        ]
    
    # ==================== DESTINATION ANALYTICS ====================
    
    def track_destination_popularity(self) -> None:
        """Update destination popularity scores"""
        # Get all destinations and their trip counts
        dest_counts = self.session.query(
            Trip.destination,
            func.count(Trip.id).label('count')
        ).group_by(Trip.destination).all()
        
        for destination, count in dest_counts:
            # Update or create PopularDestination entry
            pop_dest = self.session.query(PopularDestination).filter(
                PopularDestination.city_name == destination
            ).first()
            
            if po_dest:
                pop_dest.trip_count = count
                pop_dest.popularity_score = min(100, count * 10)  # Simple scoring
                pop_dest.last_updated = datetime.utcnow()
            else:
                pop_dest = PopularDestination(
                    city_name=destination,
                    trip_count=count,
                    popularity_score=min(100, count * 10),
                    last_updated=datetime.utcnow()
                )
                self.session.add(pop_dest)
        
        self.session.commit()
    
    def get_popular_destinations(self, limit: int = 20) -> List[Dict]:
        """Get most popular destinations"""
        results = self.session.query(PopularDestination).order_by(
            PopularDestination.popularity_score.desc()
        ).limit(limit).all()
        
        return [
            {
                'destination': dest.city_name,
                'country': dest.country,
                'trip_count': dest.trip_count,
                'popularity_score': round(dest.popularity_score, 2),
                'average_cost_index': dest.average_cost_index or 0
            }
            for dest in results
        ]
    
    # ==================== PLATFORM HEALTH METRICS ====================
    
    def get_platform_health(self) -> Dict:
        """Get overall platform health metrics"""
        stats = {
            'users': self.get_user_stats(),
            'trips': self.get_trip_stats(),
            'financial': self.get_financial_stats(),
            'social': self.get_social_stats()
        }
        
        # Calculate health score (0-100)
        health_score = 0
        
        # User engagement component (40 points)
        health_score += min(40, (stats['users']['active_users'] / max(stats['users']['total_users'], 1)) * 40)
        
        # Trip activity component (30 points)
        trips_per_user = (stats['trips']['total_trips'] / max(stats['users']['total_users'], 1))
        health_score += min(30, (trips_per_user / 2) * 30)
        
        # Social engagement component (30 points)
        share_adoption = stats['social']['sharing_adoption_rate']
        health_score += min(30, (share_adoption / 100) * 30)
        
        stats['platform_health_score'] = round(health_score, 1)
        stats['status'] = 'excellent' if health_score >= 80 else 'good' if health_score >= 60 else 'needs_improvement'
        
        return stats
    
    # ==================== CUSTOM REPORTS ====================
    
    def generate_summary_report(self, days: int = 30) -> Dict:
        """Generate a comprehensive summary report"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        new_users = self.session.query(func.count(User.id)).filter(
            User.created_at >= start_date
        ).scalar() or 0
        
        new_trips = self.session.query(func.count(Trip.id)).filter(
            Trip.created_at >= start_date
        ).scalar() or 0
        
        new_shares = self.session.query(func.count(SharedTrip.id)).filter(
            SharedTrip.shared_on >= start_date
        ).scalar() or 0
        
        expense_amount = self.session.query(func.sum(Expense.amount)).filter(
            Expense.created_at >= start_date,
            Expense.status != 'cancelled'
        ).scalar() or 0
        
        return {
            'period_days': days,
            'new_users': new_users,
            'new_trips': new_trips,
            'new_shares': new_shares,
            'total_expenses_tracked': round(expense_amount, 2),
            'report_generated': datetime.utcnow().isoformat()
        }
    
    # ==================== USAGE EXAMPLE ====================
    
    def log_analytics_event(self, user_id: int, event_type: str, event_data: Dict = None) -> AnalyticsEvent:
        """Log an analytics event for future analysis"""
        event = AnalyticsEvent(
            user_id=user_id,
            event_type=event_type,
            event_data=event_data or {}
        )
        self.session.add(event)
        self.session.commit()
        return event


if __name__ == "__main__":
    # Initialize dashboard
    dashboard = AdminAnalyticsDashboard()
    
    # Example usage
    # print("User Stats:", dashboard.get_user_stats())
    # print("Trip Stats:", dashboard.get_trip_stats())
    # print("Platform Health:", dashboard.get_platform_health())
    # print("Popular Destinations:", dashboard.get_popular_destinations())
    
    print("Admin Analytics Dashboard initialized!")
