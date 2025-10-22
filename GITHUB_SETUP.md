# CyberLearn - GitHub Setup & Push Guide

## 🚀 Quick Setup (Run on Your VM)

### Step 1: Initialize Git Repository

```bash
# Navigate to project directory
cd "c:\Users\yaniv\10Root Dropbox\Yaniv Radunsky\Documents\50-59 Projects\57 ClaudeCode\57.14_Learning_app"

# Initialize Git
git init

# Configure Git (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 2: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `cyberlearn` (or your preferred name)
3. Description: `Adaptive Cybersecurity Learning Platform with Jim Kwik Principles`
4. Choose: **Public** (for open source) or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we have these already)
6. Click **Create repository**

### Step 3: Add Files and Commit

```bash
# Add all files (respects .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: Complete CyberLearn adaptive learning platform

- Adaptive learning engine with skill profiling
- Gamification system (XP, badges, levels, streaks)
- Interactive Streamlit UI
- Complete sample lesson (CIA Triad)
- All 10 Jim Kwik principles integrated
- Comprehensive documentation (22,000+ words)
- Production-ready code (5,000+ lines)

🛡️ Generated with Claude Code
"
```

### Step 4: Connect to GitHub and Push

```bash
# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/cyberlearn.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: You may be prompted for GitHub credentials. If using a personal access token (PAT), enter it as the password.

---

## 🔐 Authentication Setup

