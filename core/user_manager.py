import re
from pathlib import Path
from typing import Dict, Tuple

from core.utils import load_json_safe, save_json_safe

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
_CMD_RE = re.compile(r'^[a-zA-Z0-9_-]+$')


class UserManager:
    def __init__(self):
        self.user_dir = PROJECT_ROOT / "user"
        self.custom_path = self.user_dir / "custom.json"
        self.modified_path = self.user_dir / "modified.json"
        self.aliases_path = self.user_dir / "aliases.json"
        self.user_dir.mkdir(exist_ok=True)

    def load_custom_commands(self) -> Dict:
        return load_json_safe(self.custom_path)

    def load_modified_commands(self) -> Dict:
        return load_json_safe(self.modified_path)

    def load_aliases(self) -> Dict:
        return load_json_safe(self.aliases_path)

    def add_custom_command(self, command_name: str, cmd_template: str,
                           description: str, category: str = "custom") -> Tuple[bool, str]:
        if not command_name or not _CMD_RE.match(command_name):
            return False, "Command name must contain only letters, numbers, hyphens, and underscores"
        custom_data = self.load_custom_commands()
        if 'categories' not in custom_data:
            custom_data['categories'] = {}
        if category not in custom_data['categories']:
            custom_data['categories'][category] = {'name': category.capitalize(), 'commands': {}}
        if command_name in custom_data['categories'][category].get('commands', {}):
            return False, f"Command '{command_name}' already exists in category '{category}'"
        custom_data['categories'][category].setdefault('commands', {})
        custom_data['categories'][category]['commands'][command_name] = {
            'cmd': cmd_template, 'description': description, 'args': cmd_template.count('{}')
        }
        if save_json_safe(self.custom_path, custom_data):
            return True, f"Command '{command_name}' added successfully"
        return False, "Failed to save custom command"

    def remove_custom_command(self, command_name: str) -> Tuple[bool, str]:
        return self._remove_from(command_name, self.custom_path, "custom")

    def modify_builtin_command(self, command_name: str, new_cmd_template: str,
                               new_description: str, category: str) -> Tuple[bool, str]:
        modified_data = self.load_modified_commands()
        if 'categories' not in modified_data:
            modified_data['categories'] = {}
        if category not in modified_data['categories']:
            modified_data['categories'][category] = {'name': category.capitalize(), 'commands': {}}
        modified_data['categories'][category].setdefault('commands', {})
        modified_data['categories'][category]['commands'][command_name] = {
            'cmd': new_cmd_template, 'description': new_description, 'args': new_cmd_template.count('{}')
        }
        if save_json_safe(self.modified_path, modified_data):
            return True, f"Command '{command_name}' modified successfully"
        return False, "Failed to save modification"

    def remove_modification(self, command_name: str) -> Tuple[bool, str]:
        return self._remove_from(command_name, self.modified_path, "modification")

    def _remove_from(self, command_name: str, file_path: Path, kind: str) -> Tuple[bool, str]:
        data = load_json_safe(file_path)
        for category, cat_data in data.get('categories', {}).items():
            if command_name in cat_data.get('commands', {}):
                del cat_data['commands'][command_name]
                if not cat_data['commands']:
                    del data['categories'][category]
                if save_json_safe(file_path, data):
                    return True, f"Command '{command_name}' removed from {kind}"
                return False, "Failed to save changes"
        return (False, f"Command '{command_name}' not found in {kind}") if kind != "custom" \
            else (False, f"Command '{command_name}' not found")

    def add_alias(self, alias_name: str, actual_command: str) -> Tuple[bool, str]:
        if not alias_name or not _CMD_RE.match(alias_name):
            return False, "Alias name must contain only letters, numbers, hyphens, and underscores"
        aliases = self.load_aliases()
        if alias_name in aliases:
            return False, f"Alias '{alias_name}' already exists"
        aliases[alias_name] = actual_command
        if save_json_safe(self.aliases_path, aliases):
            return True, f"Alias '{alias_name}' added successfully"
        return False, "Failed to save alias"

    def list_all_user_commands(self) -> Dict:
        result = {}
        custom = self.load_custom_commands()
        for category, cat_data in custom.get('categories', {}).items():
            for cmd_name, cmd_info in cat_data.get('commands', {}).items():
                result[cmd_name] = {**cmd_info, 'source': 'custom', 'category': category}
        modified = self.load_modified_commands()
        for category, cat_data in modified.get('categories', {}).items():
            for cmd_name, cmd_info in cat_data.get('commands', {}).items():
                result[cmd_name] = {**cmd_info, 'source': 'modified', 'category': category}
        return result


def get_user_manager() -> UserManager:
    return UserManager()
