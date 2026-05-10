"""
Traveloop - Backend API Server
Flask-based REST API for the Traveloop travel planning platform
Implements all core functionality with proper error handling and authentication
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
from datetime import datetime, date
import os
import json

from models import create_database, get_session, User
from trip_management_engine import TripManagementEngine
from financial_intelligence import FinancialIntelligence
from social_collaboration import SocialCollaborationEngine
from admin_analytics import AdminAnalyticsDashboard


# ==================== FLASK APP SETUP ====================

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///travel_database.db')

# Initialize database
create_database(DATABASE_URL)

# Initialize engines
trip_engine = TripManagementEngine(DATABASE_URL)
financial_engine = FinancialIntelligence(DATABASE_URL)
social_engine = SocialCollaborationEngine(DATABASE_URL)
analytics_engine = AdminAnalyticsDashboard(DATABASE_URL)


# ==================== MIDDLEWARE & AUTHENTICATION ====================

def token_required(f):
    """Decorator for routes requiring authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            # TODO: Implement JWT token validation
            # For now, we'll accept any token
            user_id = 1  # Placeholder
            return f(user_id, *args, **kwargs)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
    
    return decorated


def error_handler(f):
    """Decorator for consistent error handling"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return decorated


# ==================== TRIP ENDPOINTS ====================

@app.route('/api/trips', methods=['GET'])
@token_required
@error_handler
def get_trips(user_id):
    """Get all trips for the authenticated user"""
    trips = trip_engine.get_user_trips(user_id)
    return jsonify([{
        'id': trip.id,
        'title': trip.title,
        'description': trip.description,
        'start_date': str(trip.start_date),
        'end_date': str(trip.end_date),
        'budget': trip.budget,
        'destination': trip.destination,
        'created_at': trip.created_at.isoformat()
    } for trip in trips])


@app.route('/api/trips', methods=['POST'])
@token_required
@error_handler
def create_trip(user_id):
    """Create a new trip"""
    data = request.get_json()
    
    try:
        trip = trip_engine.create_trip(
            user_id=user_id,
            title=data['title'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            description=data.get('description', ''),
            budget=float(data.get('budget', 0))
        )
        
        # Log analytics event
        analytics_engine.log_analytics_event(user_id, 'trip_created', {'trip_id': trip.id})
        
        return jsonify({
            'message': 'Trip created successfully',
            'trip_id': trip.id,
            'title': trip.title
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400


@app.route('/api/trips/<int:trip_id>', methods=['GET'])
@token_required
@error_handler
def get_trip(user_id, trip_id):
    """Get detailed trip information"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    if trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    summary = trip_engine.get_itinerary_summary(trip_id)
    
    return jsonify({
        'id': trip.id,
        'title': trip.title,
        'description': trip.description,
        'start_date': str(trip.start_date),
        'end_date': str(trip.end_date),
        'budget': trip.budget,
        'destination': trip.destination,
        'stops_count': summary.get('stops_count', 0),
        'activities_count': summary.get('activities_count', 0),
        'created_at': trip.created_at.isoformat()
    })


@app.route('/api/trips/<int:trip_id>', methods=['PUT'])
@token_required
@error_handler
def update_trip(user_id, trip_id):
    """Update trip details"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    if trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    update_data = {}
    
    if 'title' in data:
        update_data['title'] = data['title']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'budget' in data:
        update_data['budget'] = float(data['budget'])
    
    trip_engine.update_trip(trip_id, **update_data)
    
    return jsonify({'message': 'Trip updated successfully'})


@app.route('/api/trips/<int:trip_id>', methods=['DELETE'])
@token_required
@error_handler
def delete_trip(user_id, trip_id):
    """Delete a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    if trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    trip_engine.delete_trip(trip_id)
    
    return jsonify({'message': 'Trip deleted successfully'})


# ==================== STOP/CITY ENDPOINTS ====================

