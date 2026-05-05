#!/bin/bash

# Ka - Easy Linux Commands
# Uninstall script
# Author: Abdelrahman Gaballah

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${RED}"
echo "░██                     "
echo "░██                     "
echo "░██    ░██    ░██████   "
echo "░██   ░██          ░██  "
echo "░███████      ░███████  "
echo "░██   ░██    ░██   ░██  "
echo "░██    ░██    ░█████░██ "
echo -e "${NC}"
echo -e "${RED}☥ Ka - Easy Linux Commands Uninstaller${NC}"
echo ""

# Confirm uninstallation
echo -e "${YELLOW}Warning: This will remove ka and all its configuration files.${NC}"
read -p "Are you sure you want to uninstall? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Uninstall cancelled.${NC}"
    exit 0
fi

# Remove ka executable
KA_PATH=$(which ka 2>/dev/null || echo "")

if [ -n "$KA_PATH" ]; then
    echo -e "${BLUE}Removing ka executable from $KA_PATH...${NC}"
    rm -f "$KA_PATH"
    echo -e "${GREEN}✓ Removed ka executable${NC}"
else
    echo -e "${YELLOW}ka executable not found in PATH${NC}"
    
    # Try to remove from common locations
    for loc in "/usr/local/bin/ka" "$HOME/.local/bin/ka"; do
        if [ -f "$loc" ]; then
            echo -e "${BLUE}Removing $loc...${NC}"
            rm -f "$loc"
        fi
    done
fi

# Remove configuration directory
KA_CONFIG_DIR="$HOME/.config/ka"

if [ -d "$KA_CONFIG_DIR" ]; then
    echo -e "${BLUE}Removing configuration directory: $KA_CONFIG_DIR${NC}"
    rm -rf "$KA_CONFIG_DIR"
    echo -e "${GREEN}✓ Removed configuration files${NC}"
fi

# Ask about removing project directory (if not in HOME)
if [[ "$(pwd)" != "$HOME"* ]]; then
    echo ""
    read -p "Do you want to remove the project directory? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
        echo -e "${BLUE}Removing project directory: $PROJECT_DIR${NC}"
        rm -rf "$PROJECT_DIR"
        echo -e "${GREEN}✓ Removed project directory${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✓ Ka has been uninstalled successfully!${NC}"
echo ""
echo -e "If you added '${YELLOW}$HOME/.local/bin${NC}' to your PATH manually,"
echo -e "you may want to remove that line from your ~/.bashrc or ~/.zshrc"