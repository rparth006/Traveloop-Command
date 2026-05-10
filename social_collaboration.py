"""
Traveloop - Social & Collaboration Features
Public sharing, trip cloning, collaborative planning, and social engagement
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from models import Trip, User, SharedTrip, get_session
from sqlalchemy import func
import uuid
import copy


class SocialCollaborationEngine:
    """
    Social features and collaborative travel planning
    Handles sharing, cloning, and community engagement
    """
    
    def __init__(self, database_url='sqlite:///travel_database.db'):
        """Initialize the social collaboration engine"""
        self.database_url = database_url
        self.session = get_session(database_url)
    
    # ==================== TRIP SHARING ====================
    
    def create_shared_trip(self, trip_id: int, shared_by: int, 
                          is_public: bool = True, expires_in_days: int = None) -> SharedTrip:
        """
        Create a public share link for a trip
        
        Args:
            trip_id: ID of the trip to share
            shared_by: ID of the user sharing
            is_public: Whether it's publicly accessible
            expires_in_days: Optional expiration time
            
        Returns:
            SharedTrip object with public URL
        """
        share_token = str(uuid.uuid4())
        
        shared_trip = SharedTrip(
            trip_id=trip_id,
            share_token=share_token,
            shared_by=shared_by,
            is_public=is_public,
            shared_on=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days) if expires_in_days else None
        )
        
        self.session.add(shared_trip)
        self.session.commit()
        return shared_trip
    
    def get_shared_trip_by_token(self, share_token: str) -> Optional[SharedTrip]:
        """Get a shared trip by its public token"""
        shared = self.session.query(SharedTrip).filter(SharedTrip.share_token == share_token).first()
        
        # Check if expired
        if shared and shared.expires_at and shared.expires_at < datetime.utcnow():
            return None
        
        return shared
    
    def get_trip_shares(self, trip_id: int) -> List[SharedTrip]:
        """Get all shares for a specific trip"""
        return self.session.query(SharedTrip).filter(SharedTrip.trip_id == trip_id).all()
    
    def revoke_shared_trip(self, share_id: int) -> bool:
        """Revoke a shared trip link"""
        shared = self.session.query(SharedTrip).filter(SharedTrip.id == share_id).first()
        if shared:
            self.session.delete(shared)
            self.session.commit()
            return True
        return False
    
    def get_public_url(self, trip_id: int) -> Optional[str]:
        """Get the public URL for a trip"""
        shares = self.get_trip_shares(trip_id)
        if shares:
            # Return first active share
            for share in shares:
                if not share.expires_at or share.expires_at > datetime.utcnow():
                    return share.get_public_url()
        return None
    
    # ==================== TRIP CLONING ====================
    
    def clone_trip(self, source_trip_id: int, user_id: int, 
                   new_title: str = None, keep_dates: bool = False) -> Trip:
        """
        Create a copy of a trip (template cloning)
        
        Args:
            source_trip_id: ID of the trip to clone
            user_id: ID of the user cloning the trip
            new_title: Title for the cloned trip (optional)
            keep_dates: Whether to keep the same dates or shift to current dates
            
        Returns:
            New Trip object
        """
        source_trip = self.session.query(Trip).filter(Trip.id == source_trip_id).first()
        
        if not source_trip:
            raise ValueError("Source trip not found")
        
        # Create new trip
        new_title = new_title or f"{source_trip.title} (Copy)"
        
        if keep_dates:
            new_start = source_trip.start_date
            new_end = source_trip.end_date
        else:
            # Shift dates to current date + offset
            today = datetime.utcnow().date()
            date_offset = (today - source_trip.start_date).days
            new_start = source_trip.start_date + timedelta(days=date_offset)
            new_end = source_trip.end_date + timedelta(days=date_offset)
        
        cloned_trip = Trip(
            user_id=user_id,
            title=new_title,
            description=source_trip.description,
            start_date=new_start,
            end_date=new_end,
            destination=source_trip.destination,
            budget=source_trip.budget
        )
        
        self.session.add(cloned_trip)
        self.session.commit()
        
        # Clone stops and activities
        from trip_management_engine import TripManagementEngine
        engine = TripManagementEngine(self.database_url)
        
        for stop in source_trip.stops:
            new_arrival = stop.arrival_date + timedelta(days=date_offset) if not keep_dates else stop.arrival_date
            new_departure = stop.departure_date + timedelta(days=date_offset) if not keep_dates else stop.departure_date
            
            new_stop = engine.add_stop(
                trip_id=cloned_trip.id,
                location=stop.location,
                arrival_date=new_arrival,
                departure_date=new_departure,
                latitude=stop.latitude,
                longitude=stop.longitude,
                notes=stop.notes
            )
            
            # Clone activities for this stop
            for activity in stop.activities:
                new_start_time = activity.start_time
                new_end_time = activity.end_time
                
                if new_start_time and not keep_dates:
                    new_start_time = activity.start_time + timedelta(days=date_offset)
                if new_end_time and not keep_dates:
                    new_end_time = activity.end_time + timedelta(days=date_offset)
                
                engine.add_activity(
                    trip_id=cloned_trip.id,
                    stop_id=new_stop.id,
                    name=activity.name,
                    activity_type=activity.activity_type,
                    start_time=new_start_time,
                    end_time=new_end_time,
                    cost=activity.cost,
                    description=activity.description
                )
        
        # Update share count
        share = self.get_shared_trip_by_token(source_trip.id)
        if share:
            share.copy_count += 1
            self.session.commit()
        
        return cloned_trip
    
    # ==================== SOCIAL ENGAGEMENT ====================
    
    def get_trending_trips(self, limit: int = 10) -> List[Trip]:
        """Get trending trips based on copy count"""
        trending_shares = self.session.query(SharedTrip).order_by(
            SharedTrip.copy_count.desc()
        ).limit(limit).all()
        
        trending_trips = []
        for share in trending_shares:
            trip = self.session.query(Trip).filter(Trip.id == share.trip_id).first()
            if trip:
                trending_trips.append(trip)
        
        return trending_trips
    
    def get_popular_destinations_from_trips(self, limit: int = 10) -> List[Dict]:
        """
        Get most visited destinations across all trips
        Useful for dashboard and recommendations
        """
        from sqlalchemy import text
        
        # Query to get most common stops
        result = self.session.query(
            func.lower(Trip.destination).label('destination'),
            func.count(Trip.id).label('trip_count')
        ).group_by(func.lower(Trip.destination)).order_by(
            func.count(Trip.id).desc()
        ).limit(limit).all()
        
        return [
            {'destination': row[0], 'trip_count': row[1]}
            for row in result
        ]
    
    def get_user_community_stats(self) -> Dict:
        """Get community statistics"""
        total_users = self.session.query(func.count(User.id)).scalar()
        total_trips = self.session.query(func.count(Trip.id)).scalar()
        total_shares = self.session.query(func.count(SharedTrip.id)).scalar()
        total_clones = self.session.query(func.sum(SharedTrip.copy_count)).scalar()
        
        return {
            'total_users': total_users or 0,
            'total_trips': total_trips or 0,
            'total_shares': total_shares or 0,
            'total_clones': total_clones or 0
        }
    
    # ==================== COLLABORATIVE PLANNING ====================
    
    def add_collaborator(self, trip_id: int, collaborator_email: str) -> bool:
        """
        Add a collaborator to a trip (future feature)
        
        Note: This is a placeholder for full collaborative features
        In production, implement with a TripCollaborator model
        """
        # TODO: Implement collaborator management
        # This would involve:
        # - Sending invitations
        # - Managing permissions (view, edit, comment)
        # - Real-time sync of changes
        pass
    
    def get_team_trips(self, user_id: int) -> List[Trip]:
        """Get trips where user is a collaborator or owner"""
        # For now, return user's own trips
        # In production, expand to include collaborative trips
        return self.session.query(Trip).filter(Trip.user_id == user_id).all()
    
    # ==================== SOCIAL METRICS ====================
    
    def get_trip_engagement(self, trip_id: int) -> Dict:
        """Get engagement metrics for a shared trip"""
        shares = self.session.query(SharedTrip).filter(SharedTrip.trip_id == trip_id).all()
        
        total_copies = 0
        total_views = 0  # Placeholder for view tracking
        active_shares = 0
        
        for share in shares:
            if not share.expires_at or share.expires_at > datetime.utcnow():
                active_shares += 1
            total_copies += share.copy_count
        
        return {
            'active_shares': active_shares,
            'total_copies': total_copies,
            'total_views': total_views,
            'engagement_score': total_copies + (active_shares * 10)
        }
    
    def get_user_activity_feed(self, user_id: int) -> List[Dict]:
        """
        Get activity feed for a user
        Shows recent trips, shares, and clones
        """
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        activities = []
        
        # Get user's trips
        for trip in user.trips:
            activities.append({
                'type': 'trip_created',
                'title': trip.title,
                'timestamp': trip.created_at,
                'trip_id': trip.id
            })
            
            # Get shares for this trip
            for share in self.get_trip_shares(trip.id):
                activities.append({
                    'type': 'trip_shared',
                    'title': f"Shared: {trip.title}",
                    'timestamp': share.shared_on,
                    'trip_id': trip.id
                })
        
        # Sort by timestamp (newest first)
        return sorted(activities, key=lambda x: x['timestamp'], reverse=True)[:10]
    
    # ==================== SHARING ANALYTICS ====================
    
    def get_sharing_stats(self) -> Dict:
        """Get platform-wide sharing statistics"""
        total_shares = self.session.query(func.count(SharedTrip.id)).scalar()
        total_clones = self.session.query(func.sum(SharedTrip.copy_count)).scalar()
        average_clones = self.session.query(func.avg(SharedTrip.copy_count)).scalar()
        
        active_shares = self.session.query(func.count(SharedTrip.id)).filter(
            (SharedTrip.expires_at.is_(None)) | (SharedTrip.expires_at > datetime.utcnow())
        ).scalar()
        
        return {
            'total_shares': total_shares or 0,
            'active_shares': active_shares or 0,
            'total_clones': int(total_clones) if total_clones else 0,
            'average_clones_per_share': round(average_clones or 0, 2)
        }


# ==================== USAGE EXAMPLE ====================

if __name__ == "__main__":
    # Initialize engine
    sce = SocialCollaborationEngine()
    
    # Example usage
    # Create a shared link
    # shared = sce.create_shared_trip(trip_id=1, shared_by=1, expires_in_days=30)
    # print(f"Public URL: {shared.get_public_url()}")
    
    # Clone a trip
    # cloned_trip = sce.clone_trip(source_trip_id=1, user_id=2, new_title="My Europe Trip")
    # print(f"Trip cloned: {cloned_trip}")
    
    # Get trending trips
    # trending = sce.get_trending_trips()
    # print(f"Trending: {trending}")
    
    print("Social Collaboration Engine initialized!")