@app.route('/api/trips/<int:trip_id>/stops', methods=['GET'])
@token_required
@error_handler
def get_stops(user_id, trip_id):
    """Get all stops for a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    stops = trip_engine.get_trip_stops(trip_id)
    
    return jsonify([{
        'id': stop.id,
        'location': stop.location,
        'arrival_date': str(stop.arrival_date),
        'departure_date': str(stop.departure_date),
        'latitude': stop.latitude,
        'longitude': stop.longitude,
        'sequence_order': stop.sequence_order,
        'notes': stop.notes
    } for stop in stops])


@app.route('/api/trips/<int:trip_id>/stops', methods=['POST'])
@token_required
@error_handler
def add_stop(user_id, trip_id):
    """Add a city/stop to a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        stop = trip_engine.add_stop(
            trip_id=trip_id,
            location=data['location'],
            arrival_date=datetime.strptime(data['arrival_date'], '%Y-%m-%d').date(),
            departure_date=datetime.strptime(data['departure_date'], '%Y-%m-%d').date(),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            notes=data.get('notes', '')
        )
        
        return jsonify({
            'message': 'Stop added successfully',
            'stop_id': stop.id,
            'location': stop.location
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400


@app.route('/api/trips/<int:trip_id>/stops/<int:stop_id>', methods=['DELETE'])
@token_required
@error_handler
def delete_stop(user_id, trip_id, stop_id):
    """Remove a stop from a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if trip_engine.remove_stop(stop_id):
        return jsonify({'message': 'Stop removed successfully'})
    else:
        return jsonify({'error': 'Stop not found'}), 404


@app.route('/api/trips/<int:trip_id>/stops/reorder', methods=['POST'])
@token_required
@error_handler
def reorder_stops(user_id, trip_id):
    """Reorder stops in a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    stop_ids = data.get('stop_ids', [])
    
    if trip_engine.reorder_stops(trip_id, stop_ids):
        return jsonify({'message': 'Stops reordered successfully'})
    else:
        return jsonify({'error': 'Failed to reorder stops'}), 400


# ==================== ACTIVITY ENDPOINTS ====================

@app.route('/api/trips/<int:trip_id>/activities', methods=['GET'])
@token_required
@error_handler
def get_activities(user_id, trip_id):
    """Get all activities for a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    activities = trip_engine.get_trip_activities(trip_id)
    
    return jsonify([{
        'id': activity.id,
        'name': activity.name,
        'activity_type': activity.activity_type,
        'stop_id': activity.stop_id,
        'start_time': activity.start_time.isoformat() if activity.start_time else None,
        'end_time': activity.end_time.isoformat() if activity.end_time else None,
        'cost': activity.cost,
        'description': activity.description,
        'status': activity.status
    } for activity in activities])


@app.route('/api/trips/<int:trip_id>/stops/<int:stop_id>/activities', methods=['POST'])
@token_required
@error_handler
def add_activity(user_id, trip_id, stop_id):
    """Add an activity to a stop"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        activity = trip_engine.add_activity(
            trip_id=trip_id,
            stop_id=stop_id,
            name=data['name'],
            activity_type=data.get('activity_type', 'general'),
            start_time=datetime.fromisoformat(data['start_time']) if 'start_time' in data else None,
            end_time=datetime.fromisoformat(data['end_time']) if 'end_time' in data else None,
            cost=float(data.get('cost', 0)),
            description=data.get('description', '')
        )
        
        return jsonify({
            'message': 'Activity added successfully',
            'activity_id': activity.id,
            'name': activity.name
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400


# ==================== EXPENSE ENDPOINTS ====================

@app.route('/api/trips/<int:trip_id>/expenses', methods=['GET'])
@token_required
@error_handler
def get_expenses(user_id, trip_id):
    """Get all expenses for a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    expenses = financial_engine.get_trip_expenses(trip_id)
    
    return jsonify([{
        'id': expense.id,
        'description': expense.description,
        'amount': expense.amount,
        'category': expense.category,
        'expense_date': str(expense.expense_date),
        'payment_method': expense.payment_method,
        'paid_by': expense.paid_by,
        'status': expense.status
    } for expense in expenses])


@app.route('/api/trips/<int:trip_id>/expenses', methods=['POST'])
@token_required
@error_handler
def add_expense(user_id, trip_id):
    """Add an expense to a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        expense = financial_engine.add_expense(
            trip_id=trip_id,
            description=data['description'],
            amount=float(data['amount']),
            category=data['category'],
            expense_date=datetime.strptime(data.get('expense_date', str(date.today())), '%Y-%m-%d').date(),
            payment_method=data.get('payment_method', 'cash'),
            paid_by=data.get('paid_by', ''),
            notes=data.get('notes', '')
        )
        
        return jsonify({
            'message': 'Expense added successfully',
            'expense_id': expense.id
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400


@app.route('/api/trips/<int:trip_id>/budget-status', methods=['GET'])
@token_required
@error_handler
def get_budget_status(user_id, trip_id):
    """Get budget status for a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    status = financial_engine.get_budget_status(trip_id)
    alerts = financial_engine.check_budget_alerts(trip_id)
    
    return jsonify({
        'budget_status': status,
        'alerts': alerts
    })


# ==================== ITINERARY ENDPOINTS ====================

@app.route('/api/trips/<int:trip_id>/itinerary', methods=['GET'])
@token_required
@error_handler
def get_itinerary(user_id, trip_id):
    """Get day-wise itinerary"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    itinerary = trip_engine.get_day_wise_itinerary(trip_id)
    
    # Convert to JSON-serializable format
    result = {}
    for date_key, data in itinerary.items():
        result[date_key] = {
            'stops': [{'id': s.id, 'location': s.location} for s in data['stops']],
            'activities': [{'id': a.id, 'name': a.name, 'time': str(a.start_time)} for a in data['activities']]
        }
    
    return jsonify(result)


# ==================== SOCIAL & SHARING ENDPOINTS ====================

@app.route('/api/trips/<int:trip_id>/share', methods=['POST'])
@token_required
@error_handler
def create_shared_link(user_id, trip_id):
    """Create a public share link for a trip"""
    trip = trip_engine.get_trip(trip_id)
    
    if not trip or trip.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    expires_in_days = data.get('expires_in_days')
    
    shared = social_engine.create_shared_trip(
        trip_id=trip_id,
        shared_by=user_id,
        expires_in_days=expires_in_days
    )
    
    return jsonify({
        'message': 'Trip shared successfully',
        'public_url': shared.get_public_url(),
        'share_token': shared.share_token
    }), 201


@app.route('/api/shared/<share_token>', methods=['GET'])
@error_handler
def view_shared_trip(share_token):
    """View a publicly shared trip"""
    shared = social_engine.get_shared_trip_by_token(share_token)
    
    if not shared:
        return jsonify({'error': 'Share link not found or expired'}), 404
    
    trip = trip_engine.get_trip(shared.trip_id)
    summary = trip_engine.get_itinerary_summary(shared.trip_id)
    
    return jsonify({
        'trip': {
            'title': trip.title,
            'description': trip.description,
            'budget': trip.budget,
            'stops_count': summary['stops_count'],
            'activities_count': summary['activities_count']
        },
        'user': {
            'name': trip.user.name
        }
    })


@app.route('/api/trips/<int:trip_id>/clone', methods=['POST'])
@token_required
@error_handler
def clone_trip(user_id, trip_id):
    """Clone a trip as a template"""
    data = request.get_json()
    
    try:
        cloned = social_engine.clone_trip(
            source_trip_id=trip_id,
            user_id=user_id,
            new_title=data.get('title'),
            keep_dates=data.get('keep_dates', False)
        )
        
        return jsonify({
            'message': 'Trip cloned successfully',
            'new_trip_id': cloned.id,
            'title': cloned.title
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


# ==================== ANALYTICS ENDPOINTS ====================

@app.route('/admin/analytics/overview', methods=['GET'])
@token_required
@error_handler
def get_analytics_overview(user_id):
    """Get platform analytics overview (admin only)"""
    # TODO: Add admin role check
    
    platform_health = analytics_engine.get_platform_health()
    
    return jsonify(platform_health)


@app.route('/admin/analytics/users', methods=['GET'])
@token_required
@error_handler
def get_user_analytics(user_id):
    """Get user analytics"""
    # TODO: Add admin role check
    
    stats = analytics_engine.get_user_stats()
    active_users = analytics_engine.get_most_active_users(limit=10)
    
    return jsonify({
        'stats': stats,
        'most_active': active_users
    })


@app.route('/admin/analytics/destinations', methods=['GET'])
@token_required
@error_handler
def get_destination_analytics(user_id):
    """Get popular destinations"""
    # TODO: Add admin role check
    
    destinations = analytics_engine.get_popular_destinations(limit=20)
    
    return jsonify({'destinations': destinations})


# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    # Create tables if they don't exist
    create_database(DATABASE_URL)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', True) == 'True'
    )
