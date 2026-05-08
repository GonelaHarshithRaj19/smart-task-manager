# Deployment Guide

Production deployment instructions for Smart Task Manager.

## Environment Preparation

### 1. Production Environment Variables

Create `.env.production`:

```
SECRET_KEY=your-production-secret-key-here-must-be-long-random-string
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql+psycopg://prod_user:prod_password@prod.host.com:5432/smart_task_manager
SESSION_COOKIE_SECURE=True
FLASK_PORT=8000
```

### 2. Update Configuration

Edit `config.py`:

```python
# Production settings
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True
SQLALCHEMY_ECHO = False  # Disable query logging
```

### 3. Database Setup

```bash
# Backup development database
pg_dump smart_task_manager > backup.sql

# Create production database
CREATE DATABASE smart_task_manager_prod;

# Restore or initialize
psql smart_task_manager_prod < schema.sql
```

## Deployment Options

### Option 1: Heroku

```bash
# Install Heroku CLI
# Create Heroku app
heroku create smart-task-manager

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0

# Set environment variables
heroku config:set SECRET_KEY=your-secret
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Initialize database
heroku run python init_db.py --seed
```

### Option 2: AWS EC2

```bash
# 1. Launch Ubuntu EC2 instance
# 2. SSH into instance
ssh -i key.pem ubuntu@your-instance.com

# 3. Install dependencies
sudo apt-get update
sudo apt-get install python3-pip postgresql postgresql-contrib nginx

# 4. Clone repository
git clone https://github.com/yourusername/smart-task-manager.git
cd smart-task-manager

# 5. Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Configure PostgreSQL
sudo -u postgres createdb smart_task_manager

# 7. Setup .env file
nano .env

# 8. Initialize database
python init_db.py --seed

# 9. Install Gunicorn
pip install gunicorn

# 10. Start application
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 app:app
```

### Option 3: Docker

**Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "run_app.py"]
```

**docker-compose.yml**:

```yaml
version: '3'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: smart_task_manager
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: python run_app.py
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql+psycopg://postgres:postgres@db:5432/smart_task_manager
      FLASK_ENV: production
    depends_on:
      - db

volumes:
  postgres_data:
```

**Deploy with Docker**:

```bash
docker-compose up -d
docker-compose exec web python init_db.py --seed
```

## Nginx Configuration

**File**: `/etc/nginx/sites-available/default`

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable and restart:

```bash
sudo systemctl restart nginx
```

## SSL Certificate Setup

Using Let's Encrypt:

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## Security Checklist

- ✅ `SECRET_KEY` changed to random string
- ✅ `DEBUG = False`
- ✅ `SESSION_COOKIE_SECURE = True`
- ✅ HTTPS/SSL enabled
- ✅ Database password strong and unique
- ✅ Environment variables in `.env` (not in code)
- ✅ Firewall configured (only ports 80, 443)
- ✅ Regular database backups enabled
- ✅ Application logs monitored
- ✅ CORS settings configured appropriately

## Monitoring

### Application Logs

```bash
# With Gunicorn
gunicorn --error-logfile - --access-logfile - --loglevel debug app:app

# View logs
tail -f app.log
```

### Database Backups

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
pg_dump smart_task_manager > $BACKUP_DIR/backup_$DATE.sql
```

### Performance Monitoring

```bash
# Monitor system resources
watch -n 1 'free -h && echo "---" && df -h'

# Check PostgreSQL connections
psql -U postgres -c "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"
```

## Scaling Considerations

### Load Balancing

For multiple application servers:

```nginx
upstream app_servers {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://app_servers;
    }
}
```

### Caching

Add Redis for session caching:

```python
# config.py
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
SESSION_REDIS = redis.from_url(REDIS_URL)
```

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
CREATE INDEX idx_tasks_created_date ON tasks(created_date DESC);
CREATE INDEX idx_users_email ON users(email);
```

## Troubleshooting Production

### Application Won't Start

```bash
# Check logs
journalctl -u gunicorn -n 50

# Test Python
python -c "from app import create_app; print('OK')"

# Verify environment
env | grep FLASK
```

### Database Connection Issues

```bash
# Test connection
psql -U postgres -h your-host -d smart_task_manager

# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql.log
```

### High Memory Usage

```bash
# Restart application
sudo systemctl restart gunicorn

# Check resource usage
ps aux | grep gunicorn
```

## Rollback Procedure

```bash
# Keep previous version
git tag deployment-v1
git checkout deployment-v1

# Restart application
sudo systemctl restart gunicorn

# Restore database if needed
psql smart_task_manager < backup.sql
```

## Maintenance

### Regular Tasks

- ✅ Daily: Monitor logs and alerts
- ✅ Weekly: Check disk space and backups
- ✅ Monthly: Update dependencies, security patches
- ✅ Quarterly: Database optimization and cleanup

### Database Maintenance

```bash
# Vacuum and analyze
psql -U postgres -d smart_task_manager -c "VACUUM ANALYZE;"

# Check database size
psql -U postgres -c "SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;"
```

---

For questions or issues, refer to [README.md](README.md) or [POSTGRES_SETUP.md](POSTGRES_SETUP.md).
