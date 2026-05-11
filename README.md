# ☥ ka - Easy Linux Commands

```
░██                     
░██                     
░██    ░██    ░██████   
░██   ░██          ░██  
░███████      ░███████  
░██   ░██    ░██   ░██  
░██    ░██    ░█████░██ 
```
[![GitHub stars](https://img.shields.io/github/stars/abdelrahman-gaballah/ka)](https://github.com/abdelrahman-gaballah/ka/stargazers)
[![GitHub license](https://img.shields.io/github/license/abdelrahman-gaballah/ka)](https://github.com/abdelrahman-gaballah/ka/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

**Ka** is a command-line tool that translates simple natural language commands into actual Linux commands. Type `ka space` instead of `df -h`, or `ka ram` instead of `free -h`.

---

## Table of Contents

1. [Why Ka?](#why-ka)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Command Reference](#command-reference)
6. [Language Support](#language-support)
7. [Customization](#customization)
8. [Project Structure](#project-structure)
9. [Development](#development)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)
12. [Author](#author)

---

## Why Ka?

Linux is powerful, but remembering commands like `df -h`, `free -h`, `nmcli device wifi list`, `systemctl suspend`, and `rsync -av --progress --delete` is hard for beginners.

Ka solves this by letting you write what you mean:

| You want to... | Instead of typing... | Just type... |
|----------------|----------------------|---------------|
| Check disk space | `df -h` | `ka space` |
| See RAM usage | `free -h` | `ka ram` |
| List WiFi networks | `nmcli device wifi list` | `ka wifi` |
| Suspend computer | `systemctl suspend` | `ka suspend` |
| Copy a file | `cp source.txt dest.txt` | `ka copy source.txt dest.txt` |

---

## Features

| Feature | Description |
|---------|-------------|
| 🎯 **150+ Built-in Commands** | Covers system info, files, network, processes, and more |
| 🌍 **Multi-language Support** | English, Arabic, and you can add any language |
| 🔧 **Fully Customizable** | Add your own commands or override existing ones |
| 🔌 **Program Discovery** | Detects installed programs (docker, git, node, etc.) and suggests shortcuts |
| ⚡ **Lightweight** | Zero external dependencies, pure Python standard library |
| 📴 **Works Offline** | No internet required after installation |
| 🎨 **Beautiful Output** | Colored, formatted, and paginated output |
| 🔒 **Safe** | Sanitizes user input, prevents command injection |
| 📦 **Portable** | Single executable, easy to backup and move |
| 🧪 **Well Tested** | Unit tests for all core modules |

---

## Installation

### Method 1: Quick Install (Recommended)

```bash
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
./scripts/install.sh
```

The installer will:
- Copy `ka` to `~/.local/bin/` or `/usr/local/bin/`
- Create `~/.config/ka/` with default configuration
- Copy language files and user templates
- Make the `ka` command available system-wide

### Method 2: Manual Install

```bash
# Copy executable
sudo cp ka /usr/local/bin/
sudo chmod +x /usr/local/bin/ka

# Create config directory
mkdir -p ~/.config/ka

# Copy configuration files
cp config.json ~/.config/ka/
cp -r langs/ ~/.config/ka/
cp -r user/ ~/.config/ka/
mkdir -p ~/.config/ka/discovered
mkdir -p ~/.config/ka/logs

# Add to PATH if needed (add to ~/.bashrc)
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

### Method 3: Using pip (Future)

```bash
pip install ka-linux-commands
```

### Verify Installation

```bash
ka version
# Output: Ka version 0.1.0

ka help
# Shows all available commands
```

---

## Quick Start

### First Time Users

```bash
# Show all available commands
ka help

# Show system information
ka space
ka ram
ka cpu

# Show network information
ka ip
ka wifi

# File operations
ka list
ka create folder myproject
ka copy file.txt myproject/
ka list myproject/

# System control
ka uptime
ka battery

# Process management
ka processes
ka top
```

### Examples with Arguments

```bash
# Copy file
ka copy source.txt destination.txt

# Move file
ka move old.txt new.txt

# Delete with confirmation
ka delete unwanted.txt

# Ping a website
ka ping google.com

# Find a file
ka find myfile.txt

# Shutdown after 5 minutes
ka shutdown 5m

# Cancel shutdown
ka cancel shutdown
```

---

## Command Reference

### System Information (10 commands)

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ka space` | Disk space usage | `df -h` | None |
| `ka space here` | Current directory size | `du -sh .` | None |
| `ka ram` | RAM usage | `free -h` | None |
| `ka cpu` | CPU usage | `top -bn1 \| grep "Cpu(s)"` | None |
| `ka battery` | Battery status | `upower -i` | None |
| `ka uptime` | System uptime | `uptime` | None |
| `ka os` | OS information | `cat /etc/os-release` | None |
| `ka kernel` | Kernel version | `uname -r` | None |
| `ka users` | Logged in users | `who` | None |
| `ka date` | Current date/time | `date` | None |

### File Operations (15 commands)

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ka list` | List all files | `ls -la` | Optional: path |
| `ka list large` | Sort by size | `ls -laS` | Optional: path |
| `ka list recent` | Sort by date | `ls -lat` | Optional: path |
| `ka tree` | Directory tree | `tree` | Optional: path |
| `ka copy` | Copy file/dir | `cp -r` | source, destination |
| `ka move` | Move file/dir | `mv` | source, destination |
| `ka delete` | Delete with confirm | `rm -i` | file |
| `ka delete force` | Force delete | `rm -f` | file |
| `ka create folder` | Create directory | `mkdir -p` | folder_name |
| `ka create file` | Create empty file | `touch` | file_name |
| `ka rename` | Rename file | `mv` | old, new |
| `ka open folder` | Open in file manager | `xdg-open` | folder |
| `ka zip` | Compress file/dir | `zip -r` | output, input |
| `ka unzip` | Extract archive | `unzip` | file |
| `ka find` | Search for file | `find . -name` | filename |

### Network (10 commands)

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ka ip` | IP addresses | `ip a` | None |
| `ka ip public` | Public IP | `curl ifconfig.me` | None |
| `ka wifi` | List WiFi networks | `nmcli dev wifi list` | None |
| `ka wifi connect` | Connect to WiFi | `nmcli dev wifi connect` | SSID, password |
| `ka wifi off` | Disable WiFi | `nmcli radio wifi off` | None |
| `ka wifi on` | Enable WiFi | `nmcli radio wifi on` | None |
| `ka ping` | Ping host | `ping -c 4` | hostname |
| `ka ports` | Open ports | `ss -tuln` | None |
| `ka firewall status` | Firewall status | `sudo ufw status` | None |
| `ka speedtest` | Internet speed | `speedtest-cli` | None |

### System Control (12 commands)

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ka shutdown` | Shutdown now | `shutdown now` | None |
| `ka shutdown` | Shutdown after N minutes | `shutdown +` | minutes |
| `ka restart` | Reboot | `reboot` | None |
| `ka suspend` | Suspend | `systemctl suspend` | None |
| `ka lock` | Lock screen | `loginctl lock-session` | None |
| `ka logout` | Log out | `gnome-session-quit` | None |
| `ka update` | Update packages | `sudo apt update && sudo apt upgrade` | None |
| `ka clean` | Clean apt cache | `sudo apt autoremove && sudo apt autoclean` | None |
| `ka brightness up` | Increase brightness | `brightnessctl set +10%` | None |
| `ka brightness down` | Decrease brightness | `brightnessctl set 10%-` | None |
| `ka volume up` | Increase volume | `pactl set-sink-volume @DEFAULT_SINK@ +5%` | None |
| `ka volume down` | Decrease volume | `pactl set-sink-volume @DEFAULT_SINK@ -5%` | None |

### Process Management (8 commands)

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ka processes` | All processes | `ps aux` | None |
| `ka top` | Real-time processes | `top` | None |
| `ka kill` | Kill process by PID | `kill` | pid |
| `ka kill name` | Kill by name | `pkill` | process_name |
| `ka force kill` | Force kill | `kill -9` | pid |
| `ka memory hog` | Top memory users | `ps aux --sort=-%mem \| head -10` | None |
| `ka cpu hog` | Top CPU users | `ps aux --sort=-%cpu \| head -10` | None |
| `ka service status` | Service status | `systemctl status` | service_name |

### Development (10 commands)

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ka git status` | Git status | `git status` | None |
| `ka git pull` | Git pull | `git pull` | None |
| `ka git push` | Git push | `git push` | None |
| `ka git commit` | Git commit | `git commit -m` | message |
| `ka python run` | Run Python script | `python3` | script.py |
| `ka python repl` | Python REPL | `python3` | None |
| `ka node run` | Run Node.js script | `node` | script.js |
| `ka npm install` | Install npm package | `npm install` | package_name |
| `ka make` | Run make | `make` | None |
| `ka docker ps` | List containers | `docker ps` | None |

### Useful Utilities (10 commands)

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ka weather` | Weather forecast | `curl wttr.in` | Optional: city |
| `ka translate` | Translate text | `trans` | text |
| `ka calendar` | Show calendar | `cal` | None |
| `ka timer` | Set timer | `sleep` | seconds |
| `ka notes` | Open notes | `$EDITOR ~/.ka_notes.txt` | None |
| `ka todo` | Show todo list | `cat ~/.ka_todo.txt` | None |
| `ka todo add` | Add todo item | `echo` | task |
| `ka clipboard copy` | Copy to clipboard | `xclip -selection clipboard` | text |
| `ka clipboard paste` | Paste from clipboard | `xclip -selection clipboard -o` | None |
| `ka screenshot` | Take screenshot | `gnome-screenshot` | None |

---

## Language Support

### Current Languages

| Code | Language | Status | Coverage |
|------|----------|--------|----------|
| `en` | English | 100% | All commands |
| `ar` | العربية (Arabic) | 100% | All commands |

### Change Language

```bash
# Edit config file
nano ~/.config/ka/config.json
```

Change the `language` field:

```json
{
  "language": "ar",
  "auto_discover": true,
  "confirm_dangerous": true
}
```

### Add a New Language

Run the language creation script:

```bash
cd ka
./scripts/create_lang.sh
```

Follow the prompts:
1. Enter language code (e.g., `fr`, `es`, `de`, `zh`)
2. Enter language name (e.g., `Français`, `Español`)
3. The script creates `langs/{code}.json` from `template.json`
4. Translate the file manually or use a translation tool

### Language File Structure

```json
{
  "language": "en",
  "name": "English",
  "categories": {
    "system_info": {
      "name": "System Information",
      "commands": {
        "space": {
          "cmd": "df -h",
          "description": "Show disk space usage",
          "args": 0
        }
      }
    }
  }
}
```

---

## Customization

### Add Your Own Command

Edit `~/.config/ka/user/custom.json`:

```json
{
  "categories": {
    "my_shortcuts": {
      "name": "My Shortcuts",
      "commands": {
        "backupdocs": {
          "cmd": "rsync -av --progress ~/Documents /media/backup/",
          "description": "Backup Documents folder",
          "args": 0
        },
        "deploy": {
          "cmd": "cd ~/myproject && git pull && npm install && npm run build",
          "description": "Deploy my project",
          "args": 0
        },
        "greet": {
          "cmd": "echo Hello {}! Welcome to Ka",
          "description": "Greet someone",
          "args": 1
        }
      }
    }
  }
}
```

### Modify Existing Command

Edit `~/.config/ka/user/modified.json`:

```json
{
  "categories": {
    "system_info": {
      "commands": {
        "space": {
          "cmd": "df -h --total",
          "description": "Show disk space with total",
          "args": 0
        }
      }
    },
    "network": {
      "commands": {
        "ping": {
          "cmd": "ping -c 10 {}",
          "description": "Send 10 ping packets",
          "args": 1
        }
      }
    }
  }
}
```

### Add Shell Alias

Edit `~/.config/ka/user/aliases.json`:

```json
{
  "ll": "ls -la",
  "gst": "git status",
  "gco": "git checkout",
  "dc": "docker-compose"
}
```

### Program Discovery

Ka automatically detects installed programs and suggests shortcuts:

```bash
# Run discovery manually
ka discover

# View discovered programs
ka discovered list
```

Discovered shortcuts are added automatically and can be used immediately.

---

## Project Structure

```
ka/
│
├── ka                          # Main executable (Python script)
├── config.json                 # User configuration (language, options)
├── README.md                   # This file
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── setup.py                    # Pip installation setup
│
├── core/                       # Core modules
│   ├── __init__.py
│   ├── loader.py               # Load language and user files
│   ├── parser.py               # Parse user input
│   ├── executor.py             # Execute system commands
│   ├── formatter.py            # Format terminal output
│   ├── lang_manager.py         # Manage language files
│   ├── user_manager.py         # Manage user customizations
│   ├── discoverer.py           # Discover installed programs
│   └── utils.py                # Utility functions
│
├── langs/                      # Language files
│   ├── en.json                 # English (default)
│   ├── ar.json                 # Arabic
│   └── template.json           # Template for new languages
│
├── user/                       # User data (preserved during updates)
│   ├── custom.json             # User-added commands
│   ├── modified.json           # User-modified commands
│   └── aliases.json            # User shell aliases
│
├── discovered/                 # Auto-discovered programs cache
│   ├── programs.json           # Discovered programs list
│   └── cache.json              # Discovery cache
│
├── logs/                       # Log files
│   └── ka.log                  # Application logs
│
├── scripts/                    # Helper scripts
│   ├── install.sh              # Install Ka system-wide
│   ├── update.sh               # Update to latest version
│   ├── uninstall.sh            # Remove Ka completely
│   └── create_lang.sh          # Create new language file
│
├── tests/                      # Unit tests
│   ├── test_loader.py
│   ├── test_parser.py
│   ├── test_executor.py
│   ├── test_lang_manager.py
│   └── fixtures/
│       └── sample_lang.json
│
├── docs/                       # Documentation
│   ├── installation.md
│   ├── usage.md
│   ├── commands.md
│   ├── languages.md
│   └── examples/
│
└── .github/                    # GitHub configuration
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── ci.yml
```

---

## Development

### Prerequisites

```bash
python3 --version  # Python 3.6+
git --version      # Git for cloning
```

### Setup Development Environment

```bash
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest tests/ -v
python -m pytest tests/ --cov=core/
```

### Run Without Installing

```bash
./ka help
./ka space
./ka version
```

### Add a New Command to Default Language

1. Edit `langs/en.json`
2. Add your command to the appropriate category:

```json
"mycommand": {
  "cmd": "actual-command --options",
  "description": "What this command does",
  "args": 0
}
```

3. Test it: `./ka mycommand`

### Build Distribution

```bash
python setup.py sdist bdist_wheel
```

### Code Style

```bash
# Check with pylint
pylint core/

# Format with black
black core/
```

---

## Troubleshooting

### Issue: `ka: command not found`

**Solution:** Add `~/.local/bin` to PATH:

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: `Permission denied` when running commands

**Solution:** Some commands need sudo. Run with privileges:

```bash
sudo ka update
```

### Issue: Language file JSON errors

**Solution:** Validate JSON syntax:

```bash
python -m json.tool ~/.config/ka/langs/your_lang.json
```

### Issue: Nothing happens when typing commands

**Solution:** Check that Ka is properly installed:

```bash
which ka
ka version
```

### Issue: Colors not showing

**Solution:** Some terminals don't support ANSI colors. Disable colors in config:

```json
{
  "use_colors": false
}
```

### Issue: Custom commands not working

**Solution:** Check JSON syntax in `~/.config/ka/user/custom.json`:

```bash
python -m json.tool ~/.config/ka/user/custom.json
```

---

## License

MIT License — Copyright (c) 2026 Abdelrahman Gaballah

---

## Author

**Abdelrahman Gaballah** — [GitHub](https://github.com/abdelrahman-gaballah)