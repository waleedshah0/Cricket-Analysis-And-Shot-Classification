# GitHub Upload - Quick Commands

## TL;DR - Copy & Paste These Commands

### 1. First Time Setup (One Time Only)

```powershell
cd d:\cricket

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Initialize repository
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Cricket AI Squad and Shot Classification System"
```

### 2. Add Remote & Push

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/cricket-ai-squad.git

git branch -M main

git push -u origin main
```

When prompted for password, paste your GitHub **Personal Access Token** (not your password!)

### 3. Verify

Go to: `https://github.com/YOUR_USERNAME/cricket-ai-squad`

You should see all your files!

---

## For Future Updates

```powershell
cd d:\cricket

git status              # See what changed
git add .              # Stage changes
git commit -m "Your message"
git push origin main   # Push to GitHub
```

---

## Get Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "Cricket AI Squad"
4. Check: `repo`, `workflow`
5. Click "Generate token"
6. **Copy it** (you'll only see it once)
7. Use as password when pushing

---

## Create Repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `cricket-ai-squad`
3. Description: Cricket AI Squad & Shot Classification System
4. Public or Private: Your choice
5. Click "Create repository"

---

## Useful Commands

```powershell
git status              # See current status
git log --oneline      # See commit history
git branch             # See branches
git checkout -b name   # Create new branch
git push origin main   # Push to GitHub
git pull origin main   # Pull from GitHub
```

---

## File Size Limits

⚠️ **Files too large for GitHub:**
- `model_weights.h5` (excluded by .gitignore ✅)
- `node_modules/` (excluded by .gitignore ✅)
- `venv/` (excluded by .gitignore ✅)
- `*.log` files (excluded by .gitignore ✅)

All covered! ✨

---

## If Something Goes Wrong

```powershell
# Reset to clean state
git reset --hard HEAD

# Start over
git init
git add .
git commit -m "message"
git remote add origin https://...
git push -u origin main
```

---

**You're ready! Follow the 3 sections above and you'll be on GitHub.** 🚀
