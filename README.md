# 📋 Smart Task Management System

A complete web-based task management system built with Flask, PostgreSQL, and modern web technologies. Features real-time updates via WebSockets, advanced analytics using Pandas and NumPy, and a responsive user interface.

## ✨ Features

- **User Authentication**
  - User registration with validation
  - Secure login with bcrypt password hashing
  - Session management
  - Logout functionality

- **Task Management**
  - Create, read, update, delete tasks (CRUD operations)
  - Task prioritization (High, Medium, Low)
  - Task status tracking (Pending, In Progress, Completed)
  - Due date management
  - Task descriptions

- **Real-time Updates**
  - WebSocket integration via Flask-SocketIO
  - Real-time notifications for task changes
  - Live dashboard updates
  - Instant task creation/update/deletion events

- **Analytics Dashboard**
  - Total tasks count
  - Completed tasks count
  - Pending tasks count
  - In-progress tasks count
  - Completion percentage
  - Priority distribution
  - Average completion time
  - Built with Pandas and NumPy

- **Responsive Design**
  - Mobile-friendly interface
  - Tablet and desktop optimization
  - Modern UI with smooth animations
  - Real-time notification system

- **REST API**
  - JSON-based API endpoints
  - Task CRUD operations
  - Statistics endpoint
  - Proper error handling

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-SocketIO
- **Database**: PostgreSQL
- **Data Analysis**: Pandas, NumPy
- **Security**: bcrypt for password hashing
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **WebSocket**: python-socketio, python-engineio

## 📁 Project Structure

```
smart-task-manager/
├── app/
│   ├── models/
│   │   └── __init__.py           # Database models (User, Task)
│   ├── routes/
│   │   ├── __init__.py           # Route blueprints
│   │   ├── auth.py               # Authentication routes
│   │   └── task.py               # Task API routes
│   ├── templates/
│   │   ├── register.html         # Registration page
│   │   ├── login.html            # Login page
│   │   └── dashboard.html        # Main dashboard
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css         # Main stylesheet
│   │   └── js/
│   │       └── main.js           # Frontend JavaScript
│   └── __init__.py
├── database/
├── utils/
├── app.py                        # Flask application factory
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone or Download Project

```bash
cd smart-task-manager
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database

For detailed PostgreSQL setup instructions, see [POSTGRES_SETUP.md](POSTGRES_SETUP.md)

**Quick Setup** (Windows):

1. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
2. Create database:
```sql
psql -U postgres
CREATE DATABASE smart_task_manager;
\q
```

3. Configure `.env` file:
```
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/smart_task_manager
```

4. Replace `YOUR_PASSWORD` with your PostgreSQL password

### Step 5: Initialize Database

Use the initialization script to create tables and add sample data:

```bash
# Create tables
python init_db.py

# Create tables + add sample data
python init_db.py --seed
```

**Login with test credentials** (if seed data was added):
- Username: `testuser`
- Password: `password123`

### Step 6: Run the Application

```bash
python run_app.py
```

The application will start at `http://localhost:5000`

**Available Commands**:
- `python run_app.py` - Start the application
- `python test_api.py` - Run API tests (app must be running)
- `python init_db.py --seed` - Add sample data

## 📖 Usage Guide

### 1. **Register a New Account**

- Navigate to the registration page
- Enter username (minimum 3 characters)
- Enter valid email address
- Enter password (minimum 6 characters)
- Confirm password
- Click "Create Account"

### 2. **Login**

- Enter your username and password
- Click "Sign In"
- You'll be redirected to the dashboard

### 3. **Create Tasks**

- Fill in the task title (required)
- Add optional description
- Select priority (High, Medium, Low)
- Set due date (optional)
- Click "Create Task"
- Notification will confirm task creation
- Task appears immediately in the table

### 4. **Manage Tasks**

**View Tasks**:
- All your tasks appear in the table
- Filter by status or priority using the filter options
- Click "Refresh" to reload tasks

**Edit Tasks**:
- Click "Edit" button on any task row
- Modify task details in the modal
- Change priority and status
- Click "Update Task"

**Delete Tasks**:
- Click "Delete" button on any task row
- Confirm deletion
- Task is removed immediately

### 5. **Monitor Analytics**

- Dashboard displays real-time analytics cards
- Total Tasks: Count of all your tasks
- Completed: Number of finished tasks
- Pending: Tasks not started
- In Progress: Tasks being worked on
- Completion Rate: Percentage of completed tasks
- High Priority: Count of high-priority tasks

