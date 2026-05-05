#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: loader.py - Load and merge language files
Author: Abdelrahman Gaballah
"""

import json
import os
from pathlib import Path

# Get the project root directory (parent of core folder)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def load_json_file(file_path):
    """
    Load a JSON file and return its content as a dictionary.
    
    Args:
        file_path (Path): Path to the JSON file
    
    Returns:
        dict: Content of the JSON file, or empty dict if file not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File not found - {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path} - {e}")
        return {}

def load_language(lang_code):
    """
    Load a language file from langs/ directory.
    
    Args:
        lang_code (str): Language code (e.g., 'en', 'ar')
    
    Returns:
        dict: Language data, or empty dict if not found
    """
    lang_path = PROJECT_ROOT / "langs" / f"{lang_code}.json"
    return load_json_file(lang_path)

def load_user_custom():
    """
    Load user custom commands from user/custom.json.
    
    Returns:
        dict: User custom commands data
    """
    custom_path = PROJECT_ROOT / "user" / "custom.json"
    return load_json_file(custom_path)

def load_user_modified():
    """
    Load user modified commands from user/modified.json.
    These override built-in commands.
    
    Returns:
        dict: User modified commands data
    """
    modified_path = PROJECT_ROOT / "user" / "modified.json"
    return load_json_file(modified_path)

def merge_commands(lang_data, user_custom, user_modified):
    """
    Merge built-in commands with user custom and user modified commands.
    Priority: user_modified > user_custom > lang_data
    
    Args:
        lang_data (dict): Built-in language commands
        user_custom (dict): User added custom commands
        user_modified (dict): User modified existing commands
    
    Returns:
        dict: Merged commands with proper priority
    """
    result = lang_data.copy() if lang_data else {}
    
    # Ensure categories exist
    if 'categories' not in result:
        result['categories'] = {}
    
    # Apply user modified commands (highest priority - override)
    if user_modified and 'categories' in user_modified:
        for cat_name, cat_data in user_modified['categories'].items():
            if cat_name not in result['categories']:
                result['categories'][cat_name] = {}
            if 'commands' in cat_data:
                if 'commands' not in result['categories'][cat_name]:
                    result['categories'][cat_name]['commands'] = {}
                # Override existing commands
                for cmd_name, cmd_info in cat_data['commands'].items():
                    result['categories'][cat_name]['commands'][cmd_name] = cmd_info
    
    # Apply user custom commands (add new commands)
    if user_custom and 'categories' in user_custom:
        for cat_name, cat_data in user_custom['categories'].items():
            if cat_name not in result['categories']:
                result['categories'][cat_name] = {}
            if 'commands' in cat_data:
                if 'commands' not in result['categories'][cat_name]:
                    result['categories'][cat_name]['commands'] = {}
                # Add new commands (don't override if already exists from modified)
                for cmd_name, cmd_info in cat_data['commands'].items():
                    if cmd_name not in result['categories'][cat_name]['commands']:
                        result['categories'][cat_name]['commands'][cmd_name] = cmd_info
    
    return result

def get_all_commands(merged_data):
    """
    Extract all command names and their info into a flat dictionary.
    
    Args:
        merged_data (dict): Merged command data with categories
    
    Returns:
        dict: Flat dictionary of command_name -> {cmd, description, category}
    """
    all_commands = {}
    
    for cat_name, cat_data in merged_data.get('categories', {}).items():
        for cmd_name, cmd_info in cat_data.get('commands', {}).items():
            all_commands[cmd_name] = {
                'cmd': cmd_info.get('cmd', ''),
                'description': cmd_info.get('description', ''),
                'category': cat_data.get('name', cat_name),
                'args': cmd_info.get('args', 0)
            }
    
    return all_commands

def find_command(cmd_name, merged_data):
    """
    Search for a command by name in the merged data.
    
    Args:
        cmd_name (str): Command name to search for
        merged_data (dict): Merged command data with categories
    
    Returns:
        dict or None: Command info if found, None otherwise
    """
    for cat_name, cat_data in merged_data.get('categories', {}).items():
        for cmd, cmd_info in cat_data.get('commands', {}).items():
            if cmd == cmd_name:
                return cmd_info
    return None