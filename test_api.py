"""
API Testing Script
Tests all REST API endpoints to ensure they work correctly
Run this script after starting the application
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5000'

# Test data
TEST_USER = {
    'username': 'apitest_' + datetime.now().strftime('%Y%m%d%H%M%S'),
    'email': f'test_{datetime.now().strftime("%Y%m%d%H%M%S")}@example.com',
    'password': 'testpass123',
    'confirm_password': 'testpass123'
}

def print_result(test_name, status, message=""):
    """Print test result"""
    status_symbol = "✅" if status else "❌"
    print(f"{status_symbol} {test_name}")
    if message:
        print(f"   └─ {message}")

def test_authentication():
    """Test user registration and login"""
    print("\n📝 Testing Authentication...")
    session = requests.Session()
    
    # Test 1: Register user
    print("  1. Testing user registration...")
    response = session.post(
        f'{BASE_URL}/auth/register',
        json=TEST_USER
    )
    print_result("User Registration", response.status_code in [201, 302], 
                f"Status: {response.status_code}")
    
    # Test 2: Login
    print("  2. Testing user login...")
    response = session.post(
        f'{BASE_URL}/auth/login',
        json={'username': TEST_USER['username'], 'password': TEST_USER['password']}
    )
    print_result("User Login", response.status_code in [200, 302],
                f"Status: {response.status_code}")
    
    return session

def test_task_api(session):
    """Test task CRUD operations"""
    print("\n📋 Testing Task API...")
    
    # Test 1: Create task
    print("  1. Testing create task...")
    task_data = {
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'high',
        'due_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    }
    response = session.post(
        f'{BASE_URL}/api/tasks',
        json=task_data
    )
    print_result("Create Task", response.status_code == 201,
                f"Status: {response.status_code}")
    
    task_id = None
    if response.status_code == 201:
        data = response.json()
        if data.get('success'):
            task_id = data.get('data', {}).get('id')
    
    # Test 2: Get all tasks
    print("  2. Testing get all tasks...")
    response = session.get(f'{BASE_URL}/api/tasks')
    print_result("Get All Tasks", response.status_code == 200,
                f"Status: {response.status_code}, Tasks: {response.json().get('count', 0)}")
    
    # Test 3: Get single task
    if task_id:
        print("  3. Testing get single task...")
        response = session.get(f'{BASE_URL}/api/tasks/{task_id}')
        print_result("Get Single Task", response.status_code == 200,
                    f"Status: {response.status_code}")
    
    # Test 4: Update task
    if task_id:
        print("  4. Testing update task...")
        update_data = {'status': 'in_progress', 'priority': 'medium'}
        response = session.put(
            f'{BASE_URL}/api/tasks/{task_id}',
            json=update_data
        )
        print_result("Update Task", response.status_code == 200,
                    f"Status: {response.status_code}")
    
    # Test 5: Get task stats
    print("  5. Testing task statistics...")
    response = session.get(f'{BASE_URL}/api/tasks/stats')
    print_result("Get Task Stats", response.status_code == 200,
                f"Status: {response.status_code}")
    
    if response.status_code == 200:
        stats = response.json().get('data', {})
        print(f"     Total: {stats.get('total_tasks', 0)} | "
              f"Completed: {stats.get('completed_tasks', 0)} | "
              f"Pending: {stats.get('pending_tasks', 0)}")
    
    # Test 6: Delete task
    if task_id:
        print("  6. Testing delete task...")
        response = session.delete(f'{BASE_URL}/api/tasks/{task_id}')
        print_result("Delete Task", response.status_code == 200,
                    f"Status: {response.status_code}")

def test_filters(session):
    """Test task filtering"""
    print("\n🔍 Testing Task Filters...")
    
    # Create multiple tasks with different statuses
    tasks = [
        {'title': 'High Priority Task', 'priority': 'high', 'status': 'pending'},
        {'title': 'Medium Priority Task', 'priority': 'medium', 'status': 'in_progress'},
        {'title': 'Low Priority Task', 'priority': 'low', 'status': 'completed'},
    ]
    
    for task in tasks:
        session.post(f'{BASE_URL}/api/tasks', json=task)
    
    # Test 1: Filter by status
    print("  1. Testing filter by status...")
    response = session.get(f'{BASE_URL}/api/tasks?status=pending')
    print_result("Filter by Status", response.status_code == 200,
                f"Found: {response.json().get('count', 0)} tasks")
    
    # Test 2: Filter by priority
    print("  2. Testing filter by priority...")
    response = session.get(f'{BASE_URL}/api/tasks?priority=high')
    print_result("Filter by Priority", response.status_code == 200,
                f"Found: {response.json().get('count', 0)} tasks")

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 Smart Task Manager - API Tests")
    print("=" * 60)
    
    try:
        # Test authentication
        session = test_authentication()
        
        # Test task API
        test_task_api(session)
        
        # Test filters
        test_filters(session)
        
        print("\n" + "=" * 60)
        print("✅ API Testing Complete!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        print("Make sure the application is running on http://localhost:5000")

if __name__ == '__main__':
    main()
