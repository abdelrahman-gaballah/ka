#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: parser.py - Parse and validate user input
Author: Abdelrahman Gaballah
"""

import re
import shlex
from typing import Tuple, List, Optional, Dict

class CommandParser:
    """
    Parser class to handle user input validation and command extraction.
    """
    
    def __init__(self):
        """Initialize the parser with command patterns."""
        # Allowed characters in command names (letters, numbers, hyphen, underscore)
        self.command_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
        
        # Allowed characters in arguments (safe characters only)
        self.arg_pattern = re.compile(r'^[a-zA-Z0-9_\-./\\:]+$')
    
    def parse_input(self, args: List[str]) -> Tuple[Optional[str], List[str]]:
        """
        Parse command line arguments.
        
        Args:
            args: List of command line arguments (sys.argv[1:])
        
        Returns:
            Tuple of (command_name, list_of_arguments)
            Returns (None, []) if no command provided
        """
        if not args:
            return None, []
        
        command_name = args[0].lower()
        arguments = args[1:] if len(args) > 1 else []
        
        return command_name, arguments
    
    def validate_command_name(self, command_name: str) -> bool:
        """
        Validate that the command name contains only safe characters.
        
        Args:
            command_name: The command name to validate
        
        Returns:
            True if valid, False otherwise
        """
        if not command_name:
            return False
        return bool(self.command_pattern.match(command_name))
    
    def validate_arguments(self, arguments: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate all arguments for safety.
        
        Args:
            arguments: List of arguments to validate
        
        Returns:
            Tuple of (is_valid, list_of_invalid_arguments)
        """
        invalid_args = []
        
        for arg in arguments:
            # Skip empty strings
            if not arg:
                continue
            
            # Check for dangerous patterns
            if self._is_dangerous_pattern(arg):
                invalid_args.append(arg)
                continue
            
            # Check against allowed pattern
            if not self.arg_pattern.match(arg):
                # Allow paths with spaces (quoted) - they come as single arg
                if ' ' in arg:
                    # Check each part after splitting by space
                    parts = arg.split()
                    for part in parts:
                        if part and not self.arg_pattern.match(part) and not self._is_dangerous_pattern(part):
                            invalid_args.append(part)
                elif not self._is_safe_special_char(arg):
                    invalid_args.append(arg)
        
        return len(invalid_args) == 0, invalid_args
    
    def _is_dangerous_pattern(self, text: str) -> bool:
        """
        Check if text contains dangerous shell patterns.
        
        Args:
            text: The string to check
        
        Returns:
            True if dangerous pattern found, False otherwise
        """
        dangerous_patterns = [
            ';', '&&', '||', '|', '`', '$(',
            '$(', '${', '$[', '((', '))',
            '>', '>>', '<', '<<',
            '*', '?', '[', ']',
            '&', '#', '!', '~'
        ]
        
        # Special handling for asterisk - allow as wildcard? No, too dangerous
        for pattern in dangerous_patterns:
            if pattern in text:
                # Allow slash and dot and colon for paths
                if pattern in ['/', '.', ':']:
                    continue
                return True
        return False
    
    def _is_safe_special_char(self, text: str) -> bool:
        """
        Allow certain special characters that are safe.
        
        Args:
            text: The string to check
        
        Returns:
            True if safe, False otherwise
        """
        # Allow these characters as they are common in file names
        safe_chars = ['-', '_', '.', '/', ':', '@']
        
        # Check if all characters are either alphanumeric or in safe_chars
        for char in text:
            if not (char.isalnum() or char in safe_chars):
                return False
        return True
    
    def sanitize_argument(self, arg: str) -> str:
        """
        Sanitize a single argument to make it safe.
        
        Args:
            arg: The argument to sanitize
        
        Returns:
            Sanitized argument string
        """
        # Remove any dangerous shell metacharacters
        dangerous = [';', '&&', '||', '|', '`', '$(', '$(']
        result = arg
        
        for d in dangerous:
            result = result.replace(d, '')
        
        return result.strip()
    
    def check_argument_count(self, command_info: Dict, provided_args: List[str]) -> Tuple[bool, str]:
        """
        Check if the number of arguments matches command expectations.
        
        Args:
            command_info: Command information dict with 'args' key
            provided_args: List of arguments provided by user
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_args = command_info.get('args', 0)
        
        if required_args == 0:
            if provided_args:
                # Some commands can accept extra args, so this is a warning, not error
                return True, ""
            return True, ""
        
        if len(provided_args) < required_args:
            return False, f"Missing arguments. Expected {required_args}, got {len(provided_args)}"
        
        return True, ""
    
    def extract_command_name(self, full_input: str) -> Optional[str]:
        """
        Extract command name from full input string (for cases where user types the full command).
        
        Args:
            full_input: Full command string
        
        Returns:
            Command name or None
        """
        # Split using shell-like parsing
        try:
            parts = shlex.split(full_input)
            if parts:
                return parts[0].lower()
        except ValueError:
            # Invalid quoting, try simple split
            parts = full_input.split()
            if parts:
                return parts[0].lower()
        
        return None

def quick_parse(args: List[str]) -> Tuple[Optional[str], List[str]]:
    """
    Quick helper function to parse command line arguments.
    
    Args:
        args: List of command line arguments (sys.argv[1:])
    
    Returns:
        Tuple of (command_name, list_of_arguments)
    """
    parser = CommandParser()
    return parser.parse_input(args)

def is_help_request(command_name: str, args: List[str]) -> bool:
    """
    Check if user is requesting help.
    
    Args:
        command_name: The command name
        args: List of arguments
    
    Returns:
        True if help requested, False otherwise
    """
    help_flags = ['help', '-h', '--help', '-help', '?']
    
    if command_name in help_flags:
        return True
    
    for arg in args:
        if arg in help_flags:
            return True
    
    return False

def is_version_request(command_name: str, args: List[str]) -> bool:
    """
    Check if user is requesting version info.
    
    Args:
        command_name: The command name
        args: List of arguments
    
    Returns:
        True if version requested, False otherwise
    """
    version_flags = ['version', '-v', '--version', '-version']
    
    if command_name in version_flags:
        return True
    
    for arg in args:
        if arg in version_flags:
            return True
    
    return False