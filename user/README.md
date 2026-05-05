# User Customization Directory for Ka

This directory contains your personal customizations. Files here are never overwritten during updates.

## Files in this Directory

| File | Purpose |
|------|---------|
| `custom.json` | Add your own custom commands |
| `modified.json` | Override built-in commands |
| `aliases.json` | Add shell aliases |

## 1. Adding Custom Commands (`custom.json`)

Add your own commands to this file. These will appear alongside built-in commands.

### Example:

```json
{
  "categories": {
    "my_shortcuts": {
      "name": "My Personal Shortcuts",
      "commands": {
        "backupdocs": {
          "cmd": "rsync -av --progress ~/Documents /media/backup/",
          "description": "Backup my Documents folder",
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
        },
        "backup": {
          "cmd": "tar -czvf backup_{}.tar.gz {}",
          "description": "Create timestamped backup",
          "args": 2
        }
      }
    },
    "development": {
      "name": "My Dev Commands",
      "commands": {
        "rebuild": {
          "cmd": "make clean && make && sudo make install",
          "description": "Full rebuild and install",
          "args": 0
        }
      }
    }
  }
}
```

## 2. Modifying Built-in Commands (`modified.json`)

Override existing commands with your own versions. This does not delete the original, just overrides it.

### Example:

```json
{
  "categories": {
    "system_info": {
      "commands": {
        "space": {
          "cmd": "df -h --total",
          "description": "Show disk space including total",
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
    },
    "file_operations": {
      "commands": {
        "list": {
          "cmd": "ls -la --color=auto",
          "description": "List files with colors",
          "args": 0
        }
      }
    }
  }
}
```

## 3. Adding Aliases (`aliases.json`)

Add shell aliases that work like regular shortcuts.

### Example:

```json
{
  "ll": "ls -la",
  "la": "ls -a",
  "gst": "git status",
  "gco": "git checkout",
  "gcm": "git commit -m",
  "dc": "docker-compose",
  "dcu": "docker-compose up -d",
  "dcd": "docker-compose down",
  "k": "kubectl",
  "kgp": "kubectl get pods",
  "nrs": "npm run start",
  "nrb": "npm run build"
}
```

## Priority Order

When Ka looks for a command, it checks in this order:

1. `modified.json` (highest priority - overrides everything)
2. `custom.json` (user-added commands)
3. Language files (built-in commands)

This means you can completely replace any built-in command using `modified.json`.

## Tips for Custom Commands

### Using Arguments

- Use `{}` as placeholders for arguments
- Set `args` to the number of required arguments
- Extra arguments are automatically appended

### Command Examples with Arguments

| Command | Template | Args | Usage |
|---------|----------|------|-------|
| Copy files | `cp {} {}` | 2 | `ka copy source dest` |
| Greet | `echo Hello {}!` | 1 | `ka greet John` |
| Compress | `tar -czvf {}.tar.gz {}` | 2 | `ka compress output input` |

### Running Multiple Commands

Use `&&` to chain commands:

```json
"updateall": {
  "cmd": "git pull && npm install && npm run build",
  "description": "Update and rebuild project",
  "args": 0
}
```

### Using Variables

You can use environment variables:

```json
"projects": {
  "cmd": "ls $PROJECTS_DIR",
  "description": "List projects directory",
  "args": 0
}
```

### Sudo Commands

Include `sudo` in the command template:

```json
"install package": {
  "cmd": "sudo apt install {}",
  "description": "Install package with apt",
  "args": 1
}
```

## Validation

To validate your JSON files:

```bash
python -m json.tool user/custom.json
python -m json.tool user/modified.json
python -m json.tool user/aliases.json
```

## Backup

These files are your personal settings. Back them up:

```bash
cp -r ~/.config/ka/user ~/backup/ka-user/
```

## Troubleshooting

### Command not recognized

- Check JSON syntax
- Ensure `args` matches number of `{}`
- Restart ka after changes

### Override not working

- Check category name matches built-in
- Check command name matches exactly
- Ensure `modified.json` has correct structure

### Alias not working

- Restart shell after adding aliases
- Check alias name has no spaces
- Alias command must be valid shell syntax