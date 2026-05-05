# Usage Guide for Ka

This document provides comprehensive instructions for using Ka commands and features.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Command Categories](#command-categories)
3. [Working with Arguments](#working-with-arguments)
4. [Command Examples](#command-examples)
5. [Help System](#help-system)
6. [Language Switching](#language-switching)
7. [Custom Commands](#custom-commands)
8. [Aliases](#aliases)
9. [Tips and Tricks](#tips-and-tricks)
10. [FAQ](#faq)

## Basic Usage

The basic syntax for Ka is:

```bash
ka <command> [arguments...]
```

### First Steps

```bash
# Display all available commands
ka help

# Show version information
ka version

# Check disk space
ka space

# Check RAM usage
ka ram

# List files in current directory
ka list
```

## Command Categories

Ka organizes commands into categories for easier discovery:

| Category | Description | Example Commands |
|----------|-------------|------------------|
| System Information | Hardware and system status | `space`, `ram`, `cpu`, `battery` |
| File Operations | File and directory management | `list`, `copy`, `move`, `delete` |
| Network | Internet and WiFi commands | `ip`, `wifi`, `ping`, `download` |
| System Control | Power and system management | `shutdown`, `restart`, `suspend` |
| Process Management | Running processes | `processes`, `kill`, `top` |
| Development | Git, Python, Node.js, Docker | `git status`, `python run` |
| Utilities | Helpful tools | `weather`, `timer`, `notes` |

## Working with Arguments

### Commands with No Arguments

Some commands don't need any arguments:

```bash
ka space
ka ram
ka list
ka uptime
```

### Commands with One Argument

Use `{}` as a placeholder for the argument:

```bash
# Delete a file
ka delete myfile.txt

# Create a folder
ka create folder myproject

# Find a file
ka find myfile.txt

# Ping a host
ka ping google.com
```

### Commands with Multiple Arguments

```bash
# Copy file (source, destination)
ka copy file1.txt file2.txt

# Move file (source, destination)
ka move old.txt new.txt

# Connect to WiFi (SSID, password)
ka wifi connect MyWiFi mypassword123
```

### Commands with Optional Arguments

Some commands work with or without arguments:

```bash
# List current directory
ka list

# List specific directory
ka list /home/user/Documents
```

## Command Examples

### System Information

```bash
# Disk space
ka space                    # All disks
ka space here               # Current directory size
ka space folder Downloads   # Specific folder size

# Memory
ka ram                      # RAM usage
ka ram detailed             # RAM with totals

# CPU
ka cpu                      # CPU usage percentage
ka cpu info                 # CPU model and specs
ka cpu cores                # Number of cores

# Battery
ka battery                  # Battery percentage and time
ka battery full             # Time to full charge

# System
ka uptime                   # How long system has been running
ka os                       # Operating system name
ka kernel                   # Kernel version
ka date                     # Current date and time
ka calendar                 # Month calendar
```

### File Operations

```bash
# Listing files
ka list                     # All files including hidden
ka list large               # Sorted by size
ka list recent              # Sorted by date
ka tree                     # Directory tree structure
ka tree depth 2             # Tree with depth limit

# Copy and move
ka copy file.txt backup/    # Copy to directory
ka copy file1.txt file2.txt # Copy with new name
ka move old.txt new.txt     # Rename
ka move file.txt Documents/ # Move to directory

# Create and delete
ka create folder myproject  # New directory
ka create file config.py    # Empty file
ka delete unwanted.txt      # Delete with confirmation
ka delete force temp.log    # Force delete no confirm
ka delete folder oldstuff/  # Delete directory

# Compression
ka zip myarchive Documents/ # Create zip archive
ka unzip myarchive.zip      # Extract zip archive
ka tar compress backup.tar.gz Documents/  # Create tar.gz
ka tar extract backup.tar.gz              # Extract tar.gz

# Search
ka find myfile.txt          # Find file by name
ka find text "hello world"  # Search text in files
ka find large 100           # Files larger than 100MB
```

### Network

```bash
# IP addresses
ka ip                       # Local IP addresses
ka ip public                # Public IP address
ka ip location 8.8.8.8      # IP geolocation

# WiFi
ka wifi                     # List available networks
ka wifi connect MyWiFi pass123  # Connect to network
ka wifi disconnect          # Disconnect from WiFi
ka wifi off                 # Disable WiFi radio
ka wifi on                  # Enable WiFi radio

# Connectivity
ka ping google.com          # Ping 4 times
ka ping continuous 1.1.1.1  # Continuous ping
ka speedtest                # Internet speed test

# Firewall
ka firewall status          # Check firewall status
ka firewall enable          # Turn on firewall
ka firewall disable         # Turn off firewall

# Downloads
ka download https://example.com/file.zip  # Download file
ka download resume https://example.com/file.zip  # Resume download
```

### System Control

```bash
# Power management
ka shutdown                 # Shutdown immediately
ka shutdown 5               # Shutdown after 5 minutes
ka cancel shutdown          # Cancel scheduled shutdown
ka restart                  # Reboot system
ka suspend                  # Sleep mode
ka lock                     # Lock screen
ka logout                   # Log out current user

# Updates
ka update                   # Full system update
ka update check             # Check for updates only
ka upgrade                  # Upgrade packages only
ka clean                    # Clean unused packages

# Hardware
ka brightness up            # Increase brightness
ka brightness down          # Decrease brightness
ka brightness set 50        # Set to 50%
ka volume up                # Increase volume
ka volume down              # Decrease volume
ka volume set 30            # Set to 30%
ka mute                     # Mute/unmute
```

### Process Management

```bash
# View processes
ka processes                # All running processes
ka processes user root      # Processes for specific user
ka top                      # Interactive process viewer
ka htop                     # Enhanced process viewer

# Kill processes
ka kill 1234                # Kill process by PID
ka kill name firefox        # Kill by process name
ka force kill 1234          # Force kill (SIGKILL)

# Resource usage
ka memory hog               # Top 10 memory users
ka cpu hog                  # Top 10 CPU users

# Services
ka service status docker    # Check service status
ka service start nginx      # Start service
ka service stop nginx       # Stop service
ka service restart nginx    # Restart service
```

### Development

```bash
# Git
ka git status               # Repository status
ka git add file.py          # Stage file
ka git add all              # Stage all files
ka git commit "message"     # Commit changes
ka git push                 # Push to remote
ka git pull                 # Pull from remote
ka git log                  # View commit history
ka git branch               # List branches
ka git checkout main        # Switch branch

# Python
ka python run script.py     # Run Python script
ka python repl              # Start Python REPL
ka python install requests  # Install pip package

# Node.js
ka node run app.js          # Run Node script
ka node repl                # Start Node REPL
ka npm install express      # Install npm package
ka npm init                 # Initialize npm project

# Docker
ka docker ps                # List running containers
ka docker ps all            # List all containers
ka docker stop container    # Stop container
ka docker rm container      # Remove container
ka docker images            # List images
```

### Utilities

```bash
# Weather
ka weather Cairo            # Weather in Cairo
ka weather today Cairo      # Brief weather

# Translation
ka translate "hello world"  # Translate text

# Timers and notes
ka timer 10                 # 10 second timer
ka timer minutes 5          # 5 minute timer
ka notes                    # Open notes file
ka todo                     # Show todo list
ka todo add "Buy milk"      # Add todo item
ka todo remove "Buy milk"   # Remove todo item

# Screenshots
ka screenshot               # Interactive screenshot
ka screenshot full          # Full screen
ka screenshot window        # Active window

# Clipboard
ka clipboard copy "text"    # Copy to clipboard
ka clipboard paste          # Paste from clipboard

# General
ka clear                    # Clear terminal
ka echo "Hello World"       # Print text
ka man ls                   # Show manual for ls command
```

## Help System

### List All Commands

```bash
ka help
```

This displays all available commands organized by category.

### Command Categories

```bash
ka help system              # Show system commands only
ka help network             # Show network commands only
ka help files               # Show file commands only
```

### Command Details

```bash
ka help space               # Show details about space command
```

## Language Switching

### Check Current Language

```bash
cat ~/.config/ka/config.json
```

### Change to Arabic

Edit `~/.config/ka/config.json`:

```json
{
  "language": "ar"
}
```

### Available Languages

```bash
# List available languages
ls ~/.config/ka/langs/
```

## Custom Commands

### Adding Custom Commands

Edit `~/.config/ka/user/custom.json`:

```json
{
  "categories": {
    "my_shortcuts": {
      "name": "My Shortcuts",
      "commands": {
        "deploy": {
          "cmd": "cd ~/myproject && git pull && npm install && npm run build",
          "description": "Deploy my project",
          "args": 0
        }
      }
    }
  }
}
```

### Modifying Built-in Commands

Edit `~/.config/ka/user/modified.json`:

```json
{
  "categories": {
    "system_info": {
      "commands": {
        "space": {
          "cmd": "df -h --total",
          "description": "Disk space with total",
          "args": 0
        }
      }
    }
  }
}
```

## Aliases

Add shell aliases in `~/.config/ka/user/aliases.json`:

```json
{
  "ll": "ls -la",
  "gst": "git status",
  "dc": "docker-compose"
}
```

## Tips and Tricks

### Tip 1: Chain Commands

```bash
ka copy file.txt backup/ && ka list backup/
```

### Tip 2: Use with sudo

```bash
sudo ka update
```

### Tip 3: Create Complex Custom Commands

```json
"backup": {
  "cmd": "tar -czvf backup_$(date +%Y%m%d).tar.gz {}",
  "description": "Create dated backup",
  "args": 1
}
```

### Tip 4: Use Environment Variables

```json
"projects": {
  "cmd": "ls $PROJECTS_DIR",
  "description": "List projects",
  "args": 0
}
```

### Tip 5: Quick Navigation

```bash
alias ..="cd .."
alias ...="cd ../.."
```

Add these to `aliases.json`.

## FAQ

### Q: What happens if I type an unknown command?

A: Ka will show "Command not found" and suggest using `ka help`.

### Q: Can I use Ka in scripts?

A: Yes, Ka works in bash scripts like any other command.

### Q: How do I see the actual command being run?

A: Use dry run mode (if implemented) or check the command in the language file.

### Q: Can I undo a command?

A: No, Ka executes system commands directly. Be careful with delete commands.

### Q: Are my custom commands preserved during updates?

A: Yes, the `user/` directory is never overwritten during updates.

### Q: How do I backup my configuration?

A: Copy the `~/.config/ka` directory.

### Q: Can I share my custom commands with others?

A: Yes, share your `custom.json` and `modified.json` files.

## Next Steps

- Explore [Commands Reference](commands.md) for all available commands
- Learn about [Language Support](languages.md)
- Check [Customization Guide](languages.md#customization) for advanced usage