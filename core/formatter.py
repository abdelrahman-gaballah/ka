#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: formatter.py - Format output for display
Author: Abdelrahman Gaballah
"""

from typing import Dict, List, Optional

class OutputFormatter:
    """
    Format output for terminal display with colors and styling.
    """
    
    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
    }
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize the formatter.
        
        Args:
            use_colors: If True, use ANSI colors in output
        """
        self.use_colors = use_colors
    
    def colorize(self, text: str, color: str) -> str:
        """
        Wrap text with color codes.
        
        Args:
            text: Text to colorize
            color: Color name from COLORS dict
        
        Returns:
            Colorized text string
        """
        if not self.use_colors:
            return text
        
        color_code = self.COLORS.get(color, self.COLORS['reset'])
        return f"{color_code}{text}{self.COLORS['reset']}"
    
    def print_header(self, title: str):
        """
        Print a section header.
        
        Args:
            title: Header text
        """
        print(self.colorize(f"\n📦 {title}", 'cyan'))
        print(self.colorize("-" * 40, 'dim'))
    
    def print_success(self, message: str):
        """
        Print a success message.
        
        Args:
            message: Success message
        """
        print(self.colorize(f"✅ {message}", 'green'))
    
    def print_error(self, message: str):
        """
        Print an error message.
        
        Args:
            message: Error message
        """
        print(self.colorize(f"❌ {message}", 'red'))
    
    def print_warning(self, message: str):
        """
        Print a warning message.
        
        Args:
            message: Warning message
        """
        print(self.colorize(f"⚠️ {message}", 'yellow'))
    
    def print_info(self, message: str):
        """
        Print an info message.
        
        Args:
            message: Info message
        """
        print(self.colorize(f"ℹ️ {message}", 'blue'))
    
    def print_command_list(self, commands: Dict, category: Optional[str] = None):
        """
        Print a formatted list of commands.
        
        Args:
            commands: Dictionary of commands with their info
            category: Optional category name to display
        """
        if category:
            print(self.colorize(f"\n📂 {category}:", 'magenta'))
        
        for cmd_name, cmd_info in commands.items():
            desc = cmd_info.get('description', 'No description')
            print(f"   {self.colorize(cmd_name, 'green')} - {desc}")
    
    def print_help_table(self, commands_by_category: Dict):
        """
        Print a help table with commands organized by category.
        
        Args:
            commands_by_category: Dict with category names as keys
        """
        self.print_header("AVAILABLE COMMANDS")
        
        for category, commands in commands_by_category.items():
            print(self.colorize(f"\n{category}:", 'yellow'))
            for cmd_name, cmd_info in commands.items():
                desc = cmd_info.get('description', '')
                args_info = f" [arg]" if cmd_info.get('args', 0) > 0 else ""
                print(f"  {self.colorize(cmd_name + args_info, 'green'):<20} - {desc}")
    
    def print_version(self, version: str, name: str = "Ka"):
        """
        Print version information.
        
        Args:
            version: Version string
            name: Application name
        """
        logo = """
░██                     
░██                     
░██    ░██    ░██████   
░██   ░██          ░██  
░███████      ░███████  
░██   ░██    ░██   ░██  
░██    ░██    ░█████░██ 
        """
        
        if self.use_colors:
            print(self.colorize(logo, 'cyan'))
        else:
            print(logo)
        
        print(self.colorize(f"☥ {name} - Easy Linux Commands", 'bold'))
        print(self.colorize(f"Version {version}", 'dim'))
    
    def print_command_result(self, stdout: str, stderr: str, max_lines: int = 50):
        """
        Print command execution result.
        
        Args:
            stdout: Standard output
            stderr: Standard error
            max_lines: Maximum lines to display
        """
        if stdout:
            lines = stdout.split('\n')
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                lines.append(self.colorize(f"... (truncated, {len(stdout.split(chr(10))) - max_lines} lines hidden)", 'dim'))
            print('\n'.join(lines))
        
        if stderr:
            print(self.colorize(stderr, 'red'))
    
    def format_command_not_found(self, command: str):
        """
        Format command not found message.
        
        Args:
            command: Command name that wasn't found
        """
        self.print_error(f"Command '{command}' not found")
        print(self.colorize("Try 'ka help' to see available commands", 'dim'))

def format_table(data: List[Dict], headers: List[str]) -> str:
    """
    Format data as a table.
    
    Args:
        data: List of dictionaries with data
        headers: List of header names
    
    Returns:
        Formatted table string
    """
    if not data:
        return ""
    
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in data:
        for i, header in enumerate(headers):
            val = str(row.get(header, ''))
            widths[i] = max(widths[i], len(val))
    
    # Build separator line
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    
    # Build header line
    header_line = "|"
    for i, header in enumerate(headers):
        header_line += f" {header:<{widths[i]}} |"
    
    # Build rows
    lines = [sep, header_line, sep]
    for row in data:
        line = "|"
        for i, header in enumerate(headers):
            val = str(row.get(header, ''))
            line += f" {val:<{widths[i]}} |"
        lines.append(line)
    lines.append(sep)
    
    return "\n".join(lines)