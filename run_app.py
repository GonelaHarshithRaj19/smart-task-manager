#!/usr/bin/env python
"""
Smart Task Manager - Application Entry Point
Run this file to start the Flask application
"""

from app import create_app, db
from app.models import User, Task
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# Register CLI commands
@app.shell_context_processor
def make_shell_context():
    """Create shell context for flask shell"""
    return {'db': db, 'User': User, 'Task': Task}

@app.cli.command()
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")

@app.cli.command()
def seed_db():
    """Add sample data to database"""
    from datetime import datetime, timedelta
    
    with app.app_context():
        # Check if test user already exists
        if User.query.filter_by(username='testuser').first():
            print("ℹ️  Test user already exists")
            return
        
        # Create test user
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()
        
        # Create sample tasks
        tasks = [
            Task(
                user_id=test_user.id,
                title='Welcome to Smart Task Manager',
                description='This is your first task. Edit, delete, or mark as complete.',
                priority='high',
                status='pending'
            ),
            Task(
                user_id=test_user.id,
                title='Setup PostgreSQL',
                description='Configure and connect PostgreSQL database.',
                priority='high',
                status='in_progress',
                due_date=datetime.utcnow() + timedelta(days=1)
            ),
            Task(
                user_id=test_user.id,
                title='Review Project Code',
                description='Code review and quality improvements.',
                priority='medium',
                status='pending',
                due_date=datetime.utcnow() + timedelta(days=3)
            ),
        ]
        
        for task in tasks:
            db.session.add(task)
        
        db.session.commit()
        print("✅ Sample data added successfully!")
        print(f"   - Test User: testuser / password123")
        print(f"   - Test Email: test@example.com")
        print(f"   - Sample Tasks: 3")

if __name__ == '__main__':
    # Get configuration
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print("=" * 60)
    print("🚀 Smart Task Manager - Starting Application")
    print("=" * 60)
    print(f"📍 URL: http://localhost:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"💾 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("=" * 60)
    print("Press CTRL+C to stop the server\n")
    
    # Run the application
    app.socketio.run(app, host='0.0.0.0', port=port, debug=debug)
