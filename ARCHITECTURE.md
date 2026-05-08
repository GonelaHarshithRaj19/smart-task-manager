# Architecture & Code Structure

Comprehensive documentation of Smart Task Manager architecture and code organization.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser (Client)                 │
│                    (HTML/CSS/JavaScript)                │
└──────────────┬──────────────────────────────────────────┘
               │
        ┌──────┴─────────┐
        │                │
    HTTP/REST         WebSocket
        │                │
┌───────▼────────────────▼──────────────────────────────┐
│              Flask Web Application                     │
│  (Routes, Request Handling, Business Logic)           │
└──────────────┬────────────────────────────────────────┘
               │
        ┌──────▼──────┐
        │              │
    SQLAlchemy    SocketIO
        │              │
        │         WebSocket Server
        │              │
┌───────▼──────────────────────────────────────────────┐
│            PostgreSQL Database                        │
│        (Users, Tasks, Relationships)                  │
└──────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
smart-task-manager/
├── app/                          # Main application package
│   ├── __init__.py              # App initialization (empty)
│   ├── models/
│   │   └── __init__.py          # SQLAlchemy models (User, Task)
│   ├── routes/
│   │   ├── __init__.py          # Blueprint registration
│   │   ├── auth.py              # Authentication routes (register, login, logout)
│   │   └── task.py              # Task API routes (CRUD, stats)
│   ├── templates/
│   │   ├── base.html            # Base template (if needed)
│   │   ├── register.html        # User registration page
│   │   ├── login.html           # User login page
│   │   ├── dashboard.html       # Main dashboard
│   │   └── profile.html         # User profile page
│   └── static/
│       ├── css/
│       │   └── style.css        # Main stylesheet
│       └── js/
│           └── main.js          # Frontend JavaScript
│
├── database/
│   ├── __init__.py              # Database package
│   └── schema.sql               # PostgreSQL schema dump
│
├── utils/
│   └── __init__.py              # Utility functions
│
├── app.py                       # Flask app factory & configuration
├── config.py                    # Configuration settings
├── init_db.py                   # Database initialization script
├── run_app.py                   # Application entry point
├── test_api.py                  # API testing script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (DO NOT COMMIT)
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── POSTGRES_SETUP.md            # PostgreSQL setup guide
├── DEPLOYMENT.md                # Production deployment guide
├── ARCHITECTURE.md              # This file
└── CONTRIBUTING.md              # Contribution guidelines
```

## 🔄 Data Flow

### Authentication Flow

```
User Registration
├─ User submits registration form
├─ Server validates input (username, email, password)
├─ Server hashes password with bcrypt
├─ User record created in database
└─ Redirect to login page

User Login
├─ User submits credentials
├─ Server retrieves user by username
├─ Server verifies password hash
├─ Session created and user_id stored
├─ User redirected to dashboard
└─ SocketIO client connects with session
```

### Task Management Flow

```
Create Task
├─ Frontend sends POST request to /api/tasks
├─ Server validates user is logged in
├─ Server validates task data (title required)
├─ Task record created in database
├─ WebSocket emits 'task_created' event
└─ Frontend receives event and updates UI

Get Tasks
├─ Frontend sends GET request to /api/tasks
├─ Server retrieves tasks for current user
├─ Server applies filters/sorting if requested
└─ Frontend receives JSON array and renders table

Update Task
├─ Frontend sends PUT request to /api/tasks/<id>
├─ Server validates ownership (user_id match)
├─ Server updates specified fields
├─ WebSocket emits 'task_updated' event
└─ Frontend updates task in UI

Delete Task
├─ Frontend sends DELETE request to /api/tasks/<id>
├─ Server validates ownership
├─ Server deletes task record
├─ WebSocket emits 'task_deleted' event
└─ Frontend removes task from UI
```

### Analytics Flow

```
Get Statistics
├─ Frontend sends GET request to /api/tasks/stats
├─ Server retrieves all tasks for user
├─ Pandas converts tasks to DataFrame
├─ NumPy/Pandas calculates statistics
│  ├─ Total tasks count
│  ├─ Status distribution
│  ├─ Priority distribution
│  ├─ Completion percentage
│  └─ Time-based analytics
├─ Results formatted as JSON
└─ Frontend renders analytics cards
```

## 📊 Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                    -- Unique user ID
    username VARCHAR(80) UNIQUE NOT NULL,     -- Login username
    email VARCHAR(120) UNIQUE NOT NULL,       -- User email
    password VARCHAR(255) NOT NULL,           -- Hashed password (bcrypt)
    created_date TIMESTAMP DEFAULT NOW()      -- Account creation date
);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,                    -- Unique task ID
    user_id INTEGER FOREIGN KEY,              -- Link to user
    title VARCHAR(255) NOT NULL,              -- Task title
    description TEXT,                         -- Task description
    priority VARCHAR(20),                     -- high, medium, low
    status VARCHAR(20),                       -- pending, in_progress, completed
    created_date TIMESTAMP DEFAULT NOW(),     -- Task creation date
    updated_date TIMESTAMP DEFAULT NOW(),     -- Last update date
    due_date TIMESTAMP                        -- Optional due date
);
```

