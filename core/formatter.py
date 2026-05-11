import re
from typing import Dict, Optional

_KA_LOGO = """
░██                     
░██                     
░██    ░██    ░██████   
░██   ░██          ░██  
░███████      ░███████  
░██   ░██    ░██   ░██  
░██    ░██    ░█████░██ 
"""

_COLORS = {
    'reset': '\033[0m', 'bold': '\033[1m', 'dim': '\033[2m',
    'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m',
    'blue': '\033[34m', 'magenta': '\033[35m', 'cyan': '\033[36m',
    'white': '\033[37m',
}


class OutputFormatter:
    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors

    def _c(self, text: str, color: str) -> str:
        if not self.use_colors:
            return text
        return f"{_COLORS.get(color, _COLORS['reset'])}{text}{_COLORS['reset']}"

    def print_header(self, title: str):
        print(self._c(f"\n{title}", 'cyan'))
        print(self._c("-" * 40, 'dim'))

    def print_success(self, message: str):
        print(self._c(message, 'green'))

    def print_error(self, message: str):
        print(self._c(message, 'red'))

    def print_warning(self, message: str):
        print(self._c(message, 'yellow'))

    def print_info(self, message: str):
        print(self._c(message, 'blue'))

    def print_command_list(self, commands: Dict, category: Optional[str] = None):
        if category:
            print(self._c(category + ":", 'magenta'))
        for cmd_name, cmd_info in commands.items():
            desc = cmd_info.get('description', 'No description')
            print(f"   {self._c(cmd_name, 'green')} - {desc}")

    @staticmethod
    def _visible_len(s: str) -> int:
        return len(re.sub(r'\033\[[0-9;]*m', '', s))

    def print_help_table(self, commands_by_category: Dict):
        self.print_header("AVAILABLE COMMANDS")
        for category, commands in commands_by_category.items():
            print(self._c(category + ":", 'yellow'))
            for cmd_name, cmd_info in commands.items():
                desc = cmd_info.get('description', '')
                needs_arg = " [arg]" if cmd_info.get('args', 0) > 0 else ""
                display = cmd_name + needs_arg
                visible = self._visible_len(display)
                padding = max(2, 22 - visible)
                print(f"  {self._c(display, 'green')}{' ' * padding} - {desc}")

    def print_version(self, version: str, name: str = "Ka"):
        if self.use_colors:
            print(self._c(_KA_LOGO, 'cyan'))
        else:
            print(_KA_LOGO)
        print(self._c(f"{name} - Easy Linux Commands", 'bold'))
        print(self._c(f"Version {version}", 'dim'))

    def print_command_result(self, stdout: str, stderr: str, max_lines: int = 50):
        if stdout:
            lines = stdout.split('\n')
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                lines.append(self._c(f"... (truncated)", 'dim'))
            print('\n'.join(lines))
        if stderr:
            print(self._c(stderr, 'red'))

    def format_command_not_found(self, command: str):
        self.print_error(f"Command '{command}' not found")
        print(self._c("Try 'ka help' to see available commands", 'dim'))



