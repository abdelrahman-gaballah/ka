#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: utils.py - Utility functions for file operations and helpers
Author: Abdelrahman Gaballah
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path object of project root
    """
    return PROJECT_ROOT

def ensure_dir(directory: Path) -> bool:
    """
    Ensure a directory exists, create if not.
    
    Args:
        directory: Path to directory
    
    Returns:
        True if directory exists or created, False otherwise
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except (PermissionError, OSError):
        return False

def file_exists(file_path: Path) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to file
    
    Returns:
        True if file exists, False otherwise
    """
    return file_path.exists() and file_path.is_file()

def read_file(file_path: Path) -> Optional[str]:
    """
    Read a file and return its content.
    
    Args:
        file_path: Path to file
    
    Returns:
        File content as string, or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (IOError, UnicodeDecodeError):
        return None

def write_file(file_path: Path, content: str) -> bool:
    """
    Write content to a file.
    
    Args:
        file_path: Path to file
        content: Content to write
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError:
        return False

def append_to_file(file_path: Path, content: str) -> bool:
    """
    Append content to a file.
    
    Args:
        file_path: Path to file
        content: Content to append
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError:
        return False

def load_json_safe(file_path: Path) -> Dict:
    """
    Load JSON file safely, return empty dict on error.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        Dictionary content or empty dict
    """
    if not file_exists(file_path):
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_json_safe(file_path: Path, data: Dict) -> bool:
    """
    Save data to JSON file safely.
    
    Args:
        file_path: Path to JSON file
        data: Data to save
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, TypeError):
        return False

def merge_dicts(base: Dict, override: Dict) -> Dict:
    """
    Recursively merge two dictionaries.
    
    Args:
        base: Base dictionary
        override: Dictionary with values to override
    
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def get_timestamp() -> str:
    """
    Get current timestamp as string.
    
    Returns:
        Timestamp string (YYYY-MM-DD HH:MM:SS)
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(message: str, level: str = "INFO", log_file: str = "ka.log") -> None:
    """
    Log a message to the log file.
    
    Args:
        message: Message to log
        level: Log level (INFO, WARNING, ERROR)
        log_file: Name of log file
    """
    log_path = PROJECT_ROOT / "logs" / log_file
    
    # Ensure logs directory exists
    ensure_dir(log_path.parent)
    
    timestamp = get_timestamp()
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    
    append_to_file(log_path, log_entry)

def run_command(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    """
    Run a system command and return result.
    
    Args:
        cmd: List of command parts
        timeout: Timeout in seconds
    
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"
    except Exception as e:
        return -1, "", str(e)

def is_command_available(command: str) -> bool:
    """
    Check if a command is available in PATH.
    
    Args:
        command: Command name to check
    
    Returns:
        True if command exists, False otherwise
    """
    return shutil.which(command) is not None

def get_shell() -> str:
    """
    Get the current user's shell.
    
    Returns:
        Shell path or 'bash' as default
    """
    return os.environ.get('SHELL', '/bin/bash')

def get_user_home() -> Path:
    """
    Get the user's home directory.
    
    Returns:
        Path to home directory
    """
    return Path.home()

def confirm_action(prompt: str, default: bool = False) -> bool:
    """
    Ask user for confirmation.
    
    Args:
        prompt: Question to ask
        default: Default answer (True for yes, False for no)
    
    Returns:
        True if confirmed, False otherwise
    """
    default_prompt = " [Y/n]: " if default else " [y/N]: "
    
    try:
        response = input(prompt + default_prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        return False
    
    if default:
        return response != 'n' and response != 'no'
    else:
        return response == 'y' or response == 'yes'

def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    os.system('clear' if os.name == 'posix' else 'cls')

def print_colored(text: str, color: str = "reset") -> None:
    """
    Print colored text to terminal.
    
    Args:
        text: Text to print
        color: Color name (red, green, yellow, blue, magenta, cyan, white, bold, dim, reset)
    """
    colors = {
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
    
    color_code = colors.get(color, colors['reset'])
    print(f"{color_code}{text}{colors['reset']}")

def exit_with_error(message: str, code: int = 1) -> None:
    """
    Print error message and exit.
    
    Args:
        message: Error message
        code: Exit code
    """
    print_colored(f"Error: {message}", "red")
    sys.exit(code)

def exit_with_success(message: str, code: int = 0) -> None:
    """
    Print success message and exit.
    
    Args:
        message: Success message
        code: Exit code
    """
    print_colored(f"✓ {message}", "green")
    sys.exit(code)

def validate_command_name(name: str) -> bool:
    """
    Validate command name (alphanumeric, hyphen, underscore).
    
    Args:
        name: Command name to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not name or len(name) > 50:
        return False
    
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_')
    return all(c in allowed_chars for c in name)

def get_version() -> str:
    """
    Get the current version of Ka.
    
    Returns:
        Version string
    """
    return "0.1.0"

def get_ka_path() -> Optional[Path]:
    """
    Get the path to the ka executable.
    
    Returns:
        Path to ka executable or None if not found
    """
    ka_path = PROJECT_ROOT / "ka"
    
    if ka_path.exists() and os.access(ka_path, os.X_OK):
        return ka_path
    
    # Check if ka is in PATH
    path_ka = shutil.which("ka")
    if path_ka:
        return Path(path_ka)
    
    return None