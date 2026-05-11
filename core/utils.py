import os
import sys
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent.absolute()


def get_project_root() -> Path:
    return PROJECT_ROOT


def ensure_dir(directory: Path) -> bool:
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except (PermissionError, OSError):
        return False


def file_exists(file_path: Path) -> bool:
    return file_path.exists() and file_path.is_file()


def read_file(file_path: Path) -> Optional[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (IOError, UnicodeDecodeError):
        return None


def write_file(file_path: Path, content: str) -> bool:
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError:
        return False


def append_to_file(file_path: Path, content: str) -> bool:
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError:
        return False


def load_json_safe(file_path: Path) -> Dict:
    if not file_exists(file_path):
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_json_safe(file_path: Path, data: Dict) -> bool:
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, TypeError):
        return False


def merge_dicts(base: Dict, override: Dict) -> Dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_message(message: str, level: str = "INFO", log_file: str = "ka.log") -> None:
    log_dir = Path.home() / ".config/ka" / "logs"
    log_path = log_dir / log_file
    ensure_dir(log_dir)
    append_to_file(log_path, f"[{get_timestamp()}] [{level}] {message}\n")


def run_command(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0] if cmd else ''}"
    except (PermissionError, OSError) as e:
        return -1, "", str(e)


def is_command_available(command: str) -> bool:
    return shutil.which(command) is not None


def get_shell() -> str:
    return os.environ.get('SHELL') or shutil.which('bash') or '/bin/sh'


def get_user_home() -> Path:
    return Path.home()


def confirm_action(prompt: str, default: bool = False) -> bool:
    suffix = " [Y/n]: " if default else " [y/N]: "
    try:
        response = input(prompt + suffix).strip().lower()
    except (KeyboardInterrupt, EOFError):
        return False
    if default:
        return response != 'n' and response != 'no'
    return response == 'y' or response == 'yes'


def clear_screen() -> None:
    subprocess.run(['clear'] if os.name == 'posix' else ['cls'])


_COLORS = {
    'reset': '\033[0m', 'bold': '\033[1m', 'dim': '\033[2m',
    'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m',
    'blue': '\033[34m', 'magenta': '\033[35m', 'cyan': '\033[36m',
    'white': '\033[37m',
}


def print_colored(text: str, color: str = "reset") -> None:
    print(f"{_COLORS.get(color, _COLORS['reset'])}{text}{_COLORS['reset']}")


def exit_with_error(message: str, code: int = 1) -> None:
    print_colored(f"Error: {message}", "red")
    sys.exit(code)


def exit_with_success(message: str, code: int = 0) -> None:
    print_colored(f"\u2713 {message}", "green")
    sys.exit(code)


def validate_command_name(name: str) -> bool:
    if not name or len(name) > 50:
        return False
    allowed = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_')
    return all(c in allowed for c in name)


def get_version() -> str:
    return "0.1.0"


def get_ka_path() -> Optional[Path]:
    ka_path = PROJECT_ROOT / "ka"
    if ka_path.exists() and os.access(ka_path, os.X_OK):
        return ka_path
    path_ka = shutil.which("ka")
    return Path(path_ka) if path_ka else None
