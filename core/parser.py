import re
import shlex
from typing import Tuple, List, Optional, Dict


DANGEROUS_PATTERNS = [';', '&&', '||', '|', '`', '$(',
                      '${', '$[', '>>', '<<', '>', '<',
                      '&', '#', '!', '~']

SAFE_PATH_CHARS = set('/.:[]*?')

HELP_FLAGS = frozenset({'help', '-h', '--help', '-help', '?'})
VERSION_FLAGS = frozenset({'version', '-v', '--version', '-version'})


class CommandParser:
    def __init__(self):
        self.command_pattern = re.compile(r'^[a-zA-Z0-9_-]+$')
        self.arg_pattern = re.compile(r'^[a-zA-Z0-9_\-./\\:@]+$')

    def parse_input(self, args: List[str]) -> Tuple[Optional[str], List[str]]:
        if not args:
            return None, []
        return args[0].lower(), args[1:] if len(args) > 1 else []

    def validate_command_name(self, command_name: str) -> bool:
        return bool(command_name) and bool(self.command_pattern.match(command_name))

    def validate_arguments(self, arguments: List[str]) -> Tuple[bool, List[str]]:
        invalid_args = []
        for arg in arguments:
            if not arg:
                continue
            if self._is_dangerous_pattern(arg):
                invalid_args.append(arg)
                continue
            if self.arg_pattern.match(arg):
                continue
            if ' ' in arg:
                for part in arg.split():
                    if part and not self.arg_pattern.match(part) and not self._is_safe_special_char(part):
                        invalid_args.append(part)
            elif not self._is_safe_special_char(arg):
                invalid_args.append(arg)

        return len(invalid_args) == 0, invalid_args

    def _is_dangerous_pattern(self, text: str) -> bool:
        for pattern in DANGEROUS_PATTERNS:
            if pattern in text and pattern not in SAFE_PATH_CHARS:
                return True
        return False

    def _is_safe_special_char(self, text: str) -> bool:
        safe_chars = {'-', '_', '.', '/', ':', '@'}
        return all(c.isalnum() or c in safe_chars for c in text)

    def sanitize_argument(self, arg: str) -> str:
        result = arg
        for d in [';', '&&', '||', '|', '`', '$(', '>', '<', '>>', '<<']:
            result = result.replace(d, '')
        return result.strip()

    def check_argument_count(self, command_info: Dict, provided_args: List[str]) -> Tuple[bool, str]:
        required_args = command_info.get('args', 0)
        if required_args and len(provided_args) < required_args:
            return False, f"Missing arguments. Expected {required_args}, got {len(provided_args)}"
        return True, ""

    def extract_command_name(self, full_input: str) -> Optional[str]:
        try:
            parts = shlex.split(full_input)
        except ValueError:
            parts = full_input.split()
        return parts[0].lower() if parts else None


def quick_parse(args: List[str]) -> Tuple[Optional[str], List[str]]:
    return CommandParser().parse_input(args)


def is_help_request(command_name: str, args: List[str]) -> bool:
    if command_name in HELP_FLAGS:
        return True
    return any(arg in HELP_FLAGS for arg in args)


def is_version_request(command_name: str, args: List[str]) -> bool:
    if command_name in VERSION_FLAGS:
        return True
    return any(arg in VERSION_FLAGS for arg in args)
