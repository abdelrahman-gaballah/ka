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

**Ka** is a simple command-line tool that turns plain English into actual Linux commands. Instead of remembering `df -h`, you type `ka space`. Instead of `free -h`, you type `ka ram`. Works offline, no dependencies, just works.

---

## Why bother?

Linux is great but the commands are a mess. Beginners get lost. I got tired of explaining `rsync -av --progress --delete` to people. So I built Ka. You write what you want, it runs the real stuff.

| If you want to... | Instead of typing... | Type this... |
|-------------------|----------------------|---------------|
| Check disk space | `df -h` | `ka space` |
| See RAM usage | `free -h` | `ka ram` |
| List WiFi networks | `nmcli device wifi list` | `ka wifi` |
| Suspend computer | `systemctl suspend` | `ka suspend` |
| Copy a file | `cp source.txt dest.txt` | `ka copy source.txt dest.txt` |

Yeah, that's the whole idea.

---

## What's inside

- Around 150 commands built in. Covers system info, files, network, processes.
- Works in English and Arabic. You can add your own language if you want.
- You can add or override commands. It's just JSON.
- Automatically detects what programs you have (docker, git, node) and suggests shortcuts.
- No external packages. Just Python's standard library.
- No internet needed after install.
- Colored output. Paginated if too long.
- Won't let you inject nasty stuff. Input is sanitized.
- Single executable. Easy to move around.
- There are tests. Not perfect, but they exist.

---

## How to install

### Quick way (just run this)

```bash
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
./scripts/install.sh
```

It puts `ka` in `~/.local/bin/` or `/usr/local/bin/`, creates `~/.config/ka/` with default configs, copies language files, and makes the command available.

### Manual way (if you like control)

```bash
sudo cp ka /usr/local/bin/
sudo chmod +x /usr/local/bin/ka
mkdir -p ~/.config/ka
cp config.json ~/.config/ka/
cp -r langs/ ~/.config/ka/
cp -r user/ ~/.config/ka/
mkdir -p ~/.config/ka/discovered
mkdir -p ~/.config/ka/logs
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

### Check if it worked

```bash
ka version
ka help
```

---

## First steps

```bash
ka space
ka ram
ka cpu
ka ip
ka wifi
ka list
ka create folder myproject
ka copy file.txt myproject/
ka uptime
ka battery
ka processes
ka top
```

For commands that need arguments:

```bash
ka copy source.txt destination.txt
ka move old.txt new.txt
ka delete unwanted.txt
ka ping google.com
ka find myfile.txt
ka shutdown 5m
ka cancel shutdown
```

---

## Commands reference (not all, but most)

### System info

| What you type | What it runs | Args |
|---------------|--------------|------|
| `ka space` | `df -h` | none |
| `ka space here` | `du -sh .` | none |
| `ka ram` | `free -h` | none |
| `ka cpu` | `top -bn1 \| grep "Cpu(s)"` | none |
| `ka battery` | `upower -i` | none |
| `ka uptime` | `uptime` | none |
| `ka os` | `cat /etc/os-release` | none |
| `ka kernel` | `uname -r` | none |

### Files

| What you type | What it runs | Args |
|---------------|--------------|------|
| `ka list` | `ls -la` | optional path |
| `ka list large` | `ls -laS` | optional path |
| `ka list recent` | `ls -lat` | optional path |
| `ka tree` | `tree` | optional path |
| `ka copy` | `cp -r` | source, dest |
| `ka move` | `mv` | source, dest |
| `ka delete` | `rm -i` | file |
| `ka delete force` | `rm -f` | file |
| `ka create folder` | `mkdir -p` | folder name |
| `ka create file` | `touch` | file name |
| `ka rename` | `mv` | old, new |
| `ka zip` | `zip -r` | output, input |
| `ka unzip` | `unzip` | file |
| `ka find` | `find . -name` | filename |

### Network

| What you type | What it runs | Args |
|---------------|--------------|------|
| `ka ip` | `ip a` | none |
| `ka ip public` | `curl ifconfig.me` | none |
| `ka wifi` | `nmcli dev wifi list` | none |
| `ka wifi connect` | `nmcli dev wifi connect` | SSID, password |
| `ka wifi off` | `nmcli radio wifi off` | none |
| `ka wifi on` | `nmcli radio wifi on` | none |
| `ka ping` | `ping -c 4` | hostname |
| `ka ports` | `ss -tuln` | none |
| `ka firewall status` | `sudo ufw status` | none |

### System control

| What you type | What it runs | Args |
|---------------|--------------|------|
| `ka shutdown` | `shutdown now` | none |
| `ka shutdown 5m` | `shutdown +5` | minutes |
| `ka restart` | `reboot` | none |
| `ka suspend` | `systemctl suspend` | none |
| `ka lock` | `loginctl lock-session` | none |
| `ka logout` | `gnome-session-quit` | none |
| `ka update` | `sudo apt update && sudo apt upgrade` | none |
| `ka clean` | `sudo apt autoremove && sudo apt autoclean` | none |
| `ka brightness up` | `brightnessctl set +10%` | none |
| `ka brightness down` | `brightnessctl set 10%-` | none |

### Processes

| What you type | What it runs | Args |
|---------------|--------------|------|
| `ka processes` | `ps aux` | none |
| `ka top` | `top` | none |
| `ka kill 1234` | `kill 1234` | pid |
| `ka kill name firefox` | `pkill firefox` | process name |
| `ka force kill 1234` | `kill -9 1234` | pid |
| `ka memory hog` | `ps aux --sort=-%mem \| head -10` | none |
| `ka cpu hog` | `ps aux --sort=-%cpu \| head -10` | none |

### Development shortcuts

| What you type | What it runs | Args |
|---------------|--------------|------|
| `ka git status` | `git status` | none |
| `ka git pull` | `git pull` | none |
| `ka git push` | `git push` | none |
| `ka git commit "msg"` | `git commit -m "msg"` | message |
| `ka python run script.py` | `python3 script.py` | script name |
| `ka python repl` | `python3` | none |
| `ka npm install express` | `npm install express` | package name |
| `ka docker ps` | `docker ps` | none |

### Other useful stuff

| What you type | What it runs | Args |
|---------------|--------------|------|
| `ka weather` | `curl wttr.in` | optional city |
| `ka weather cairo` | `curl wttr.in/cairo` | city |
| `ka calendar` | `cal` | none |
| `ka timer 30` | `sleep 30` | seconds |
| `ka notes` | `$EDITOR ~/.ka_notes.txt` | none |
| `ka todo` | `cat ~/.ka_todo.txt` | none |
| `ka todo add "buy milk"` | `echo "buy milk" >> ~/.ka_todo.txt` | task |
| `ka screenshot` | `gnome-screenshot` | none |

---

## Languages

Right now: English (en) and Arabic (ar). All commands work in both.

Switch language by editing `~/.config/ka/config.json`:

```json
{
  "language": "ar",
  "auto_discover": true,
  "confirm_dangerous": true
}
```

To add your own language:

```bash
cd ka
./scripts/create_lang.sh
```

Enter language code (like `fr`, `es`, `de`) and name. It copies `template.json` to `langs/{code}.json`. Then translate the file manually. It's a bit of work but doable.

---

## Adding your own commands

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
        "greet": {
          "cmd": "echo Hello {}!",
          "description": "Say hello to someone",
          "args": 1
        }
      }
    }
  }
}
```

