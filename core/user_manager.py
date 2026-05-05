#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: user_manager.py - Manage user custom commands and modifications
Author: Abdelrahman Gaballah
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

class UserManager:
    """
    Manage user custom commands and modifications.
    """
    
    def __init__(self):
        """Initialize the user manager."""
        self.user_dir = PROJECT_ROOT / "user"
        self.custom_path = self.user_dir / "custom.json"
        self.modified_path = self.user_dir / "modified.json"
        self.aliases_path = self.user_dir / "aliases.json"
        
        # Ensure user directory exists
        self.user_dir.mkdir(exist_ok=True)
    
    def _load_json_file(self, file_path: Path) -> Dict:
        """
        Load a JSON file safely.
        
        Args:
            file_path: Path to JSON file
        
        Returns:
            Dictionary content or empty dict if error
        """
        if not file_path.exists():
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_json_file(self, file_path: Path, data: Dict) -> bool:
        """
        Save data to a JSON file.
        
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
        except IOError:
            return False
    
    def load_custom_commands(self) -> Dict:
        """
        Load user custom commands from custom.json.
        
        Returns:
            Dictionary of custom commands
        """
        return self._load_json_file(self.custom_path)
    
    def load_modified_commands(self) -> Dict:
        """
        Load user modified commands from modified.json.
        
        Returns:
            Dictionary of modified commands
        """
        return self._load_json_file(self.modified_path)
    
    def load_aliases(self) -> Dict:
        """
        Load user aliases from aliases.json.
        
        Returns:
            Dictionary of aliases
        """
        return self._load_json_file(self.aliases_path)
    
    def add_custom_command(self, command_name: str, cmd_template: str, 
                          description: str, category: str = "custom") -> Tuple[bool, str]:
        """
        Add a new custom command.
        
        Args:
            command_name: Name of the command
            cmd_template: Command template with {} placeholders
            description: Description of the command
            category: Category name for the command
        
        Returns:
            Tuple of (success, message)
        """
        # Validate command name
        if not command_name or not command_name.isalnum():
            return False, "Command name must be alphanumeric"
        
        # Load existing custom commands
        custom_data = self.load_custom_commands()
        
        # Ensure categories structure exists
        if 'categories' not in custom_data:
            custom_data['categories'] = {}
        
        if category not in custom_data['categories']:
            custom_data['categories'][category] = {
                'name': category.capitalize(),
                'commands': {}
            }
        
        # Check if command already exists
        if command_name in custom_data['categories'][category].get('commands', {}):
            return False, f"Command '{command_name}' already exists in category '{category}'"
        
        # Add the command
        if 'commands' not in custom_data['categories'][category]:
            custom_data['categories'][category]['commands'] = {}
        
        custom_data['categories'][category]['commands'][command_name] = {
            'cmd': cmd_template,
            'description': description,
            'args': cmd_template.count('{}')
        }
        
        # Save to file
        if self._save_json_file(self.custom_path, custom_data):
            return True, f"Command '{command_name}' added successfully"
        else:
            return False, "Failed to save custom command"
    
    def remove_custom_command(self, command_name: str) -> Tuple[bool, str]:
        """
        Remove a custom command.
        
        Args:
            command_name: Name of the command to remove
        
        Returns:
            Tuple of (success, message)
        """
        custom_data = self.load_custom_commands()
        
        for category, cat_data in custom_data.get('categories', {}).items():
            if command_name in cat_data.get('commands', {}):
                del cat_data['commands'][command_name]
                
                # Remove category if empty
                if not cat_data['commands']:
                    del custom_data['categories'][category]
                
                if self._save_json_file(self.custom_path, custom_data):
                    return True, f"Command '{command_name}' removed successfully"
                else:
                    return False, "Failed to save changes"
        
        return False, f"Command '{command_name}' not found"
    
    def modify_builtin_command(self, command_name: str, new_cmd_template: str,
                               new_description: str, category: str) -> Tuple[bool, str]:
        """
        Override a built-in command with user modification.
        
        Args:
            command_name: Name of the command to modify
            new_cmd_template: New command template
            new_description: New description
            category: Category of the built-in command
        
        Returns:
            Tuple of (success, message)
        """
        modified_data = self.load_modified_commands()
        
        if 'categories' not in modified_data:
            modified_data['categories'] = {}
        
        if category not in modified_data['categories']:
            modified_data['categories'][category] = {
                'name': category.capitalize(),
                'commands': {}
            }
        
        if 'commands' not in modified_data['categories'][category]:
            modified_data['categories'][category]['commands'] = {}
        
        modified_data['categories'][category]['commands'][command_name] = {
            'cmd': new_cmd_template,
            'description': new_description,
            'args': new_cmd_template.count('{}')
        }
        
        if self._save_json_file(self.modified_path, modified_data):
            return True, f"Command '{command_name}' modified successfully"
        else:
            return False, "Failed to save modification"
    
    def remove_modification(self, command_name: str) -> Tuple[bool, str]:
        """
        Remove a user modification (revert to built-in).
        
        Args:
            command_name: Name of the command to revert
        
        Returns:
            Tuple of (success, message)
        """
        modified_data = self.load_modified_commands()
        
        for category, cat_data in modified_data.get('categories', {}).items():
            if command_name in cat_data.get('commands', {}):
                del cat_data['commands'][command_name]
                
                if self._save_json_file(self.modified_path, modified_data):
                    return True, f"Command '{command_name}' reverted to built-in"
                else:
                    return False, "Failed to save changes"
        
        return False, f"Command '{command_name}' has no modification"
    
    def add_alias(self, alias_name: str, actual_command: str) -> Tuple[bool, str]:
        """
        Add a shell alias.
        
        Args:
            alias_name: Name of the alias
            actual_command: Command that alias points to
        
        Returns:
            Tuple of (success, message)
        """
        if not alias_name or not alias_name.isalnum():
            return False, "Alias name must be alphanumeric"
        
        aliases = self.load_aliases()
        
        if alias_name in aliases:
            return False, f"Alias '{alias_name}' already exists"
        
        aliases[alias_name] = actual_command
        
        if self._save_json_file(self.aliases_path, aliases):
            return True, f"Alias '{alias_name}' added successfully"
        else:
            return False, "Failed to save alias"
    
    def list_all_user_commands(self) -> Dict:
        """
        Get all user commands (custom + modified) in a flat structure.
        
        Returns:
            Dictionary of all user commands with their info
        """
        result = {}
        
        # Add custom commands
        custom = self.load_custom_commands()
        for category, cat_data in custom.get('categories', {}).items():
            for cmd_name, cmd_info in cat_data.get('commands', {}).items():
                result[cmd_name] = {
                    **cmd_info,
                    'source': 'custom',
                    'category': category
                }
        
        # Add modified commands (these override, so add last)
        modified = self.load_modified_commands()
        for category, cat_data in modified.get('categories', {}).items():
            for cmd_name, cmd_info in cat_data.get('commands', {}).items():
                result[cmd_name] = {
                    **cmd_info,
                    'source': 'modified',
                    'category': category
                }
        
        return result

def get_user_manager() -> UserManager:
    """
    Quick helper to get UserManager instance.
    
    Returns:
        UserManager instance
    """
    return UserManager()