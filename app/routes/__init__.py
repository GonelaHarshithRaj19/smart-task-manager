"""
Routes package for Flask application
Imports and exposes all blueprints
"""

from app.routes.auth import auth_bp
from app.routes.task import task_bp

__all__ = ['auth_bp', 'task_bp']
