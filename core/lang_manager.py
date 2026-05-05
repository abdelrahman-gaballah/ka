#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: lang_manager.py - Manage language files and translations
Author: Abdelrahman Gaballah
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

class LanguageManager:
    """
    Manage language files for Ka.
    """
    
    def __init__(self):
        """Initialize the language manager."""
        self.langs_dir = PROJECT_ROOT / "langs"
        self.available_langs = self._scan_available_languages()
    
    def _scan_available_languages(self) -> Dict[str, str]:
        """
        Scan the langs directory for available language files.
        
        Returns:
            Dictionary of language_code -> language_name
        """
        languages = {}
        
        if not self.langs_dir.exists():
            return languages
        
        for lang_file in self.langs_dir.glob("*.json"):
            if lang_file.name == "template.json":
                continue
            
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    name = data.get('name', lang_code)
                    languages[lang_code] = name
            except (json.JSONDecodeError, IOError):
                languages[lang_code] = lang_code
        
        return languages
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get the display name of a language.
        
        Args:
            lang_code: Language code
        
        Returns:
            Language display name
        """
        return self.available_langs.get(lang_code, lang_code)
    
    def get_current_language(self, config: Dict) -> str:
        """
        Get current language from config.
        
        Args:
            config: Configuration dictionary
        
        Returns:
            Current language code
        """
        lang = config.get('language', 'en')
        
        if lang not in self.available_langs:
            # Fallback to English if language not available
            return 'en'
        
        return lang
    
    def list_languages(self) -> List[Dict[str, str]]:
        """
        Get list of available languages.
        
        Returns:
            List of dictionaries with 'code' and 'name' keys
        """
        result = []
        for code, name in self.available_langs.items():
            result.append({'code': code, 'name': name})
        return result
    
    def load_language_file(self, lang_code: str) -> Dict:
        """
        Load a language file.
        
        Args:
            lang_code: Language code
        
        Returns:
            Language data dictionary
        """
        lang_path = self.langs_dir / f"{lang_code}.json"
        
        try:
            with open(lang_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def create_language_template(self, lang_code: str, lang_name: str) -> bool:
        """
        Create a new language file from template.
        
        Args:
            lang_code: Language code (e.g., 'fr', 'es')
            lang_name: Display name of the language
        
        Returns:
            True if successful, False otherwise
        """
        template_path = self.langs_dir / "template.json"
        
        if not template_path.exists():
            return False
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
        except (json.JSONDecodeError, IOError):
            return False
        
        # Update language info
        template['language'] = lang_code
        template['name'] = lang_name
        
        # Save new language file
        new_lang_path = self.langs_dir / f"{lang_code}.json"
        
        try:
            with open(new_lang_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def delete_language(self, lang_code: str) -> bool:
        """
        Delete a language file (user-added only).
        
        Args:
            lang_code: Language code to delete
        
        Returns:
            True if successful, False otherwise
        """
        # Don't allow deletion of built-in languages
        if lang_code in ['en', 'ar']:
            return False
        
        lang_path = self.langs_dir / f"{lang_code}.json"
        
        if not lang_path.exists():
            return False
        
        try:
            lang_path.unlink()
            return True
        except IOError:
            return False
    
    def get_command_translation(self, lang_code: str, command_name: str, field: str = 'cmd') -> Optional[str]:
        """
        Get translated command or description for a specific command.
        
        Args:
            lang_code: Language code
            command_name: Name of the command
            field: Field to retrieve ('cmd' or 'description')
        
        Returns:
            Translated value or None if not found
        """
        lang_data = self.load_language_file(lang_code)
        
        for category in lang_data.get('categories', {}).values():
            for cmd, cmd_data in category.get('commands', {}).items():
                if cmd == command_name:
                    return cmd_data.get(field)
        
        return None

def get_language_list() -> List[str]:
    """
    Quick helper to get list of available language codes.
    
    Returns:
        List of language codes
    """
    mgr = LanguageManager()
    return list(mgr.available_langs.keys())

def is_language_available(lang_code: str) -> bool:
    """
    Check if a language is available.
    
    Args:
        lang_code: Language code to check
    
    Returns:
        True if available, False otherwise
    """
    mgr = LanguageManager()
    return lang_code in mgr.available_langs