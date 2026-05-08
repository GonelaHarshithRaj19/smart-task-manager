# Quick Start Guide

Get Smart Task Manager running in 5 minutes!

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ (or SQLite for local development)
- pip (Python package manager)

## Installation

### 1️⃣ Setup Environment

```bash
# Navigate to project
cd smart-task-manager

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure Database

**Option A: PostgreSQL (Recommended)**

See [POSTGRES_SETUP.md](POSTGRES_SETUP.md) for detailed setup

```bash
# Edit .env file
nano .env

# Update:
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/smart_task_manager
```

**Option B: SQLite (Local Development)**

Edit `.env`:
```
DATABASE_URL=sqlite:///smart_task_manager.db
```

### 3️⃣ Initialize Database

```bash
# Create tables
python init_db.py

# Add sample data (optional)
python init_db.py --seed
```

### 4️⃣ Start Application

```bash
python run_app.py
```

Open browser: **http://localhost:5000**

### 5️⃣ Test Login

**Default test credentials** (if seed data added):
- Username: `testuser`
- Password: `password123`

## Verification Checklist

- ✅ Virtual environment activated
- ✅ Dependencies installed
- ✅ `.env` file configured
- ✅ Database initialized
- ✅ Application running
- ✅ Can access http://localhost:5000
- ✅ Can login with test credentials

## Common Issues

**"ModuleNotFoundError: No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**"could not connect to server" (PostgreSQL)**
See [POSTGRES_SETUP.md](POSTGRES_SETUP.md) troubleshooting section

**"Address already in use"**
App running on port 5000. Check with:
```bash
netstat -ano | findstr :5000
```

## Next Steps

1. Explore the dashboard at http://localhost:5000
2. Create some tasks
3. Check analytics
4. Test real-time updates
5. Read full documentation in [README.md](README.md)

## Features to Try

- 📋 **Create Tasks** - Add tasks with priority, due dates, descriptions
- 📊 **View Analytics** - See task completion statistics
- 🔔 **Real-time Updates** - WebSocket live notifications
- 📱 **Responsive UI** - Works on desktop, tablet, mobile

## API Testing

```bash
# Terminal 1: Start app
python run_app.py

# Terminal 2: Run tests
python test_api.py
```

## Support

- Full documentation: [README.md](README.md)
- PostgreSQL guide: [POSTGRES_SETUP.md](POSTGRES_SETUP.md)
- Code structure: See `/app` directory

---

**Enjoy managing your tasks! 📋✨**
