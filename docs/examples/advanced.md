# Advanced Examples for Ka

This guide provides advanced usage examples and techniques for power users.

## Table of Contents

1. [Custom Commands](#custom-commands)
2. [Command Chaining](#command-chaining)
3. [Scripting with Ka](#scripting-with-ka)
4. [Advanced File Operations](#advanced-file-operations)
5. [Development Workflows](#development-workflows)
6. [System Administration](#system-administration)
7. [Performance Optimization](#performance-optimization)
8. [Integration with Other Tools](#integration-with-other-tools)

## Custom Commands

### Creating Complex Custom Commands

Edit `~/.config/ka/user/custom.json`:

```json
{
  "categories": {
    "advanced": {
      "name": "Advanced Commands",
      "commands": {
        "backup_daily": {
          "cmd": "tar -czvf ~/backups/backup_$(date +%Y%m%d).tar.gz ~/Documents ~/Pictures",
          "description": "Create daily backup of Documents and Pictures",
          "args": 0
        },
        "system_report": {
          "cmd": "echo '=== System Report ===' && echo 'Disk:' && df -h && echo 'Memory:' && free -h && echo 'CPU:' && top -bn1 | head -5",
          "description": "Generate full system report",
          "args": 0
        },
        "docker_clean": {
          "cmd": "docker system prune -af && docker volume prune -f",
          "description": "Clean all unused Docker resources",
          "args": 0
        },
        "git_sync": {
          "cmd": "git pull --rebase && git push",
          "description": "Pull with rebase and push changes",
          "args": 0
        },
        "log_analysis": {
          "cmd": "journalctl --since '{}' | grep -E 'error|warning' | tail -50",
          "description": "Show last 50 errors/warnings from system logs",
          "args": 1
        }
      }
    }
  }
}
```

### Command with Conditional Logic

```json
"smart_backup": {
  "cmd": "if [ -d /backup ]; then rsync -av ~/Documents /backup/; else mkdir -p /backup && rsync -av ~/Documents /backup/; fi",
  "description": "Backup Documents, creating backup folder if needed",
  "args": 0
}
```

### Command with User Input

```json
"interactive_clean": {
  "cmd": "read -p 'Are you sure? (y/n): ' confirm && if [ $confirm = 'y' ]; then sudo apt autoremove -y; fi",
  "description": "Clean with interactive confirmation",
  "args": 0
}
```

## Command Chaining

### Chain Multiple Commands

```bash
# Update and clean in sequence
ka update && ka clean

# Backup then list backup contents
ka backup_daily && ka list ~/backups/

# Copy file, then move to different location, then delete original
ka copy project.tar.gz /tmp/ && ka move /tmp/project.tar.gz ~/archives/ && ka delete project.tar.gz
```

### Conditional Chaining

```bash
# Only run clean if update succeeds
ka update && ka clean

# Run alternative if first fails
ka update || echo "Update failed"

# Run regardless of success/failure
ka backup_daily ; ka log_analysis today
```

### Parallel Execution

```bash
# Run commands in parallel
ka backup_daily & ka system_report & wait
```

## Scripting with Ka

### Basic Shell Script

Create `~/myscript.sh`:

```bash
#!/bin/bash

# System health check script
echo "System Health Report - $(date)"
echo "=============================="

ka space
echo ""
ka ram
echo ""
ka cpu
echo ""
ka battery

# Check if disk usage > 80%
USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $USAGE -gt 80 ]; then
    echo "WARNING: Disk usage is at ${USAGE}%"
    ka clean
fi
```

Make it executable:

```bash
chmod +x ~/myscript.sh
./myscript.sh
```

### Python Script with Ka

```python
#!/usr/bin/env python3

import subprocess
import json

def run_ka_command(cmd):
    """Run a ka command and return output."""
    result = subprocess.run(['ka', cmd], capture_output=True, text=True)
    return result.stdout

def get_disk_usage():
    """Get disk usage percentage."""
    output = run_ka_command('space')
    lines = output.split('\n')
    for line in lines:
        if '/' in line and not 'Filesystem' in line:
            parts = line.split()
            if len(parts) >= 5:
                return parts[4].replace('%', '')
    return '0'

# Main script
usagè = int(get_disk_usage())
if usage > 85:
    print(f"Critical: Disk usage at {usage}%")
    run_ka_command('clean')
else:
    print(f"Disk usage is {usage}% - OK")
```

### Automated Backup Script

```bash
#!/bin/bash

# Automated backup with rotation
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

echo "Starting backup at $DATE"

# Create backup
ka create folder "$BACKUP_DIR/$DATE"
ka copy ~/Documents "$BACKUP_DIR/$DATE/"
ka copy ~/Pictures "$BACKUP_DIR/$DATE/"

# Compress backup
ka tar compress "$BACKUP_DIR/backup_$DATE.tar.gz" "$BACKUP_DIR/$DATE"

# Remove uncompressed folder
ka delete force folder "$BACKUP_DIR/$DATE"

# Remove old backups
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup complete. Old backups removed."
```

## Advanced File Operations

### Batch File Processing

```json
"batch_rename": {
  "cmd": "for f in *{}; do mv \"$f\" \"${f//{}/$1}\"; done",
  "description": "Batch rename files (e.g., ka batch_rename old new)",
  "args": 2
}
```

### Find and Replace in Multiple Files

```json
"find_replace": {
  "cmd": "grep -rl '{}' . | xargs sed -i 's/{}/{}/g'",
  "description": "Find and replace text across files",
  "args": 2
}
```

### Monitor Directory for Changes

```bash
# Watch directory and log changes
while true; do
    ka list | diff - ~/last_list.txt
    ka list > ~/last_list.txt
    sleep 2
done
```

### Bulk Download from URL List

```json
"batch_download": {
  "cmd": "wget -i {} -P downloads/",
  "description": "Download URLs from file",
  "args": 1
}
```

## Development Workflows

### Git Workflow Automation

```json
"git_commit_push": {
  "cmd": "git add . && git commit -m '{}' && git push",
  "description": "Add all, commit with message, and push",
  "args": 1
},
"git_pull_rebase": {
  "cmd": "git fetch origin && git rebase origin/main && git pull",
  "description": "Fetch, rebase, and pull latest changes",
  "args": 0
},
"git_create_branch": {
  "cmd": "git checkout -b feature/{} && git push -u origin feature/{}",
  "description": "Create new feature branch and push to remote",
  "args": 1
}
```

### Docker Development Environment

```json
"dev_up": {
  "cmd": "docker-compose up -d && docker-compose logs -f",
  "description": "Start dev environment and show logs",
  "args": 0
},
"dev_down": {
  "cmd": "docker-compose down -v",
  "description": "Stop dev environment and remove volumes",
  "args": 0
},
"dev_rebuild": {
  "cmd": "docker-compose down && docker-compose build --no-cache && docker-compose up -d",
  "description": "Full rebuild of dev environment",
  "args": 0
}
```

### Python Development Commands

```json
"venv_create": {
  "cmd": "python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip",
  "description": "Create and activate virtual environment",
  "args": 0
},
"pytest_run": {
  "cmd": "pytest tests/ -v --cov=. --cov-report=html",
  "description": "Run tests with coverage report",
  "args": 0
}
```

## System Administration

### User Management

```json
"user_create": {
  "cmd": "sudo useradd -m -s /bin/bash {} && sudo passwd {}",
  "description": "Create new user with home directory",
  "args": 1
},
"user_delete": {
  "cmd": "sudo userdel -r {}",
  "description": "Delete user and home directory",
  "args": 1
}
```

### Service Management

```bash
# Restart all web services
for service in nginx mysql docker; do
    ka service restart $service
done
```

### Log Monitoring

```json
"watch_logs": {
  "cmd": "journalctl -f -u {}",
  "description": "Follow systemd service logs in real-time",
  "args": 1
}
```

### Disk Space Monitoring Alert

```bash
#!/bin/bash

# Alert if disk space is critical
USAGE=$(ka space | grep '/$' | awk '{print $5}' | sed 's/%//')
if [ $USAGE -gt 90 ]; then
    echo "CRITICAL: Disk usage at ${USAGE}%"
    ka notify "Disk space critical"
fi
```

## Performance Optimization

### System Performance Test

```json
"benchmark": {
  "cmd": "time (find / -name '*.txt' 2>/dev/null | wc -l) && time (ka find txt | wc -l)",
  "description": "Benchmark Ka vs native commands",
  "args": 0
}
```

### Monitor Resource Usage

```bash
# Log resource usage over time
while true; do
    echo "$(date): $(ka cpu | grep -oP '\d+(?=\.\d+% id)' | head -1)% CPU, $(ka ram | grep Mem | awk '{print $3}') RAM"
    sleep 60
done >> ~/resource_usage.log
```

## Integration with Other Tools

### Cron Jobs with Ka

Add to crontab (`crontab -e`):

```bash
# Daily backup at 2 AM
0 2 * * * /usr/local/bin/ka backup_daily

# Hourly disk check
0 * * * * /usr/local/bin/ka space >> ~/disk_usage.log

# Weekly cleanup
0 0 * * 0 /usr/local/bin/ka clean
```

### Notifications Integration

```json
"notify": {
  "cmd": "notify-send '{}' 'Command completed'",
  "description": "Send desktop notification",
  "args": 1
}
```

### Webhook Integration

```json
"webhook": {
  "cmd": "curl -X POST -H 'Content-Type: application/json' -d '{\"status\":\"{}\"}' https://your-webhook.url",
  "description": "Send status to webhook",
  "args": 1
}
```

### SSH Remote Execution

```bash
# Run Ka commands on remote server
ssh user@server 'ka space'

# Run multiple commands
ssh user@server 'ka update && ka clean'
```

## Debugging and Troubleshooting

### Enable Debug Mode

```bash
KA_DEBUG=1 ka space
```

### Log All Commands

Add to `~/.bashrc`:

```bash
export KA_LOG=~/.ka_history.log
```

### Profile Command Performance

```bash
time ka space
time ka find large 100
```

## Security Best Practices

### Command Validation

```json
"safe_delete": {
  "cmd": "if [[ {} =~ ^[a-zA-Z0-9_.-]+$ ]]; then rm -i {}; else echo 'Invalid filename'; fi",
  "description": "Delete only files with safe names",
  "args": 1
}
```

### Backup Before Modification

```json
"safe_edit": {
  "cmd": "cp {}.bak {} && $EDITOR {}",
  "description": "Backup before editing",
  "args": 1
}
```

## Next Steps

- Review [Command Reference](../commands.md) for all commands
- Learn about [Language Support](../languages.md)
- Read [Contributing Guide](../contributing.md) to help improve Ka