### 6. **Real-time Notifications**

- Notifications appear in the top-right corner
- Automatic dismissal after 5 seconds
- Success/error/info messages for all actions

## 🔌 REST API Endpoints

### Authentication Routes

```
POST   /auth/register       - User registration
POST   /auth/login          - User login
GET    /auth/logout         - User logout
GET    /auth/profile        - View user profile
```

### Task API Routes

```
GET    /api/tasks           - Get all tasks (with optional filters)
GET    /api/tasks/<id>      - Get single task
POST   /api/tasks           - Create new task
PUT    /api/tasks/<id>      - Update task
DELETE /api/tasks/<id>      - Delete task
GET    /api/tasks/stats     - Get task statistics
```

### Query Parameters (GET /api/tasks)

- `status`: Filter by status (pending, in_progress, completed)
- `priority`: Filter by priority (low, medium, high)
- `sort_by`: Sort by field (created_date, due_date, priority)

### Example API Requests

**Get All Tasks**:
```bash
curl -X GET http://localhost:5000/api/tasks \
  -H "Content-Type: application/json"
```

**Create Task**:
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "due_date": "2026-05-15"
  }'
```

**Update Task**:
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "priority": "medium"
  }'
```

**Get Analytics**:
```bash
curl -X GET http://localhost:5000/api/tasks/stats \
  -H "Content-Type: application/json"
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Secret key for sessions
SECRET_KEY = 'your-secret-key-here'

# Database connection
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/db_name'

# Session settings
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# WebSocket settings
SOCKETIO_ASYNC_MODE = 'threading'
```

## 🔐 Security Features

- **Password Hashing**: Bcrypt with 12 rounds for secure password storage
- **Session Management**: Secure Flask session handling
- **Login Protection**: Routes require authentication
- **Input Validation**: Form validation on both client and server
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **CSRF Protection**: Flask session-based protection

## 📊 Analytics Engine

The analytics module uses Pandas and NumPy to calculate:

- **Task Statistics**: Count tasks by status
- **Completion Rate**: Percentage of completed tasks
- **Priority Distribution**: Tasks by priority level
- **Average Completion Time**: Using datetime calculations
- **Trend Analysis**: Historical task data

## 🌐 WebSocket Events

**Server-side Events**:
- `task_created`: Emitted when a new task is created
- `task_updated`: Emitted when a task is updated
- `task_deleted`: Emitted when a task is deleted

**Client-side Events**:
- `connect`: Triggered when client connects
- `disconnect`: Triggered when client disconnects

## 🐛 Troubleshooting

### Database Connection Error

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
1. Ensure PostgreSQL is running
2. Check database credentials in `config.py`
3. Verify database exists: `CREATE DATABASE smart_task_manager;`

### Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**:
Modify the port in `app.py`:
```python
socketio.run(app, host='0.0.0.0', port=5001, debug=True)
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### WebSocket Connection Failed

**Problem**: WebSocket connection errors in browser console

**Solution**:
1. Ensure Flask-SocketIO is installed
2. Check browser console for errors
3. Verify CORS settings in `config.py`

## 📝 Environment Variables

Create a `.env` file for sensitive configuration:

```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/smart_task_manager
FLASK_ENV=development
```

Load in `config.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🚢 Deployment

### For Production

1. **Set Environment**:
```python
FLASK_ENV=production
DEBUG=False
SESSION_COOKIE_SECURE=True
```

2. **Use Production Server** (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn --worker-class eventlet -w 1 app:app
```

3. **Configure HTTPS** using reverse proxy (Nginx, Apache)

4. **Database**: Use hosted PostgreSQL service (AWS RDS, Heroku, etc.)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)

## 📄 License

This project is provided as-is for educational and development purposes.

## 👥 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Flask documentation
3. Check browser console for JavaScript errors
4. Review server logs for Python errors

## ✅ Checklist for First-time Setup

- [ ] Clone/download project
- [ ] Create virtual environment
- [ ] Install requirements.txt
- [ ] Create PostgreSQL database
- [ ] Update config.py with database credentials
- [ ] Run application
- [ ] Register new account
- [ ] Create test tasks
- [ ] Verify real-time updates
- [ ] Check analytics display

## 🎉 You're All Set!

Start managing your tasks efficiently with the Smart Task Management System!

Happy tasking! 📋✨
