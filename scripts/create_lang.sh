#!/bin/bash

# Ka - Easy Linux Commands
# Create new language file script
# Author: Abdelrahman Gaballah

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LANGS_DIR="$PROJECT_DIR/langs"
TEMPLATE_FILE="$LANGS_DIR/template.json"

echo -e "${BLUE}"
echo "░██                     "
echo "░██                     "
echo "░██    ░██    ░██████   "
echo "░██   ░██          ░██  "
echo "░███████      ░███████  "
echo "░██   ░██    ░██   ░██  "
echo "░██    ░██    ░█████░██ "
echo -e "${NC}"
echo -e "${CYAN}☥ Ka - Create New Language File${NC}"
echo ""

# Check if template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${RED}Error: template.json not found in $LANGS_DIR${NC}"
    exit 1
fi

# Get language code
echo -e "${YELLOW}Enter language code (e.g., fr, es, de, zh):${NC}"
read -p "> " LANG_CODE

# Validate language code
if [ -z "$LANG_CODE" ]; then
    echo -e "${RED}Error: Language code cannot be empty${NC}"
    exit 1
fi

if [[ ! "$LANG_CODE" =~ ^[a-z]{2,3}$ ]]; then
    echo -e "${YELLOW}Warning: Language code should be 2-3 lowercase letters${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# Check if language file already exists
LANG_FILE="$LANGS_DIR/$LANG_CODE.json"
if [ -f "$LANG_FILE" ]; then
    echo -e "${RED}Error: Language file $LANG_CODE.json already exists${NC}"
    exit 1
fi

# Get language name
echo -e "${YELLOW}Enter language display name (e.g., Français, Español, Deutsch):${NC}"
read -p "> " LANG_NAME

if [ -z "$LANG_NAME" ]; then
    echo -e "${RED}Error: Language name cannot be empty${NC}"
    exit 1
fi

# Copy template to new language file
cp "$TEMPLATE_FILE" "$LANG_FILE"

# Update language code and name in the file
sed -i "s/\"language\": \"TEMPLATE\"/\"language\": \"$LANG_CODE\"/" "$LANG_FILE"
sed -i "s/\"name\": \"Template Language\"/\"name\": \"$LANG_NAME\"/" "$LANG_FILE"

echo -e "${GREEN}✓ Language file created: $LANG_FILE${NC}"
echo ""

# Ask if user wants to edit the file now
echo -e "${YELLOW}Do you want to edit the language file now? (y/N):${NC}"
read -p "> " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Try to open with default editor
    if [ -n "$EDITOR" ]; then
        $EDITOR "$LANG_FILE"
    elif command -v nano &> /dev/null; then
        nano "$LANG_FILE"
    elif command -v vim &> /dev/null; then
        vim "$LANG_FILE"
    elif command -v vi &> /dev/null; then
        vi "$LANG_FILE"
    else
        echo -e "${YELLOW}No editor found. Please edit manually: $LANG_FILE${NC}"
    fi
fi

echo ""
echo -e "${GREEN}✓ Language setup complete!${NC}"
echo ""
echo -e "To use this language, edit config.json:"
echo -e "  ${YELLOW}\"language\": \"$LANG_CODE\"${NC}"
echo ""
echo -e "Or run: ${YELLOW}ka config set language $LANG_CODE${NC}"س