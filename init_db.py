"""
Database Initialization Script
Run this script to initialize the database with tables and sample data
"""

import os
import sys
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask and create app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_socketio import SocketIO
from config import config
from app.models import db, User, Task

def create_app(config_name='development'):
    """Create Flask app instance"""
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), 'app', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'app', 'static'))
    
    app.config.from_object(config.get(config_name, config['default']))
    
    db.init_app(app)
    Session(app)
    socketio = SocketIO(app, manage_session=False)
    app.socketio = socketio
    
    from app.routes import auth_bp, task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    
    with app.app_context():
        db.create_all()
    
    return app, socketio


def init_database():
    """Initialize database with tables"""
    app, socketio = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Smart Task Manager - Database Initialization")
        print("=" * 50)
        print()
        
        try:
            # Drop all tables (optional - comment out if you want to keep existing data)
            # print("Dropping existing tables...")
            # db.drop_all()
            
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created successfully")
            print()
            
            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                print("Creating sample admin user...")
                admin = User(
                    username='admin',
                    email='admin@example.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin user created")
                print("  Username: admin")
                print("  Password: admin123")
                print()
                
                # Create sample tasks
                print("Creating sample tasks...")
                sample_tasks = [
                    Task(
                        user_id=admin.id,
                        title='Complete project documentation',
                        description='Write comprehensive documentation for the Smart Task Manager',
                        priority=Task.PRIORITY_HIGH,
                        status=Task.STATUS_IN_PROGRESS,
                        due_date=datetime.utcnow() + timedelta(days=7)
                    ),
                    Task(
                        user_id=admin.id,
                        title='Review code and merge PRs',
                        description='Review pending pull requests and merge them to main branch',
                        priority=Task.PRIORITY_MEDIUM,
                        status=Task.STATUS_PENDING,
                        due_date=datetime.utcnow() + timedelta(days=3)
                    ),
                    Task(
                        user_id=admin.id,
                        title='Setup production deployment',
                        description='Configure production server and deploy application',
                        priority=Task.PRIORITY_HIGH,
                        status=Task.STATUS_PENDING,
                        due_date=datetime.utcnow() + timedelta(days=14)
                    ),
                    Task(
                        user_id=admin.id,
                        title='Write unit tests',
                        description='Write comprehensive unit tests for API endpoints',
                        priority=Task.PRIORITY_MEDIUM,
                        status=Task.STATUS_COMPLETED,
                        due_date=datetime.utcnow() - timedelta(days=5)
                    ),
                    Task(
                        user_id=admin.id,
                        title='Database optimization',
                        description='Optimize database queries and add indexes',
                        priority=Task.PRIORITY_LOW,
                        status=Task.STATUS_PENDING
                    )
                ]
                
                for task in sample_tasks:
                    db.session.add(task)
                
                db.session.commit()
                print(f"✓ Created {len(sample_tasks)} sample tasks")
            else:
                print("✓ Database already initialized")
                print(f"  Found {User.query.count()} user(s)")
                print(f"  Found {Task.query.count()} task(s)")
            
            print()
            print("=" * 50)
            print("Database initialization completed successfully!")
            print("=" * 50)
            print()
            print("Next steps:")
            print("1. Update config.py with your database credentials")
            print("2. Run: python app.py")
            print("3. Navigate to: http://localhost:5000")
            print()
            
        except Exception as e:
            print(f"✗ Error during initialization: {e}")
            db.session.rollback()
            sys.exit(1)


if __name__ == '__main__':
    init_database()