**Indexes**:
- `users.username` - Fast login lookups
- `users.email` - Email uniqueness check
- `tasks.user_id` - Retrieve user's tasks
- `tasks.status` - Filter by status
- `tasks.created_date` - Sort by date

## 🔐 Security Architecture

### Password Security

```
User Input (plaintext)
        ↓
Bcrypt Hash (12 rounds)
        ↓
Hashed String (stored in DB)
        ↓
User Login → Input compared with hash
```

### Session Security

```
Login Success
        ↓
Session created (Flask-Session)
        ↓
user_id stored in session
        ↓
Session ID in cookie (HTTPONLY, SECURE flags)
        ↓
@login_required decorator validates session
```

### API Protection

```
Request to /api/tasks
        ↓
@api_login_required decorator
        ↓
Check if 'user_id' in session
        ↓
If yes → Proceed with request
If no → Return 401 Unauthorized
```

## 🔌 WebSocket Events

### Server Emits

```python
# When task is created
emit('task_created', {
    'id': task.id,
    'title': task.title,
    'status': task.status
}, room=f'user_{user_id}')

# When task is updated
emit('task_updated', task.to_dict(), room=f'user_{user_id}')

# When task is deleted
emit('task_deleted', {'id': task_id}, room=f'user_{user_id}')
```

### Client Handles

```javascript
socket.on('task_created', (data) => {
    // Add task to table
    allTasks.push(data);
    renderTasks(allTasks);
    showNotification('Task created!');
});

socket.on('task_updated', (data) => {
    // Update task in table
    // Refresh analytics
});

socket.on('task_deleted', (data) => {
    // Remove task from table
    // Refresh analytics
});
```

## 📈 Performance Considerations

### Database Optimization

1. **Indexes**: Primary keys, foreign keys, and filter columns
2. **Query Optimization**: Use SQLAlchemy efficiently
3. **Connection Pooling**: Flask-SQLAlchemy handles connections
4. **Caching**: Could add Redis for session caching

### Frontend Optimization

1. **Lazy Loading**: Load tasks as needed
2. **Client-side Filtering**: Filter before rendering
3. **Debouncing**: Throttle WebSocket events
4. **Compression**: gzip CSS/JS in production

## 🧪 Testing Architecture

### Unit Tests

```
Test Models → Test validators and methods
Test Routes → Test endpoints and status codes
Test Utils → Test helper functions
```

### Integration Tests

```
Test API Workflow
├─ Register user
├─ Login user
├─ Create task
├─ Update task
├─ Get stats
└─ Delete task
```

## 📚 Key Technologies

### Backend

- **Flask**: Web framework for routing and HTTP handling
- **SQLAlchemy**: ORM for database operations
- **Flask-SocketIO**: WebSocket implementation
- **Bcrypt**: Password hashing

### Frontend

- **HTML5**: Structure
- **CSS3**: Styling with flexbox/grid
- **JavaScript (Vanilla)**: DOM manipulation, API calls
- **Socket.IO Client**: Real-time communication

### Data Processing

- **Pandas**: DataFrames for data analysis
- **NumPy**: Numerical computations

### Database

- **PostgreSQL**: Primary relational database
- **SQLite**: Alternative for development

## 🔄 Request/Response Cycle

```
User Action (click, form submit)
        ↓
JavaScript event handler triggered
        ↓
FETCH API call to /api/endpoint
        ↓
Flask route receives request
        ↓
Validate user is authenticated
        ↓
Validate request data
        ↓
Perform database operation
        ↓
Emit WebSocket event (optional)
        ↓
Return JSON response
        ↓
Frontend receives response
        ↓
Update DOM if successful
        ↓
Show notification to user
```

## 🚀 Scalability

### Current Limitations

- Single PostgreSQL instance
- Single Flask app server
- In-memory session storage

### Scaling Strategies

1. **Database**: Replication, connection pooling
2. **Backend**: Load balancing, multiple app servers
3. **Caching**: Redis for sessions and frequently accessed data
4. **CDN**: Static files delivery
5. **Message Queue**: Celery for async tasks

---

For more information, see [README.md](README.md), [DEPLOYMENT.md](DEPLOYMENT.md), or source code comments.
