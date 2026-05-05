# Installation Guide for Ka

This document provides detailed instructions for installing Ka on various Linux distributions.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Manual Installation](#manual-installation)
4. [Distribution Specific Instructions](#distribution-specific-instructions)
5. [Post-Installation](#post-installation)
6. [Troubleshooting](#troubleshooting)
7. [Uninstallation](#uninstallation)

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Operating System | Linux (any distribution) | Ubuntu 20.04+, Linux Mint 20+, Debian 11+ |
| Python Version | 3.6 or higher | 3.9 or higher |
| Disk Space | 10 MB | 50 MB |
| RAM | 128 MB | 256 MB |
| Internet | Required only for download | Required only for download |

### Supported Distributions

- Ubuntu 18.04, 20.04, 22.04, 24.04
- Linux Mint 19, 20, 21, 22
- Debian 10, 11, 12
- Fedora 36, 37, 38, 39
- Arch Linux
- Pop!_OS 20.04, 22.04
- Elementary OS 6, 7
- Zorin OS 16, 17

## Quick Installation

### Method 1: Using Git (Recommended)

```bash
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
./scripts/install.sh
```

### Method 2: Using wget

```bash
wget https://github.com/abdelrahman-gaballah/ka/archive/refs/heads/main.zip
unzip main.zip
cd ka-main
./scripts/install.sh
```

### Method 3: Using curl

```bash
curl -L https://github.com/abdelrahman-gaballah/ka/archive/refs/heads/main.zip -o ka.zip
unzip ka.zip
cd ka-main
./scripts/install.sh
```

## Manual Installation

### Step 1: Download Ka

Choose one of the following methods:

```bash
# Using git
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka

# Or using wget
wget https://github.com/abdelrahman-gaballah/ka/archive/refs/heads/main.zip
unzip main.zip
cd ka-main
```

### Step 2: Install the Executable

```bash
# Install for current user only
mkdir -p ~/.local/bin
cp ka ~/.local/bin/
chmod +x ~/.local/bin/ka

# Or install system-wide (requires sudo)
sudo cp ka /usr/local/bin/
sudo chmod +x /usr/local/bin/ka
```

### Step 3: Create Configuration Directory

```bash
mkdir -p ~/.config/ka
```

### Step 4: Copy Configuration Files

```bash
cp config.json ~/.config/ka/
cp -r langs/ ~/.config/ka/
cp -r user/ ~/.config/ka/
mkdir -p ~/.config/ka/discovered
mkdir -p ~/.config/ka/logs
```

### Step 5: Add to PATH (if needed)

Add the following line to `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$PATH:$HOME/.local/bin"
```

Then reload:

```bash
source ~/.bashrc
```

### Step 6: Verify Installation

```bash
ka version
ka help
```

## Distribution Specific Instructions

### Ubuntu / Debian / Linux Mint

```bash
# Install dependencies (optional, for full functionality)
sudo apt update
sudo apt install -y python3 python3-pip git curl wget

# Install Ka
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
./scripts/install.sh
```

### Fedora

```bash
# Install dependencies
sudo dnf install -y python3 git curl wget

# Install Ka
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
./scripts/install.sh
```

### Arch Linux

```bash
# Install dependencies
sudo pacman -S python git curl wget

# Install Ka
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
./scripts/install.sh
```

### openSUSE

```bash
# Install dependencies
sudo zypper install -y python3 git curl wget

# Install Ka
git clone https://github.com/abdelrahman-gaballah/ka.git
cd ka
./scripts/install.sh
```

## Post-Installation

### First Run

After installation, test Ka with basic commands:

```bash
ka help
ka space
ka ram
ka list
```

### Set Default Language

Edit the configuration file:

```bash
nano ~/.config/ka/config.json
```

Change the language field:

```json
{
  "language": "en"
}
```

Available languages: `en` (English), `ar` (Arabic)

### Add Custom Commands

Edit the custom commands file:

```bash
nano ~/.config/ka/user/custom.json
```

### Enable Auto-Completion (Optional)

For bash, add to `~/.bashrc`:

```bash
_ka_completion() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=( $(compgen -W "$(ka list-commands 2>/dev/null)" -- $cur) )
}
complete -F _ka_completion ka
```

For zsh, add to `~/.zshrc`:

```bash
_ka_completion() {
    local -a commands
    commands=(${(f)"$(ka list-commands 2>/dev/null)"})
    compadd $commands
}
compdef _ka_completion ka
```

## Troubleshooting

### Issue: `ka: command not found`

**Solution 1:** Add to PATH

```bash
export PATH="$PATH:$HOME/.local/bin"
```

**Solution 2:** Reinstall with sudo

```bash
sudo cp ka /usr/local/bin/
sudo chmod +x /usr/local/bin/ka
```

### Issue: `Python not found`

**Solution:** Install Python 3.6 or higher

```bash
# Ubuntu/Debian
sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

### Issue: `Permission denied` when running installation

**Solution:** Make the script executable

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Issue: `No module named 'core'`

**Solution:** Run from the correct directory

```bash
cd /path/to/ka
./ka help
```

### Issue: Language file not found

**Solution:** Check language files exist

```bash
ls ~/.config/ka/langs/
```

If missing, copy them again:

```bash
cp -r langs/ ~/.config/ka/
```

### Issue: Custom commands not working

**Solution:** Validate JSON syntax

```bash
python3 -m json.tool ~/.config/ka/user/custom.json
```

## Uninstallation

### Automatic Uninstall

```bash
cd ka
./scripts/uninstall.sh
```

### Manual Uninstall

```bash
# Remove executable
rm -f ~/.local/bin/ka
sudo rm -f /usr/local/bin/ka

# Remove configuration
rm -rf ~/.config/ka

# Remove project directory (optional)
rm -rf /path/to/ka
```

### Clean Removal

To completely remove all Ka files:

```bash
# Find and remove all Ka-related files
find ~ -name "*ka*" -type f 2>/dev/null | grep -E "(\.ka|ka\.|~/.config/ka)"
```

## Upgrading

To upgrade to the latest version:

```bash
cd ka
git pull
./scripts/install.sh
```

Or use the update script:

```bash
./scripts/update.sh
```

## Next Steps

- Read the [Usage Guide](usage.md)
- Explore available commands in [Commands Reference](commands.md)
- Learn about [Language Support](languages.md)
- Check out [Customization](languages.md#customization)

## Support

If you encounter any issues not covered here:

1. Check the [FAQ](usage.md#faq)
2. Search existing [GitHub Issues](https://github.com/abdelrahman-gaballah/ka/issues)
3. Open a new issue with details about your system and the problem