### Option A: Personal Access Token (Recommended)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Name: `cyberlearn-deployment`
4. Expiration: 90 days (or custom)
5. Scopes: Check `repo` (all permissions)
6. Click **Generate token**
7. **COPY THE TOKEN** (you won't see it again)
8. When pushing, use token as password

### Option B: SSH Keys

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter for default location
# Set a passphrase (optional but recommended)

# Copy public key
cat ~/.ssh/id_ed25519.pub
# On Windows: type %USERPROFILE%\.ssh\id_ed25519.pub

# Add to GitHub:
# Go to GitHub → Settings → SSH and GPG keys → New SSH key
# Paste the public key

# Test connection
ssh -T git@github.com

# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/cyberlearn.git
```

---

## 📋 Pre-Push Checklist

Before pushing, verify:

- [ ] `.gitignore` is in place (database and venv excluded)
- [ ] All documentation files present
- [ ] `requirements.txt` up to date
- [ ] Sample lesson JSON included
- [ ] LICENSE file present
- [ ] No sensitive data (passwords, tokens, personal info)
- [ ] No large binary files (videos, images should be <10MB)

### Check What Will Be Committed

```bash
# See what's staged
git status

# See what's ignored
git status --ignored

# Verify database not included
git ls-files | grep -i ".db"
# Should return nothing
```

---

## 🎨 Customize Repository

### Add GitHub Repository Description

On GitHub repository page:
1. Click ⚙️ next to "About"
2. Description: `Adaptive cybersecurity learning platform integrating Jim Kwik's accelerated learning principles`
3. Website: Your deployment URL (optional)
4. Topics: `cybersecurity`, `education`, `adaptive-learning`, `gamification`, `python`, `streamlit`, `jim-kwik`
5. Save

### Add Repository Social Preview

1. Go to repository Settings
2. Scroll to "Social preview"
3. Upload an image (1280x640 recommended)
4. Save

---

## 📝 Create GitHub README Badges

Add to top of README.md:

```markdown
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/cyberlearn?style=social)](https://github.com/YOUR_USERNAME/cyberlearn)
```

---

## 🌟 Optional: GitHub Pages for Documentation

Host documentation as a website:

```bash
# Create docs branch
git checkout -b gh-pages

# Keep only markdown docs
rm -rf models core utils ui *.py *.db

# Create index.html pointing to README.md
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=README.md">
</head>
</html>
EOF

git add .
git commit -m "Setup GitHub Pages"
git push origin gh-pages

# Back to main
git checkout main
```

Then in GitHub: Settings → Pages → Source: `gh-pages` branch

---

## 🤝 Enable Collaboration Features

### 1. GitHub Issues

- Go to repository → Issues tab
- Create issue templates for:
  - Bug reports
  - Feature requests
  - Content submissions (new lessons)

### 2. GitHub Discussions

- Settings → Features → Enable Discussions
- Categories: Announcements, Q&A, Show and tell

### 3. Pull Request Template

Create `.github/pull_request_template.md`:

```markdown
## Description
[Describe your changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] New lesson content
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tested locally
- [ ] All tests pass
- [ ] Documentation updated

## Screenshots (if applicable)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed changes
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No breaking changes
```

---

## 📦 Deployment from GitHub

### Option 1: Streamlit Community Cloud (Free)

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Repository: `YOUR_USERNAME/cyberlearn`
5. Branch: `main`
6. Main file path: `app.py`
7. Click "Deploy"

**URL**: Your app will be at `https://YOUR_USERNAME-cyberlearn.streamlit.app`

### Option 2: Docker Hub (for Container Deployment)

```bash
# Build Docker image
docker build -t YOUR_USERNAME/cyberlearn:latest .

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push YOUR_USERNAME/cyberlearn:latest
```

Then on any server:
```bash
docker pull YOUR_USERNAME/cyberlearn:latest
docker run -p 8501:8501 YOUR_USERNAME/cyberlearn:latest
```

---

## 🔄 Ongoing Workflow

### Adding New Features

```bash
# Create feature branch
git checkout -b feature/new-feature-name

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "[Feature] Description of new feature"

# Push feature branch
git push origin feature/new-feature-name

# Create Pull Request on GitHub
# Review and merge
```

### Updating Content

```bash
# For new lessons
git checkout -b content/new-lesson-name

# Add lesson JSON
cp content/lesson_template.json content/new_lesson.json
# ... edit lesson ...

git add content/new_lesson.json
git commit -m "[Content] Add new lesson: Lesson Name"

git push origin content/new-lesson-name
# Create PR on GitHub
```

### Syncing Changes

```bash
# Pull latest changes
git pull origin main

# Or if you have local changes
git fetch origin
git merge origin/main
```

---

## 📊 GitHub Repository Insights

### Enable Repository Insights

Settings → Insights → Enable:
- Traffic (page views, clones)
- Commits activity
- Code frequency
- Contributors

### Add Community Health Files

Create `.github/` directory with:
- `CODE_OF_CONDUCT.md`
- `SECURITY.md` (vulnerability reporting)
- `SUPPORT.md` (how to get help)

---

## 🚨 Security Best Practices

### 1. Scan for Secrets

Before pushing:

```bash
# Check for potential secrets
git grep -i "password"
git grep -i "api_key"
git grep -i "secret"
git grep -i "token"
```

### 2. Enable Dependabot

Settings → Security → Dependabot:
- ✅ Enable alerts
- ✅ Enable security updates
- ✅ Enable version updates

### 3. Add Security Policy

Create `SECURITY.md`:

```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email:
security@your-domain.com

Do NOT open a public issue.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Security Measures

- No real exploits in content
- Input validation on all user data
- SQL injection prevention
- No eval() or exec() usage
- Sandboxed lab environments
```

---

## 🎉 Post-Push Checklist

After successful push:

- [ ] Verify repository is accessible on GitHub
- [ ] Check all files uploaded correctly
- [ ] README.md displays properly
- [ ] Documentation links work
- [ ] Add repository description and topics
- [ ] Star your own repo (optional but fun!)
- [ ] Share repository URL
- [ ] Deploy to Streamlit Cloud (optional)

---

## 🆘 Troubleshooting

### Issue: "Permission denied (publickey)"

**Fix**: Use HTTPS instead of SSH, or setup SSH keys properly

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/cyberlearn.git
```

### Issue: "Large files detected"

**Fix**: Remove large files from Git history

```bash
# Remove file from Git
git rm --cached large_file.db

# Add to .gitignore
echo "large_file.db" >> .gitignore

# Commit
git commit -m "Remove large file"
```

### Issue: "Authentication failed"

**Fix**: Use Personal Access Token as password, not GitHub password

### Issue: Files not excluded by .gitignore

**Fix**: Remove cached files

```bash
git rm -r --cached .
git add .
git commit -m "Apply .gitignore"
```

---

## 📞 Next Steps After Push

1. **Share the repository**: Post on LinkedIn, Twitter, Reddit
2. **Deploy demo**: Use Streamlit Cloud for public demo
3. **Get feedback**: Share with cybersecurity communities
4. **Iterate**: Collect issues and implement improvements
5. **Grow**: Accept contributions from others

---

## 🎊 Complete Command Sequence

**Copy-paste this entire block on your VM:**

```bash
# Navigate to project
cd "c:\Users\yaniv\10Root Dropbox\Yaniv Radunsky\Documents\50-59 Projects\57 ClaudeCode\57.14_Learning_app"

# Initialize Git
git init

# Configure (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Stage all files
git add .

# Commit
git commit -m "Initial commit: Complete CyberLearn adaptive learning platform

- Adaptive learning engine with skill profiling
- Gamification system (XP, badges, levels, streaks)
- Interactive Streamlit UI
- Complete sample lesson (CIA Triad)
- All 10 Jim Kwik principles integrated
- Comprehensive documentation (22,000+ words)
- Production-ready code (5,000+ lines)

🛡️ Generated with Claude Code"

# Add remote (REPLACE YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/cyberlearn.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Done! Your project is now on GitHub! 🎉**

---

**Repository URL will be**: `https://github.com/YOUR_USERNAME/cyberlearn`

**Live demo URL will be** (if using Streamlit Cloud): `https://YOUR_USERNAME-cyberlearn.streamlit.app`
