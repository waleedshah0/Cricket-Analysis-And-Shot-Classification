# Upload Project to GitHub - Step by Step Guide

## Step 1: Create GitHub Account & Repository

1. Go to https://github.com
2. Sign up if you don't have an account
3. Click "+" icon → "New repository"
4. Fill in:
   - **Repository name**: `cricket-ai-squad` (or your preferred name)
   - **Description**: Cricket AI Squad & Shot Classification System
   - **Public/Private**: Choose based on your preference
   - **Initialize with README**: No (we'll use our own)
5. Click "Create repository"

## Step 2: Copy Repository URL

After creating the repository, you'll see a page with:
```
https://github.com/YOUR_USERNAME/cricket-ai-squad.git
```

Copy this URL (we'll need it in Step 5)

## Step 3: Configure Git Locally

Open PowerShell and run:

```powershell
# Set your Git identity (one time)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Verify configuration
git config --global --list
```

## Step 4: Navigate to Project Directory

```powershell
cd d:\cricket
```

## Step 5: Initialize Git Repository

```powershell
# Initialize git
git init

# Check status
git status
```

You should see many untracked files. The `.gitignore` file we created will exclude:
- Virtual environments
- node_modules
- .env files
- Model weights (too large)
- Temporary files

## Step 6: Add Files to Git

```powershell
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status
```

## Step 7: Make First Commit

```powershell
git commit -m "Initial commit: Cricket AI Squad and Shot Classification System"
```

## Step 8: Add Remote Repository

Replace `YOUR_USERNAME` with your GitHub username and use the URL from Step 2:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/cricket-ai-squad.git
```

Verify:
```powershell
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/cricket-ai-squad.git (fetch)
origin  https://github.com/YOUR_USERNAME/cricket-ai-squad.git (push)
```

## Step 9: Push to GitHub

For the first push, use:

```powershell
git branch -M main
git push -u origin main
```

You'll be prompted for authentication:
- **Username**: Your GitHub username
- **Password**: Your GitHub personal access token (NOT your password)

### How to Create Personal Access Token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Cricket AI Squad"
4. Select scopes:
   - ✅ `repo` (full control)
   - ✅ `workflow` (GitHub Actions)
5. Click "Generate token"
6. Copy the token (you'll only see it once!)
7. Use this token as your password when pushing

## Step 10: Verify Upload

1. Go to https://github.com/YOUR_USERNAME/cricket-ai-squad
2. You should see all your files listed
3. Check the README is showing properly

## Step 11: Rename README (Optional)

Since we named our main README as `GITHUB-README.md`, rename it:

```powershell
# On GitHub website:
# 1. Click on GITHUB-README.md
# 2. Click the pencil icon to edit
# 3. Click the three dots menu
# 4. Select "Rename"
# 5. Change to "README.md"
```

Or via Git:

```powershell
git mv GITHUB-README.md README.md
git commit -m "Rename to README.md"
git push origin main
```

## Future Commits

After making changes:

```powershell
# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "Your commit message"

# Push to GitHub
git push origin main
```

## File Size Issues

If you get errors about large files:

```powershell
# Check large files
git rev-list --all --objects | sort -k2 | tail -10

# Remove large files from tracking
git rm --cached *.h5
git commit -m "Remove large model files"
```

## Useful Git Commands

```powershell
# See commit history
git log --oneline

# See what changed
git diff

# Undo last commit (before push)
git reset --soft HEAD~1

# Check current branch
git branch

# Create new branch
git checkout -b feature/new-feature

# Switch branch
git checkout main
```

## GitHub Pages (Optional - to host frontend)

1. Go to repository settings
2. Scroll to "Pages" section
3. Select source: `main` branch, `/root` folder
4. Wait for deployment
5. Your site will be available at: `https://YOUR_USERNAME.github.io/cricket-ai-squad`

## Troubleshooting

### Authentication Failed
- Use personal access token instead of password
- Check token hasn't expired
- Regenerate token if needed

### Large Files
- Add large files to `.gitignore`
- Use Git LFS for files > 100MB: https://git-lfs.github.com/

### Merge Conflicts
- Pull latest changes: `git pull origin main`
- Resolve conflicts manually
- Commit and push

### Accidentally Committed Sensitive Data
```powershell
# Remove from history (careful!)
git filter-branch --tree-filter 'rm -f .env' -- --all
git push origin --all --force
```

## Next Steps

1. ✅ Add GitHub badge to README
2. ✅ Enable GitHub Actions for CI/CD
3. ✅ Set up issue templates
4. ✅ Create contributing guidelines
5. ✅ Add code of conduct

---

**Congratulations!** Your project is now on GitHub! 🎉
