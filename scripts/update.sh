#!/bin/bash

# Ka - Easy Linux Commands
# Update script
# Author: Abdelrahman Gaballah

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get the directory where this script is located
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
echo -e "${GREEN}☥ Ka - Easy Linux Commands Updater${NC}"
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed. Please install git first.${NC}"
    exit 1
fi

# Check if this is a git repository
if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo -e "${RED}Error: This is not a git repository.${NC}"
    echo "Please clone from GitHub and reinstall:"
    echo "  git clone https://github.com/abdelrahman-gaballah/ka.git"
    exit 1
fi

# Save current version
CURRENT_VERSION=$(git -C "$PROJECT_DIR" describe --tags 2>/dev/null || echo "unknown")

echo -e "${BLUE}Current version: ${YELLOW}$CURRENT_VERSION${NC}"

# Fetch latest changes
echo -e "${BLUE}Fetching latest updates...${NC}"
git -C "$PROJECT_DIR" fetch --tags

# Check remote for updates
git -C "$PROJECT_DIR" remote update

LOCAL=$(git -C "$PROJECT_DIR" rev-parse @)
REMOTE=$(git -C "$PROJECT_DIR" rev-parse @{u} 2>/dev/null || echo "")

if [ -z "$REMOTE" ]; then
    echo -e "${YELLOW}No remote tracking branch found. Checking for updates...${NC}"
fi

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✓ Already up to date!${NC}"
    exit 0
fi

echo -e "${YELLOW}Updates available! Updating...${NC}"

# Stash local changes if any
if ! git -C "$PROJECT_DIR" diff --quiet; then
    echo -e "${BLUE}Stashing local changes...${NC}"
    git -C "$PROJECT_DIR" stash
    STASHED=true
else
    STASHED=false
fi

# Pull latest changes
git -C "$PROJECT_DIR" pull --rebase

# Restore stashed changes if any
if [ "$STASHED" = true ]; then
    echo -e "${BLUE}Restoring local changes...${NC}"
    git -C "$PROJECT_DIR" stash pop || true
fi

NEW_VERSION=$(git -C "$PROJECT_DIR" describe --tags 2>/dev/null || echo "unknown")
echo -e "${GREEN}✓ Updated from $CURRENT_VERSION to $NEW_VERSION${NC}"

# Reinstall after update
echo -e "${BLUE}Reinstalling ka...${NC}"
"$SCRIPT_DIR/install.sh"

echo -e "${GREEN}✓ Update completed!${NC}"