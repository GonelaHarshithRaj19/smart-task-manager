"""
Main Flask application for Smart Task Manager
Initializes Flask app, database, SocketIO, and routes
"""

from flask import Flask, render_template, redirect, url_for, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session
from config import config
from app.models import db, User, Task
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def create_app(config_name='development'):
    """
    Application factory function to create Flask app
    
    Args:
        config_name (str): Configuration environment (development, testing, production)
        
    Returns:
        Flask: Configured Flask application instance
    """
    
    # Create Flask app instance
    root_dir = os.path.dirname(__file__)
    app = Flask(__name__, 
                template_folder=os.path.join(root_dir, 'app', 'templates'),
                static_folder=os.path.join(root_dir, 'app', 'static'))
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    db.init_app(app)
    Session(app)
    socketio = SocketIO(app, manage_session=False)
    app.socketio = socketio
    
    # Register blueprints
    from app.routes import auth_bp, task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Home page route
    @app.route('/')
    def index():
        """Home page - redirects to dashboard if logged in, otherwise to login"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.login'))
    
    @app.route('/dashboard')
    def dashboard():
        """Dashboard page"""
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('auth.login'))
        
        return render_template('dashboard.html', user=user)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return {'error': 'Page not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    # WebSocket event handlers
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        if 'user_id' in session:
            user_id = session['user_id']
            join_room(f'user_{user_id}')
            print(f'User {user_id} connected')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        if 'user_id' in session:
            user_id = session['user_id']
            leave_room(f'user_{user_id}')
            print(f'User {user_id} disconnected')
    
    @socketio.on('message')
    def handle_message(data):
        """Handle generic messages"""
        if 'user_id' in session:
            user_id = session['user_id']
            emit('response', {'data': data}, room=f'user_{user_id}')
    
    return app, socketio


# Create app instance
app, socketio = create_app()


if __name__ == '__main__':
    # Run the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