That's it. Now `ka greet World` works.

To override an existing command, put it in `~/.config/ka/user/modified.json` with the same structure.

---

## Program discovery

Ka looks at what's installed on your system (docker, git, node, etc.) and makes shortcuts automatically. Run `ka discover` to trigger it manually. Then `ka discovered list` to see them. No extra config needed.

---

## Project layout (if you care)

```
ka/
├── ka                          # main script
├── config.json                 # user settings
├── core/                       # loader, parser, executor, etc.
├── langs/                      # en.json, ar.json, template.json
├── user/                       # custom.json, modified.json, aliases.json
├── discovered/                 # cached results from auto-discovery
├── logs/                       # ka.log
├── scripts/                    # install, update, uninstall, create_lang
├── tests/                      # unit tests
└── docs/                       # more detailed docs
```

---

## Developing / hacking

```bash
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run without installing:

```bash
./ka help
./ka space
```

Run tests:

```bash
python -m pytest tests/ -v
```

Add a new command to the default English set: edit `langs/en.json`, find the right category, add:

```json
"mycommand": {
  "cmd": "actual-command --options",
  "description": "what it does",
  "args": 0
}
```

Then test: `./ka mycommand`

---

## Stuff that breaks sometimes

**`ka: command not found`**  
Add `~/.local/bin` to your PATH:  
`echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc && source ~/.bashrc`

**Permission denied**  
Some commands need sudo. Use `sudo ka update` for those.

**Nothing happens**  
Check that Ka is actually installed: `which ka` and `ka version`. If nothing, re-run install.

**Colors are missing**  
Some terminals don't like ANSI. Turn off colors in `config.json`: `"use_colors": false`

**Custom commands not working**  
Your JSON is probably broken. Validate it:  
`python -m json.tool ~/.config/ka/user/custom.json`

---

## License

MIT. Do whatever you want. Copyright 2026 Abdelrahman Gaballah.

---

## Author

Abdelrahman Gaballah — [GitHub](https://github.com/abdelrahman-gaballah)
