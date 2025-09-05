#!/bin/bash

# Script to remove API key from git history
# This will rewrite git history - use with caution!

echo "⚠️  WARNING: This will rewrite git history!"
echo "⚠️  Make sure you have a backup of your repository!"
echo "⚠️  This action cannot be undone!"
echo ""
read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 1
fi

echo "Starting git history cleanup..."

# Method 1: Using git filter-branch (older method)
echo "Using git filter-branch to remove API key..."
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch main.py && \
git checkout HEAD -- main.py && \
sed -i "s/Key c8891da1d32a44f0b6af0b7133996c9b/Key YOUR_API_KEY_HERE/g" main.py && \
git add main.py' \
--prune-empty --tag-name-filter cat -- --all

# Alternative Method 2: Using BFG Repo-Cleaner (more efficient for large repos)
# Uncomment the lines below if you prefer to use BFG (you need to install it first)
# echo "Alternative: Using BFG Repo-Cleaner..."
# echo "c8891da1d32a44f0b6af0b7133996c9b" > api-keys.txt
# bfg --replace-text api-keys.txt --no-blob-protection .
# rm api-keys.txt

echo "Cleaning up..."
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ API key removal complete!"
echo ""
echo "Next steps:"
echo "1. Force push to update remote repository: git push --force-with-lease --all"
echo "2. Notify all collaborators to re-clone the repository"
echo "3. Create a new API key in Clarifai dashboard"
echo "4. Add the new API key to your .env file"
