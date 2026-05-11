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
echo -e "${GREEN}☥ Ka - Easy Linux Commands Updater${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed.${NC}"
    exit 1
fi

if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo -e "${RED}Error: Not a git repository. Clone from GitHub first.${NC}"
    exit 1
fi

CURRENT_VERSION=$(git -C "$PROJECT_DIR" describe --tags 2>/dev/null || echo "unknown")
echo -e "${BLUE}Current version: ${YELLOW}$CURRENT_VERSION${NC}"

echo -e "${BLUE}Fetching latest updates...${NC}"
git -C "$PROJECT_DIR" fetch --tags

LOCAL=$(git -C "$PROJECT_DIR" rev-parse @ 2>/dev/null || echo "")
REMOTE=$(git -C "$PROJECT_DIR" rev-parse @{u} 2>/dev/null || echo "")

if [ -z "$REMOTE" ]; then
    echo -e "${YELLOW}No remote tracking branch.${NC}"
    exit 0
fi

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}Already up to date!${NC}"
    exit 0
fi

echo -e "${YELLOW}Updates available. Updating...${NC}"

STASHED=false
if ! git -C "$PROJECT_DIR" diff --quiet --ignore-submodules; then
    echo -e "${BLUE}Stashing local changes...${NC}"
    git -C "$PROJECT_DIR" stash push --include-untracked
    STASHED=true
fi

git -C "$PROJECT_DIR" pull --rebase || {
    echo -e "${RED}Merge conflict during rebase. Resolve manually.${NC}"
    exit 1
}

if [ "$STASHED" = true ]; then
    echo -e "${BLUE}Restoring local changes...${NC}"
    git -C "$PROJECT_DIR" stash pop || echo -e "${YELLOW}Note: stash kept due to conflict.${NC}"
fi

NEW_VERSION=$(git -C "$PROJECT_DIR" describe --tags 2>/dev/null || echo "unknown")
echo -e "${GREEN}Updated from $CURRENT_VERSION to $NEW_VERSION${NC}"

echo -e "${BLUE}Reinstalling...${NC}"
"$SCRIPT_DIR/install.sh"

echo -e "${GREEN}Update completed!${NC}"
