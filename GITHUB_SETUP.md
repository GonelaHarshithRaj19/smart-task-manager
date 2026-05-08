# GitHub Repository Setup Guide

Instructions to push Smart Task Manager to GitHub and prepare for submission.

## Prerequisites

- GitHub account (create at github.com if needed)
- Git installed (https://git-scm.com/)
- Project folder ready for submission

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. Go to [github.com/new](https://github.com/new)
2. **Repository Name**: `smart-task-manager`
3. **Description**: Smart Task Management System - Python Flask application with PostgreSQL, WebSockets, and real-time analytics
4. **Visibility**: Public (for submission)
5. **Initialize with**: DO NOT check any options (we'll push existing code)
6. Click **Create Repository**

### Option B: Using GitHub CLI

```bash
gh repo create smart-task-manager --public --source=. --remote=origin --push
```

## Step 2: Initialize Git in Project

```bash
cd c:\Users\user\OneDrive\Desktop\smart-task-manager

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Smart Task Manager application"

# Check git status
git status
```

## Step 3: Connect to GitHub

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/smart-task-manager.git

# Verify remote
git remote -v

# Show remote information
git remote show origin
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 4: Push to GitHub

```bash
# Rename branch to main (if needed)
git branch -M main

# Push code to GitHub
git push -u origin main

# Verify push was successful
git log --oneline -5
```

## Step 5: Verify Repository

1. Go to `https://github.com/YOUR_USERNAME/smart-task-manager`
2. Verify all files are present:
   - ✅ app/ folder with all routes and templates
   - ✅ database/ folder with schema.sql
   - ✅ requirements.txt
   - ✅ README.md
   - ✅ QUICKSTART.md
   - ✅ POSTGRES_SETUP.md
   - ✅ ARCHITECTURE.md
   - ✅ DEPLOYMENT.md
   - ✅ .gitignore
   - ✅ All configuration files

## Step 6: Add Repository Topics

1. Go to repository settings
2. Click "Add topics"
3. Add relevant topics:
   - `python`
   - `flask`
   - `postgresql`
   - `websockets`
   - `rest-api`
   - `task-manager`
   - `web-application`

## Step 7: Create README Badge (Optional)

Add to top of README.md:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/smart-task-manager.svg?style=flat-square)](https://github.com/YOUR_USERNAME/smart-task-manager/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
```

## Step 8: Regular Updates

### After Making Changes

```bash
# Check changes
git status

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin main
```

### Create Release Tags

```bash
# Create tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"

# Push tags
git push origin --tags
```

## Step 9: Submission Information

Format for submission:

```
GitHub Repository Link: https://github.com/YOUR_USERNAME/smart-task-manager

Key Files:
- README.md - Complete setup and usage documentation
- database/schema.sql - PostgreSQL database schema
- requirements.txt - All Python dependencies
- SUBMISSION.md - Complete requirement checklist

Documentation:
- QUICKSTART.md - 5-minute setup guide
- POSTGRES_SETUP.md - PostgreSQL configuration guide
- ARCHITECTURE.md - Code structure and design
- DEPLOYMENT.md - Production deployment guide

Setup:
1. Clone: git clone https://github.com/YOUR_USERNAME/smart-task-manager.git
2. Follow: QUICKSTART.md
3. Run: python run_app.py
4. Access: http://localhost:5000
```

## Troubleshooting

### "fatal: not a git repository"

```bash
cd smart-task-manager
git init
```

### "failed to push some refs"

```bash
# Pull latest changes first
git pull origin main

# Then push
git push origin main
```

### "error: failed to push to repository"

Verify remote:
```bash
git remote -v

# If wrong, update
git remote set-url origin https://github.com/YOUR_USERNAME/smart-task-manager.git
```

### "Permission denied" (SSH issues)

Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/smart-task-manager.git
```

Or setup SSH keys:
```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096

# Add to GitHub: Settings > SSH and GPG keys > New SSH key
# Paste content of ~/.ssh/id_rsa.pub
```

## GitHub Best Practices

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add user authentication with bcrypt"
git commit -m "Implement WebSocket real-time updates"
git commit -m "Fix database connection timeout"

# Avoid
git commit -m "fix"
git commit -m "updates"
```

### .gitignore Verification

Ensure sensitive files are NOT committed:

```bash
# Check what will be committed
git status

# Verify .env is ignored
git check-ignore -v .env
```

### Branching (for development)

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to GitHub
git push origin feature/new-feature

# Create Pull Request on GitHub
# Merge after review
```

## Final Submission

### README Last Checks

- ✅ Setup instructions clear and complete
- ✅ Dependencies listed
- ✅ API documentation included
- ✅ Examples provided
- ✅ Troubleshooting section included
- ✅ License information
- ✅ Authors/contacts

### Folder Structure in Repository

```
smart-task-manager/
├── app/
├── database/
├── utils/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── POSTGRES_SETUP.md
├── DEPLOYMENT.md
├── ARCHITECTURE.md
├── SUBMISSION.md
└── ...
```

### Repository URL Format

Your submission should use:
```
https://github.com/YOUR_USERNAME/smart-task-manager
```

## Next Steps

1. Create GitHub account if needed
2. Create new repository (name: smart-task-manager)
3. Push code: `git push -u origin main`
4. Verify all files are present on GitHub
5. Update submission documentation with GitHub link
6. Test repository by cloning in another directory:

```bash
git clone https://github.com/YOUR_USERNAME/smart-task-manager.git
cd smart-task-manager
pip install -r requirements.txt
python init_db.py --seed
python run_app.py
```

---

For questions, refer to [GitHub Help](https://help.github.com/) or [Git Documentation](https://git-scm.com/doc).

**Ready to submit! ✅**
