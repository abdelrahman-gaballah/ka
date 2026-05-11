#!/bin/bash
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}"
echo "░██                     "
echo "░██                     "
echo "░██    ░██    ░██████   "
echo "░██   ░██          ░██  "
echo "░███████      ░███████  "
echo "░██   ░██    ░██   ░██  "
echo "░██    ░██    ░█████░██ "
echo -e "${NC}"
echo -e "${GREEN}☥ Ka - Easy Linux Commands Installer${NC}"

if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Running as root. Installing for all users.${NC}"
    INSTALL_DIR="/usr/local/bin"
else
    echo -e "${BLUE}Installing for current user only.${NC}"
    INSTALL_DIR="$HOME/.local/bin"
fi

mkdir -p "$INSTALL_DIR"

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH${NC}"
    echo "Add this to ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$PATH:$INSTALL_DIR\""
fi

echo -e "${BLUE}Installing ka...${NC}"
cp "$PROJECT_DIR/ka" "$INSTALL_DIR/ka"
chmod +x "$INSTALL_DIR/ka"

if [ -d "$PROJECT_DIR/core" ]; then
    rm -rf "$INSTALL_DIR/core"
    cp -r "$PROJECT_DIR/core" "$INSTALL_DIR/core"
fi

KA_CONFIG_DIR="$HOME/.config/ka"
mkdir -p "$KA_CONFIG_DIR"

if [ ! -f "$KA_CONFIG_DIR/config.json" ]; then
    cp "$PROJECT_DIR/config.json" "$KA_CONFIG_DIR/config.json"
fi

if [ ! -d "$KA_CONFIG_DIR/langs" ]; then
    cp -r "$PROJECT_DIR/langs" "$KA_CONFIG_DIR/"
fi

if [ ! -d "$KA_CONFIG_DIR/user" ]; then
    cp -r "$PROJECT_DIR/user" "$KA_CONFIG_DIR/"
fi

mkdir -p "$KA_CONFIG_DIR/discovered" "$KA_CONFIG_DIR/logs"

if command -v ka &> /dev/null; then
    echo -e "${GREEN}Ka installed successfully!${NC}"
    echo "Try: ka help"
else
    echo -e "${YELLOW}Installation complete but 'ka' may not be in PATH.${NC}"
    echo "Run: export PATH=\"\$PATH:$INSTALL_DIR\""
fi

echo ""
echo "Quick start:"
echo "  ka help      - Show all available commands"
echo "  ka version   - Show version information"
echo "  ka space     - Show disk space"
echo "  ka ram       - Show RAM usage"
echo ""
echo "Config directory: $KA_CONFIG_DIR"
echo ""
echo "For a proper system-wide install, use: pip install $PROJECT_DIR"
