"""
Task management routes with REST API endpoints
Handles task CRUD operations and returns JSON responses
"""

from flask import Blueprint, request, jsonify, session, current_app
from app.models import db, Task, User
from functools import wraps
from datetime import datetime


# Create task blueprint
task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


def api_login_required(f):
    """Decorator to check if user is logged in for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


@task_bp.route('', methods=['GET'])
@api_login_required
def get_tasks():
    """
    Get all tasks for the current user
    
    Query parameters:
    - status: Filter by status (pending, in_progress, completed)
    - priority: Filter by priority (low, medium, high)
    - sort_by: Sort by field (created_date, due_date, priority)
    
    Returns:
        JSON: List of tasks
    """
    user_id = session['user_id']
    
    try:
        # Base query
        query = Task.query.filter_by(user_id=user_id)
        
        # Filter by status if provided
        status = request.args.get('status')
        if status and status in Task.STATUS_CHOICES:
            query = query.filter_by(status=status)
        
        # Filter by priority if provided
        priority = request.args.get('priority')
        if priority and priority in Task.PRIORITY_CHOICES:
            query = query.filter_by(priority=priority)
        
        # Sort by field if provided
        sort_by = request.args.get('sort_by', 'created_date')
        if sort_by == 'created_date':
            query = query.order_by(Task.created_date.desc())
        elif sort_by == 'due_date':
            query = query.order_by(Task.due_date)
        elif sort_by == 'priority':
            # Custom ordering: high > medium > low
            priority_order = {Task.PRIORITY_HIGH: 0, Task.PRIORITY_MEDIUM: 1, Task.PRIORITY_LOW: 2}
            query = query.order_by(
                db.case(priority_order, value=Task.priority)
            )
        
        tasks = query.all()
        
        return jsonify({
            'success': True,
            'data': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['GET'])
@api_login_required
def get_task(task_id):
    """
    Get a single task by ID
    
    Args:
        task_id: Task ID
        
    Returns:
        JSON: Task data
    """
    user_id = session['user_id']
    
    try:
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        return jsonify({
            'success': True,
            'data': task.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('', methods=['POST'])
@api_login_required
def create_task():
    """
    Create a new task
    
    Request body:
    {
        'title': 'Task title',
        'description': 'Task description (optional)',
        'priority': 'high|medium|low',
        'due_date': 'YYYY-MM-DD (optional)'
    }
    
    Returns:
        JSON: Created task data
    """
    user_id = session['user_id']
    data = request.get_json()
    
    # Validation
    errors = []
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    title = data.get('title', '').strip()
    if not title:
        errors.append('Title is required')
    elif len(title) > 255:
        errors.append('Title must be less than 255 characters')
    
    priority = data.get('priority', Task.PRIORITY_MEDIUM)
    if priority not in Task.PRIORITY_CHOICES:
        errors.append(f'Invalid priority. Must be one of: {", ".join(Task.PRIORITY_CHOICES)}')
    
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    
    try:
        # Create new task
        new_task = Task(
            user_id=user_id,
            title=title,
            description=data.get('description', '').strip(),
            priority=priority,
            status=Task.STATUS_PENDING
        )
        
        # Parse due_date if provided
        due_date_str = data.get('due_date')
        if due_date_str:
            try:
                new_task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        db.session.add(new_task)
        db.session.commit()
        
        # Emit WebSocket event
        current_app.socketio.emit('task_created', new_task.to_dict(), room=f'user_{user_id}')
        
        return jsonify({
            'success': True,
            'data': new_task.to_dict(),
            'message': 'Task created successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['PUT'])
@api_login_required
def update_task(task_id):
    """
    Update an existing task
    
    Args:
        task_id: Task ID
        
    Returns:
        JSON: Updated task data
    """
    user_id = session['user_id']
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    try:
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        # Update fields
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({'success': False, 'error': 'Title cannot be empty'}), 400
            task.title = title
        
        if 'description' in data:
            task.description = data['description'].strip()
        
        if 'priority' in data:
            if data['priority'] not in Task.PRIORITY_CHOICES:
                return jsonify({'success': False, 'error': 'Invalid priority'}), 400
            task.priority = data['priority']
        
        if 'status' in data:
            if data['status'] not in Task.STATUS_CHOICES:
                return jsonify({'success': False, 'error': 'Invalid status'}), 400
            task.status = data['status']
        
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            else:
                task.due_date = None
        
        db.session.commit()
        
        # Emit WebSocket event
        current_app.socketio.emit('task_updated', task.to_dict(), room=f'user_{user_id}')
        
        return jsonify({
            'success': True,
            'data': task.to_dict(),
            'message': 'Task updated successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@api_login_required
def delete_task(task_id):
    """
    Delete a task
    
    Args:
        task_id: Task ID
        
    Returns:
        JSON: Success message
    """
    user_id = session['user_id']
    
    try:
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        # Emit WebSocket event
        current_app.socketio.emit('task_deleted', {'id': task_id}, room=f'user_{user_id}')
        
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@task_bp.route('/stats', methods=['GET'])
@api_login_required
def get_task_stats():
    """
    Get task statistics for the current user
    Uses Pandas and NumPy for calculations
    
    Returns:
        JSON: Task statistics
    """
    user_id = session['user_id']
    
    try:
        import pandas as pd
        import numpy as np
        
        # Fetch all tasks for the user
        tasks = Task.query.filter_by(user_id=user_id).all()
        
        if not tasks:
            return jsonify({
                'success': True,
                'data': {
                    'total_tasks': 0,
                    'completed_tasks': 0,
                    'pending_tasks': 0,
                    'in_progress_tasks': 0,
                    'completion_percentage': 0,
                    'high_priority_tasks': 0,
                    'medium_priority_tasks': 0,
                    'low_priority_tasks': 0,
                    'average_completion_time': None
                }
            }), 200
        
        # Convert tasks to DataFrame
        task_data = []
        for task in tasks:
            task_data.append({
                'id': task.id,
                'status': task.status,
                'priority': task.priority,
                'created_date': task.created_date,
                'updated_date': task.updated_date
            })
        
        df = pd.DataFrame(task_data)
        
        # Calculate statistics
        total_tasks = len(df)
        completed_tasks = len(df[df['status'] == Task.STATUS_COMPLETED])
        pending_tasks = len(df[df['status'] == Task.STATUS_PENDING])
        in_progress_tasks = len(df[df['status'] == Task.STATUS_IN_PROGRESS])
        
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        completion_percentage = round(completion_percentage, 2)
        
        # Priority counts
        high_priority_tasks = len(df[df['priority'] == Task.PRIORITY_HIGH])
        medium_priority_tasks = len(df[df['priority'] == Task.PRIORITY_MEDIUM])
        low_priority_tasks = len(df[df['priority'] == Task.PRIORITY_LOW])
        
        # Average completion time (in days)
        completed_df = df[df['status'] == Task.STATUS_COMPLETED]
        if len(completed_df) > 0:
            completion_times = (completed_df['updated_date'] - completed_df['created_date']).dt.days
            average_completion_time = float(np.mean(completion_times))
        else:
            average_completion_time = None
        
        return jsonify({
            'success': True,
            'data': {
                'total_tasks': int(total_tasks),
                'completed_tasks': int(completed_tasks),
                'pending_tasks': int(pending_tasks),
                'in_progress_tasks': int(in_progress_tasks),
                'completion_percentage': completion_percentage,
                'high_priority_tasks': int(high_priority_tasks),
                'medium_priority_tasks': int(medium_priority_tasks),
                'low_priority_tasks': int(low_priority_tasks),
                'average_completion_time': average_completion_time
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
