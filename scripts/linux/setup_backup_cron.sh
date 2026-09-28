#!/usr/bin/env bash
# Adds a cron entry that runs the Django backup_db management command every
# 8 hours (at 00:00, 08:00 and 16:00). Run this ONCE on the Linux server:
#
#   bash scripts/linux/setup_backup_cron.sh
#
# To remove it later, run `crontab -e` and delete the matching line.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
LOG_FILE="$PROJECT_ROOT/backups/backup_cron.log"

if [ ! -x "$PYTHON_BIN" ]; then
    echo "Could not find virtual environment Python at $PYTHON_BIN. Update this script if your venv path differs." >&2
    exit 1
fi

mkdir -p "$PROJECT_ROOT/backups"

CRON_CMD="0 0,8,16 * * * cd $PROJECT_ROOT && $PYTHON_BIN manage.py backup_db --include-media >> $LOG_FILE 2>&1"

# Install the cron job for the current user, avoiding duplicate entries if
# this script is run more than once.
( crontab -l 2>/dev/null | grep -v "manage.py backup_db" ; echo "$CRON_CMD" ) | crontab -

echo "Cron job installed. It will run every 8 hours (00:00, 08:00, 16:00)."
echo "Logs will be written to $LOG_FILE"
