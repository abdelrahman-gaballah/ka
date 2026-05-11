import json
import difflib
import copy
from pathlib import Path
from typing import Dict, Optional, List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
CONFIG_DIR = Path.home() / ".config/ka"


def load_json_file(file_path: Path) -> Dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_language(lang_code: str) -> Dict:
    return load_json_file(PROJECT_ROOT / "langs" / f"{lang_code}.json")


def _first_existing(*paths):
    for p in paths:
        if p.exists():
            return p
    return paths[-1]


def load_user_custom() -> Dict:
    path = _first_existing(CONFIG_DIR / "user" / "custom.json", PROJECT_ROOT / "user" / "custom.json")
    return load_json_file(path)


def load_user_modified() -> Dict:
    path = _first_existing(CONFIG_DIR / "user" / "modified.json", PROJECT_ROOT / "user" / "modified.json")
    return load_json_file(path)


def _apply_commands(target: Dict, source: Dict, override: bool) -> None:
    if not source or 'categories' not in source:
        return
    target_cats = target.setdefault('categories', {})
    for cat_name, cat_data in source['categories'].items():
        if cat_name not in target_cats:
            target_cats[cat_name] = {}
        for key, value in cat_data.items():
            if key != 'commands':
                target_cats[cat_name][key] = value
        if 'commands' not in cat_data:
            continue
        target_cmds = target_cats[cat_name].setdefault('commands', {})
        for cmd_name, cmd_info in cat_data['commands'].items():
            if override or cmd_name not in target_cmds:
                target_cmds[cmd_name] = copy.deepcopy(cmd_info)


def merge_commands(lang_data: Dict, user_custom: Dict, user_modified: Dict) -> Dict:
    result = copy.deepcopy(lang_data) if lang_data else {}
    if 'categories' not in result:
        result['categories'] = {}

    _apply_commands(result, user_modified, override=True)
    _apply_commands(result, user_custom, override=False)
    return result


def get_all_commands(merged_data: Dict) -> Dict:
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


def find_command(cmd_name: str, merged_data: Dict) -> Optional[Dict]:
    for cat_data in merged_data.get('categories', {}).values():
        for cmd, cmd_info in cat_data.get('commands', {}).items():
            if cmd == cmd_name:
                return cmd_info
    return None


def resolve_command(args: List[str], merged_data: Dict) -> Tuple[str, List[str]]:
    for n in range(min(len(args), 3), 0, -1):
        candidate = " ".join(args[:n])
        if find_command(candidate, merged_data) is not None:
            return candidate, args[n:]
    return args[0], args[1:]


def suggest_commands(cmd_name: str, merged_data: Dict, n: int = 3, cutoff: float = 0.5) -> List[str]:
    all_names = []
    for cat_data in merged_data.get('categories', {}).values():
        all_names.extend(cat_data.get('commands', {}).keys())
    return difflib.get_close_matches(cmd_name, all_names, n=n, cutoff=cutoff)
