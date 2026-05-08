"""
Database models for Smart Task Manager
Uses SQLAlchemy ORM to define User and Task tables
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    """
    User model representing registered users in the system
    
    Attributes:
        id: Primary key, unique identifier
        username: Username for login (unique)
        email: User email address (unique)
        password: Hashed password using bcrypt
        created_date: Account creation timestamp
        tasks: Relationship to user's tasks
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship to tasks
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """
        Hash and set password using bcrypt
        
        Args:
            password (str): Plain text password
        """
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')
    
    def check_password(self, password):
        """
        Verify password against stored hash
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_date': self.created_date.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    """
    Task model representing tasks created by users
    
    Attributes:
        id: Primary key, unique identifier
        user_id: Foreign key to User
        title: Task title
        description: Detailed task description
        priority: Task priority (high, medium, low)
        status: Task status (pending, in_progress, completed)
        created_date: Task creation timestamp
        updated_date: Last update timestamp
        due_date: Optional due date for task
    """
    __tablename__ = 'tasks'
    
    # Status options
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED]
    
    # Priority options
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH]
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default=PRIORITY_MEDIUM, nullable=False)
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False, index=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert task object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None
        }
    
    def __repr__(self):
        return f'<Task {self.title}>'
