#!/bin/bash

# Ka - Easy Linux Commands
# Installation script
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
echo -e "${GREEN}☥ Ka - Easy Linux Commands Installer${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Running as root. Installing for all users.${NC}"
    INSTALL_DIR="/usr/local/bin"
else
    echo -e "${BLUE}Installing for current user only.${NC}"
    INSTALL_DIR="$HOME/.local/bin"
fi

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Check if install directory is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH${NC}"
    echo -e "Add this to your ~/.bashrc or ~/.zshrc:"
    echo -e "export PATH=\"\$PATH:$INSTALL_DIR\""
fi

# Copy main executable
echo -e "${BLUE}Installing ka executable...${NC}"
cp "$PROJECT_DIR/ka" "$INSTALL_DIR/ka"
chmod +x "$INSTALL_DIR/ka"

# Create configuration directory in user's home
KA_CONFIG_DIR="$HOME/.config/ka"
mkdir -p "$KA_CONFIG_DIR"

# Copy configuration files if they don't exist
if [ ! -f "$KA_CONFIG_DIR/config.json" ]; then
    echo -e "${BLUE}Creating default configuration...${NC}"
    cp "$PROJECT_DIR/config.json" "$KA_CONFIG_DIR/config.json"
fi

# Copy language files
if [ ! -d "$KA_CONFIG_DIR/langs" ]; then
    echo -e "${BLUE}Copying language files...${NC}"
    cp -r "$PROJECT_DIR/langs" "$KA_CONFIG_DIR/"
fi

# Copy user directory template
if [ ! -d "$KA_CONFIG_DIR/user" ]; then
    echo -e "${BLUE}Creating user custom directory...${NC}"
    cp -r "$PROJECT_DIR/user" "$KA_CONFIG_DIR/"
fi

# Create discovered and logs directories
mkdir -p "$KA_CONFIG_DIR/discovered"
mkdir -p "$KA_CONFIG_DIR/logs"

# Create symlink or wrapper script to point to config directory
cat > "$INSTALL_DIR/ka" << EOF
#!/bin/bash
export KA_HOME="$KA_CONFIG_DIR"
exec "$PROJECT_DIR/ka" "\$@"
EOF

chmod +x "$INSTALL_DIR/ka"

# Check if ka command works
if command -v ka &> /dev/null; then
    echo -e "${GREEN}✓ Ka installed successfully!${NC}"
    echo ""
    echo -e "Try running: ${YELLOW}ka help${NC}"
else
    echo -e "${YELLOW}Installation complete but 'ka' command may not be in PATH.${NC}"
    echo -e "Run: ${YELLOW}export PATH=\"\$PATH:$INSTALL_DIR\"${NC}"
fi

# Print usage instructions
echo ""
echo -e "${GREEN}Installation completed!${NC}"
echo ""
echo -e "Quick start:"
echo -e "  ${YELLOW}ka help${NC}      - Show all available commands"
echo -e "  ${YELLOW}ka version${NC}   - Show version information"
echo -e "  ${YELLOW}ka space${NC}     - Show disk space"
echo -e "  ${YELLOW}ka ram${NC}       - Show RAM usage"
echo ""
echo -e "Configuration directory: ${BLUE}$KA_CONFIG_DIR${NC}"
echo -e "To uninstall, run: ${YELLOW}./scripts/uninstall.sh${NC}"