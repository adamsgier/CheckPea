#!/bin/bash

# Modern approach using git-filter-repo
# This is the recommended tool for rewriting git history

echo "⚠️  WARNING: This will rewrite git history using git-filter-repo!"
echo "⚠️  Make sure you have a backup of your repository!"
echo "⚠️  This action cannot be undone!"
echo ""
read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 1
fi

# Check if git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo "git-filter-repo is not installed. Installing..."
    pip install git-filter-repo
fi

echo "Using git-filter-repo to remove API key..."

# Create a text replacement file
echo "c8891da1d32a44f0b6af0b7133996c9b==>YOUR_API_KEY_HERE" > replacements.txt

# Run git-filter-repo with text replacement
git filter-repo --replace-text replacements.txt

# Clean up
rm replacements.txt

echo "✅ API key removal complete with git-filter-repo!"
echo ""
echo "Next steps:"
echo "1. Force push to update remote repository: git push --force-with-lease --all"
echo "2. Notify all collaborators to re-clone the repository"
echo "3. Create a new API key in Clarifai dashboard"
echo "4. Add the new API key to your .env file"
