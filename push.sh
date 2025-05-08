#!/bin/bash
echo "Pushing changes to GitHub..."
git add .
git commit -m "Update $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main
