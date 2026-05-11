#!/bin/bash
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

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

echo -e "${YELLOW}Warning: This will remove ka and all its configuration files.${NC}"
read -p "Are you sure you want to uninstall? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Uninstall cancelled.${NC}"
    exit 0
fi

KA_PATH=$(which ka 2>/dev/null || echo "")
if [ -n "$KA_PATH" ]; then
    rm -f "$KA_PATH"
    echo -e "${GREEN}Removed ka executable${NC}"
else
    for loc in "/usr/local/bin/ka" "$HOME/.local/bin/ka"; do
        [ -f "$loc" ] && rm -f "$loc" && echo -e "${GREEN}Removed $loc${NC}"
    done
fi

KA_CONFIG_DIR="$HOME/.config/ka"
if [ -d "$KA_CONFIG_DIR" ]; then
    rm -rf "$KA_CONFIG_DIR"
    echo -e "${GREEN}Removed configuration directory${NC}"
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
SAFE_PREFIXES=("$HOME" "/tmp" "/opt" "/usr/local" "/srv")
is_safe=false
for prefix in "${SAFE_PREFIXES[@]}"; do
    if [[ "$PROJECT_DIR" == "$prefix"* ]] && [[ "$PROJECT_DIR" != "$prefix" ]]; then
        is_safe=true
        break
    fi
done

if $is_safe && [[ "$PROJECT_DIR" != "$HOME"* ]]; then
    read -p "Remove project directory ($PROJECT_DIR)? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
        echo -e "${GREEN}Removed project directory${NC}"
    fi
fi

echo -e "${GREEN}Ka has been uninstalled.${NC}"
