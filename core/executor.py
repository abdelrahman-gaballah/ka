#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: executor.py - Execute system commands safely
Author: Abdelrahman Gaballah
"""

import subprocess
import sys
import shlex
from typing import List, Tuple, Optional

class CommandExecutor:
    """
    Execute system commands safely with argument substitution.
    """
    
    def __init__(self, dry_run: bool = False):
        """
        Initialize the executor.
        
        Args:
            dry_run: If True, print commands instead of executing
        """
        self.dry_run = dry_run
    
    def build_command(self, cmd_template: str, args: List[str]) -> Tuple[Optional[List[str]], str]:
        """
        Build the actual command by substituting {} placeholders with arguments.
        
        Args:
            cmd_template: Command template with {} placeholders
            args: Arguments provided by user
        
        Returns:
            Tuple of (command_list, error_message)
            Returns (None, error) if failed
        """
        # Split template into parts
        parts = shlex.split(cmd_template)
        result_parts = []
        arg_index = 0
        
        for part in parts:
            if part == '{}':
                if arg_index < len(args):
                    result_parts.append(args[arg_index])
                    arg_index += 1
                else:
                    return None, f"Missing argument at position {arg_index + 1}"
            else:
                result_parts.append(part)
        
        # Add remaining arguments at the end
        if arg_index < len(args):
            result_parts.extend(args[arg_index:])
        
        return result_parts, ""
    
    def execute(self, cmd_parts: List[str]) -> Tuple[bool, str, str]:
        """
        Execute a command and return the result.
        
        Args:
            cmd_parts: List of command parts (e.g., ['ls', '-la'])
        
        Returns:
            Tuple of (success, stdout, stderr)
        """
        if self.dry_run:
            print(f"[DRY RUN] Would execute: {' '.join(cmd_parts)}")
            return True, "", ""
        
        try:
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out after 30 seconds"
        except FileNotFoundError:
            return False, "", f"Command not found: {cmd_parts[0]}"
        except PermissionError:
            return False, "", f"Permission denied: {cmd_parts[0]}"
        except Exception as e:
            return False, "", str(e)
    
    def execute_with_template(self, cmd_template: str, args: List[str]) -> Tuple[bool, str]:
        """
        Execute a command using a template and user arguments.
        
        Args:
            cmd_template: Command template with {} placeholders
            args: Arguments from user
        
        Returns:
            Tuple of (success, output_message)
        """
        cmd_parts, error = self.build_command(cmd_template, args)
        
        if cmd_parts is None:
            return False, error
        
        success, stdout, stderr = self.execute(cmd_parts)
        
        output = ""
        if stdout:
            output += stdout
        if stderr:
            output += stderr
        
        return success, output.strip()
    
    def check_sudo_needed(self, cmd_parts: List[str]) -> bool:
        """
        Check if the command might need sudo privileges.
        
        Args:
            cmd_parts: The command parts to check
        
        Returns:
            True if sudo might be needed, False otherwise
        """
        # Commands that typically need sudo
        sudo_commands = [
            'apt', 'apt-get', 'dpkg', 'snap', 'systemctl',
            'service', 'modprobe', 'insmod', 'rmmod',
            'fdisk', 'mkfs', 'mount', 'umount',
            'chown', 'chmod', 'useradd', 'userdel', 'passwd'
        ]
        
        if cmd_parts and cmd_parts[0] in sudo_commands:
            return True
        
        return False

def execute_command_safe(cmd_template: str, args: List[str], dry_run: bool = False) -> bool:
    """
    Helper function to execute a command safely.
    
    Args:
        cmd_template: Command template with {} placeholders
        args: Arguments from user
        dry_run: If True, only print commands
    
    Returns:
        True if successful, False otherwise
    """
    executor = CommandExecutor(dry_run=dry_run)
    success, output = executor.execute_with_template(cmd_template, args)
    
    if output:
        print(output)
    
    return success

def run_system_command(command: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    """
    Run a system command and return the result.
    
    Args:
        command: List of command parts
        timeout: Timeout in seconds
    
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return -1, "", str(e)

def format_output(stdout: str, stderr: str, max_lines: int = 50) -> str:
    """
    Format command output for display.
    
    Args:
        stdout: Standard output from command
        stderr: Standard error from command
        max_lines: Maximum lines to display
    
    Returns:
        Formatted output string
    """
    output = ""
    
    if stdout:
        lines = stdout.split('\n')
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines.append(f"... (output truncated, {len(stdout.split(chr(10))) - max_lines} lines hidden)")
        output += '\n'.join(lines)
    
    if stderr:
        if output:
            output += '\n'
        output += f"[STDERR]\n{stderr}"
    
    return output.strip()