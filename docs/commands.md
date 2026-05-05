# Command Reference for Ka

This document provides a complete reference of all commands available in Ka, organized by category.

## Table of Contents

1. [System Information Commands](#system-information-commands)
2. [File Operations Commands](#file-operations-commands)
3. [Network Commands](#network-commands)
4. [System Control Commands](#system-control-commands)
5. [Process Management Commands](#process-management-commands)
6. [Development Commands](#development-commands)
7. [Utility Commands](#utility-commands)
8. [Command Summary Table](#command-summary-table)

## System Information Commands

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `space` | Show disk space usage | `df -h` | 0 |
| `space inode` | Show inode usage | `df -i` | 0 |
| `space here` | Show current directory size | `du -sh .` | 0 |
| `space folder` | Show specific folder size | `du -sh {}` | 1 |
| `ram` | Show RAM usage | `free -h` | 0 |
| `ram detailed` | Show RAM with totals | `free -h -t` | 0 |
| `cpu` | Show CPU usage percentage | `top -bn1 \| grep 'Cpu(s)'` | 0 |
| `cpu cores` | Show number of CPU cores | `nproc` | 0 |
| `cpu info` | Show CPU model | `lscpu \| grep 'Model name'` | 0 |
| `battery` | Show battery status | `upower -i $(upower -e \| grep BAT) \| grep -E 'percentage\|to empty'` | 0 |
| `battery full` | Show time to full charge | `upower -i $(upower -e \| grep BAT) \| grep -E 'percentage\|to full'` | 0 |
| `uptime` | Show system uptime (pretty) | `uptime -p` | 0 |
| `uptime raw` | Show uptime raw format | `uptime` | 0 |
| `os` | Show OS name | `cat /etc/os-release \| grep PRETTY_NAME \| cut -d= -f2` | 0 |
| `kernel` | Show kernel version | `uname -r` | 0 |
| `users` | Show logged in users | `who` | 0 |
| `date` | Show current date and time | `date` | 0 |
| `calendar` | Show current month calendar | `cal` | 0 |
| `calendar year` | Show specific year calendar | `cal {}` | 1 |
| `temperature` | Show CPU temperature | `sensors \| grep 'Core 0'` | 0 |
| `disk health` | Check disk health (requires sudo) | `sudo smartctl -H /dev/sda` | 0 |

## File Operations Commands

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `list` | List all files including hidden | `ls -la` | 0 |
| `list long` | List with details | `ls -l` | 0 |
| `list all` | List including hidden only | `ls -a` | 0 |
| `list large` | List sorted by size | `ls -laS` | 0 |
| `list recent` | List sorted by date | `ls -lat` | 0 |
| `tree` | Show directory tree structure | `tree` | 0 |
| `tree depth` | Show tree with depth limit | `tree -L {}` | 1 |
| `copy` | Copy file or directory | `cp -r {} {}` | 2 |
| `copy preserve` | Copy preserving attributes | `cp -rp {} {}` | 2 |
| `move` | Move or rename file/directory | `mv {} {}` | 2 |
| `delete` | Delete with confirmation | `rm -i {}` | 1 |
| `delete force` | Force delete without confirmation | `rm -f {}` | 1 |
| `delete folder` | Delete folder recursively | `rm -rf {}` | 1 |
| `create folder` | Create new directory | `mkdir -p {}` | 1 |
| `create file` | Create empty file | `touch {}` | 1 |
| `rename` | Rename file or directory | `mv {} {}` | 2 |
| `open folder` | Open directory in file manager | `xdg-open {}` | 1 |
| `open file` | Open file with default application | `xdg-open {}` | 1 |
| `zip` | Compress to zip archive | `zip -r {}.zip {}` | 2 |
| `unzip` | Extract zip archive | `unzip {}` | 1 |
| `tar compress` | Compress to tar.gz | `tar -czvf {}.tar.gz {}` | 2 |
| `tar extract` | Extract tar.gz archive | `tar -xzvf {}` | 1 |
| `find name` | Find file by name | `find . -name {}` | 1 |
| `find text` | Search text within files | `grep -r {} .` | 1 |
| `find large` | Find files larger than N MB | `find . -type f -size +{}M` | 1 |
| `find empty` | Find empty files and directories | `find . -empty` | 0 |
| `permissions` | Show file permissions | `stat -c '%a %n' {}` | 1 |
| `chmod` | Change file permissions | `chmod {} {}` | 2 |

## Network Commands

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `ip` | Show local IP addresses | `ip -br a` | 0 |
| `ip public` | Show public IP address | `curl -s ifconfig.me` | 0 |
| `ip location` | IP geolocation | `curl -s ipinfo.io/{}` | 1 |
| `wifi` | List available WiFi networks | `nmcli device wifi list` | 0 |
| `wifi connect` | Connect to WiFi network | `nmcli device wifi connect {} password {}` | 2 |
| `wifi disconnect` | Disconnect from WiFi | `nmcli device disconnect wlan0` | 0 |
| `wifi off` | Disable WiFi radio | `nmcli radio wifi off` | 0 |
| `wifi on` | Enable WiFi radio | `nmcli radio wifi on` | 0 |
| `ping` | Ping host (4 packets) | `ping -c 4 {}` | 1 |
| `ping continuous` | Continuous ping | `ping {}` | 1 |
| `ports` | Show all open ports | `ss -tuln` | 0 |
| `ports listening` | Show listening ports only | `ss -tln` | 0 |
| `firewall status` | Show firewall status | `sudo ufw status` | 0 |
| `firewall enable` | Enable firewall | `sudo ufw enable` | 0 |
| `firewall disable` | Disable firewall | `sudo ufw disable` | 0 |
| `download` | Download file | `wget {}` | 1 |
| `download resume` | Resume interrupted download | `wget -c {}` | 1 |
| `speedtest` | Test internet speed | `speedtest-cli` | 0 |
| `dns` | Show DNS servers | `cat /etc/resolv.conf` | 0 |
| `hostname` | Show system hostname | `hostname` | 0 |

## System Control Commands

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `shutdown` | Shutdown immediately | `shutdown now` | 0 |
| `shutdown time` | Shutdown after N minutes | `shutdown +{}` | 1 |
| `cancel shutdown` | Cancel scheduled shutdown | `shutdown -c` | 0 |
| `restart` | Restart system | `reboot` | 0 |
| `suspend` | Suspend (sleep) system | `systemctl suspend` | 0 |
| `hibernate` | Hibernate system | `systemctl hibernate` | 0 |
| `lock` | Lock screen | `loginctl lock-session` | 0 |
| `logout` | Log out current user | `gnome-session-quit --no-prompt` | 0 |
| `update` | Full system update | `sudo apt update && sudo apt upgrade -y` | 0 |
| `update check` | Check for updates only | `sudo apt update` | 0 |
| `upgrade` | Upgrade packages only | `sudo apt upgrade -y` | 0 |
| `clean` | Clean system packages | `sudo apt autoremove -y && sudo apt autoclean` | 0 |
| `brightness up` | Increase brightness | `brightnessctl set +10%` | 0 |
| `brightness down` | Decrease brightness | `brightnessctl set 10%-` | 0 |
| `brightness set` | Set brightness to percentage | `brightnessctl set {}%` | 1 |
| `volume up` | Increase volume | `pactl set-sink-volume @DEFAULT_SINK@ +5%` | 0 |
| `volume down` | Decrease volume | `pactl set-sink-volume @DEFAULT_SINK@ -5%` | 0 |
| `volume set` | Set volume to percentage | `pactl set-sink-volume @DEFAULT_SINK@ {}%` | 1 |
| `mute` | Mute/unmute audio | `pactl set-sink-mute @DEFAULT_SINK@ toggle` | 0 |

## Process Management Commands

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `processes` | Show all running processes | `ps aux` | 0 |
| `processes user` | Show processes for specific user | `ps aux \| grep {}` | 1 |
| `top` | Interactive process viewer | `top` | 0 |
| `htop` | Enhanced interactive viewer | `htop` | 0 |
| `kill` | Kill process by PID | `kill {}` | 1 |
| `kill name` | Kill process by name | `pkill {}` | 1 |
| `force kill` | Force kill by PID (SIGKILL) | `kill -9 {}` | 1 |
| `memory hog` | Top 10 memory consuming processes | `ps aux --sort=-%mem \| head -10` | 0 |
| `cpu hog` | Top 10 CPU consuming processes | `ps aux --sort=-%cpu \| head -10` | 0 |
| `service status` | Check service status | `systemctl status {}` | 1 |
| `service start` | Start a system service | `sudo systemctl start {}` | 1 |
| `service stop` | Stop a system service | `sudo systemctl stop {}` | 1 |
| `service restart` | Restart a system service | `sudo systemctl restart {}` | 1 |
| `service enable` | Enable service at boot | `sudo systemctl enable {}` | 1 |
| `service disable` | Disable service at boot | `sudo systemctl disable {}` | 1 |

## Development Commands

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `git status` | Show git repository status | `git status` | 0 |
| `git pull` | Pull latest changes from remote | `git pull` | 0 |
| `git push` | Push changes to remote | `git push` | 0 |
| `git commit` | Commit changes with message | `git commit -m {}` | 1 |
| `git add` | Stage specific file | `git add {}` | 1 |
| `git add all` | Stage all changes | `git add .` | 0 |
| `git log` | Show last 10 commits | `git log --oneline -10` | 0 |
| `git branch` | List git branches | `git branch` | 0 |
| `git checkout` | Switch to branch | `git checkout {}` | 1 |
| `python run` | Run Python script | `python3 {}` | 1 |
| `python repl` | Start Python interactive shell | `python3` | 0 |
| `python install` | Install Python package with pip | `pip3 install {}` | 1 |
| `node run` | Run Node.js script | `node {}` | 1 |
| `node repl` | Start Node.js REPL | `node` | 0 |
| `npm install` | Install npm package | `npm install {}` | 1 |
| `npm init` | Initialize npm project | `npm init -y` | 0 |
| `make` | Run make build | `make` | 0 |
| `make clean` | Run make clean | `make clean` | 0 |
| `docker ps` | List running containers | `docker ps` | 0 |
| `docker ps all` | List all containers (including stopped) | `docker ps -a` | 0 |
| `docker stop` | Stop running container | `docker stop {}` | 1 |
| `docker rm` | Remove container | `docker rm {}` | 1 |
| `docker images` | List Docker images | `docker images` | 0 |
| `docker rmi` | Remove Docker image | `docker rmi {}` | 1 |

## Utility Commands

| Command | Description | Real Command | Arguments |
|---------|-------------|--------------|-----------|
| `weather` | Show weather forecast | `curl -s wttr.in/{}` | 1 |
| `weather today` | Show brief weather | `curl -s wttr.in/{}?format=3` | 1 |
| `translate` | Translate text | `trans '{}'` | 1 |
| `timer` | Set timer (seconds) | `sleep {} && paplay /usr/share/sounds/freedesktop/complete.oga` | 1 |
| `timer minutes` | Set timer (minutes) | `sleep {}m && paplay /usr/share/sounds/freedesktop/complete.oga` | 1 |
| `notes` | Open notes file in editor | `$EDITOR ~/ka_notes.txt` | 0 |
| `todo` | Show todo list | `cat ~/ka_todo.txt` | 0 |
| `todo add` | Add item to todo list | `echo {} >> ~/ka_todo.txt` | 1 |
| `todo remove` | Remove item from todo list | `sed -i '/{}/d' ~/ka_todo.txt` | 1 |
| `screenshot` | Interactive screenshot | `gnome-screenshot -i` | 0 |
| `screenshot full` | Full screen screenshot | `gnome-screenshot` | 0 |
| `screenshot window` | Active window screenshot | `gnome-screenshot -w` | 0 |
| `clipboard copy` | Copy text to clipboard | `echo {} \| xclip -selection clipboard` | 1 |
| `clipboard paste` | Paste from clipboard | `xclip -selection clipboard -o` | 0 |
| `history` | Show last 20 commands | `history \| tail -20` | 0 |
| `clear` | Clear terminal screen | `clear` | 0 |
| `echo` | Print text to terminal | `echo {}` | 1 |
| `man` | Show manual page for command | `man {}` | 1 |

## Command Summary Table

Here is a quick reference of the most commonly used commands:

| Category | Most Used Commands |
|----------|-------------------|
| System | `space`, `ram`, `cpu`, `battery`, `uptime` |
| Files | `list`, `copy`, `move`, `delete`, `create folder` |
| Network | `ip`, `wifi`, `ping`, `download` |
| Control | `shutdown`, `restart`, `lock`, `update` |
| Processes | `processes`, `kill`, `top`, `memory hog` |
| Dev | `git status`, `python run`, `docker ps` |
| Utils | `weather`, `timer`, `notes`, `screenshot` |

## Related Documentation

- [Usage Guide](usage.md) - Detailed usage instructions
- [Installation Guide](installation.md) - How to install Ka
- [Language Support](languages.md) - Multi-language features
- [Customization](languages.md#customization) - Adding custom commands