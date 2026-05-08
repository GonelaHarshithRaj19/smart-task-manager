# PostgreSQL Setup Guide for Smart Task Manager

This guide provides step-by-step instructions to set up PostgreSQL for the Smart Task Manager application.

## 🪟 Windows Setup

### Step 1: Download PostgreSQL

1. Visit [PostgreSQL Official Website](https://www.postgresql.org/download/windows/)
2. Download PostgreSQL 12 or higher
3. Run the installer and follow the setup wizard

### Step 2: Installation

During installation:
- Choose installation directory (default: `C:\Program Files\PostgreSQL`)
- Set password for `postgres` user (remember this!)
- Port: Keep default `5432`
- Locale: Select your locale

### Step 3: Verify Installation

Open PowerShell and verify PostgreSQL is installed:

```powershell
psql --version
```

### Step 4: Create Database

1. **Open pgAdmin** (installed with PostgreSQL) or use command line
2. **Connect to PostgreSQL**:

```powershell
psql -U postgres
```

Enter the password you set during installation.

3. **Create Database**:

```sql
CREATE DATABASE smart_task_manager;
```

4. **Verify Creation**:

```sql
\l
```

You should see `smart_task_manager` in the list.

5. **Exit PostgreSQL**:

```sql
\q
```

### Step 5: Configure Application

1. **Edit `.env` file** in your project root:

```powershell
# Navigate to project
cd c:\Users\user\OneDrive\Desktop\smart-task-manager

# Edit .env (use your editor)
# Update DATABASE_URL to:
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/smart_task_manager
```

Replace `YOUR_PASSWORD` with the password you set for the `postgres` user.

### Step 6: Initialize Database Tables

Run the initialization script:

```powershell
python init_db.py --seed
```

This creates all tables and adds sample data.

### Step 7: Test Connection

Run the API test script:

```powershell
python test_api.py
```

## 🐧 Linux/macOS Setup

### Using Homebrew (macOS)

```bash
# Install PostgreSQL
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create database
createdb smart_task_manager

# Edit .env
nano .env
# DATABASE_URL=postgresql+psycopg://your_user:password@localhost:5432/smart_task_manager

# Initialize database
python init_db.py --seed
```

### Using apt (Linux/Ubuntu)

```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql

# Create database
sudo -u postgres createdb smart_task_manager

# Configure .env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/smart_task_manager

# Initialize
python init_db.py --seed
```

## 🔧 Troubleshooting

### Connection Error: "could not connect to server"

**Problem**: Cannot connect to PostgreSQL

**Solution**:
1. Verify PostgreSQL is running:
   ```powershell
   # Windows
   Get-Service | Where-Object {$_.Name -like "*postgres*"}
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Check DATABASE_URL format in `.env`:
   ```
   postgresql+psycopg://username:password@host:port/database
   ```

3. Verify credentials:
   ```powershell
   psql -U postgres -d smart_task_manager
   ```

### "database does not exist"

Create the database:
```sql
psql -U postgres
CREATE DATABASE smart_task_manager;
\q
```

### "FATAL: password authentication failed"

Reset PostgreSQL password:

**Windows**:
```powershell
# Stop PostgreSQL
net stop postgresql-x64-XX

# Start in safe mode and reset password
# (Requires elevated permissions)
```

**Linux**:
```bash
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'new_password';
\q
```

### Port 5432 Already in Use

Check what's using the port:

**Windows**:
```powershell
netstat -ano | findstr :5432
```

**Linux**:
```bash
sudo lsof -i :5432
```

Either stop the conflicting service or use a different port in `.env`:
```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5433/smart_task_manager
```

## 📊 PostgreSQL Management Tools

### pgAdmin (Web-based GUI)

Included with PostgreSQL installer. Access at `http://localhost:5050`

- Create databases
- Manage users
- Run queries
- View table structure

### DBeaver (Advanced)

Download from [dbeaver.io](https://dbeaver.io/)

Free desktop SQL client with excellent PostgreSQL support.

### Command Line Tools

```powershell
# Connect to database
psql -U postgres -d smart_task_manager

# Run SQL script
psql -U postgres -d smart_task_manager -f database\schema.sql

# Export database
pg_dump -U postgres smart_task_manager > backup.sql

# Restore database
psql -U postgres -d smart_task_manager < backup.sql
```

## ✅ Verification Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `smart_task_manager` created
- [ ] `.env` file configured with correct credentials
- [ ] Virtual environment activated
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] Database initialized (`python init_db.py --seed`)
- [ ] Sample data added and verified
- [ ] Application starts successfully (`python run_app.py`)
- [ ] Can access http://localhost:5000
- [ ] Can register and login with test user

## 🚀 Next Steps

1. Start the application: `python run_app.py`
2. Open browser: `http://localhost:5000`
3. Register or login with test credentials
4. Create tasks and verify functionality
5. Check analytics dashboard
6. Monitor WebSocket real-time updates

## 📞 Support

For PostgreSQL issues:
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Download Page](https://www.postgresql.org/download/)
- [Stack Overflow PostgreSQL Tag](https://stackoverflow.com/questions/tagged/postgresql)
