#!/bin/bash
LOG_FILE="run_log.txt"
BRANCH="main"

echo "Uploading log file..."
if [[ -f "$LOG_FILE" ]]; then
  git add $LOG_FILE
  git commit -m "Upload log on $(date +'%Y-%m-%d %H:%M:%S')"
  git push origin $BRANCH
else
  echo "No log file found to upload."
fi
