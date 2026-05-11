import sys
import json
import shlex
import subprocess
from pathlib import Path
from core.loader import load_language, load_user_custom, load_user_modified, merge_commands, get_all_commands, resolve_command, suggest_commands, find_command
from core.executor import CommandExecutor
from core.formatter import OutputFormatter
from core.parser import is_help_request, is_version_request, CommandParser
from core.discoverer import ProgramDiscoverer

CONFIG_DIR = Path.home() / ".config/ka"
PROJECT_ROOT = Path(__file__).parent.parent.absolute()


def _first_existing(*paths):
    for p in paths:
        if p.exists():
            return p
    return paths[-1]


def load_config():
    path = _first_existing(CONFIG_DIR / "config.json", PROJECT_ROOT / "config.json")
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def show_help(merged):
    fmt = OutputFormatter()
    fmt.print_version("0.1.0")
    flat = get_all_commands(merged)
    by_cat = {}
    for name, info in flat.items():
        cat = info.get('category', 'Other')
        by_cat.setdefault(cat, {})[name] = info
    if by_cat:
        fmt.print_help_table(by_cat)
    else:
        print("No commands available. Check your language files.")


def _is_rm(template: str) -> bool:
    executable = shlex.split(template)[0] if template else ""
    return Path(executable).name == "rm"


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: ka <command> [arguments]")
        print("       ka help     - Show all commands")
        print("       ka version  - Show version info")
        sys.exit(0)

    cmd = args[0]
    cmd_args = args[1:]

    if is_version_request(cmd, cmd_args):
        OutputFormatter().print_version("0.1.0")
        return

    config = load_config()
    lang = config.get("language", "en")
    timeout = config.get("default_timeout", 30)
    auto_discover = config.get("auto_discover", False)

    lang_path = _first_existing(
        CONFIG_DIR / "langs" / f"{lang}.json",
        PROJECT_ROOT / "langs" / f"{lang}.json"
    )
    lang_data = {}
    if lang_path.exists():
        with open(lang_path) as f:
            lang_data = json.load(f)

    user_data = load_user_custom()
    modified_data = load_user_modified()
    merged = merge_commands(lang_data, user_data, modified_data)

    if auto_discover:
        discoverer = ProgramDiscoverer()
        discovered = discoverer.discover_installed_programs()
        for prog_name, prog_info in discovered.items():
            if not prog_info.get('installed'):
                continue
            suggestions = prog_info.get('suggestions', {})
            if suggestions:
                disc_cat = merged.setdefault('categories', {}).setdefault('_discovered', {
                    'name': 'Discovered', 'commands': {}
                })
                for sname, scmd in suggestions.items():
                    if not find_command(sname, merged):
                        disc_cat['commands'][sname] = {
                            'cmd': scmd, 'description': f"via {prog_name}",
                            'args': scmd.count('{}')
                        }

    if is_help_request(cmd, cmd_args):
        show_help(merged)
        return

    resolved_cmd, resolved_args = resolve_command([cmd] + cmd_args, merged)
    cmd_info = find_command(resolved_cmd, merged)

    if not cmd_info:
        fmt = OutputFormatter()
        fmt.print_error(f"Command '{cmd}' not found")
        suggestions = suggest_commands(cmd, merged)
        if suggestions:
            print(f"Did you mean: {', '.join(suggestions)}?")
        print("Try 'ka help' to see available commands")
        sys.exit(1)

    template = cmd_info.get('cmd', '')
    if not template:
        OutputFormatter().print_error(f"Command '{resolved_cmd}' has no executable template")
        sys.exit(1)

    parser = CommandParser()
    valid, invalid = parser.validate_arguments(resolved_args)
    if not valid:
        OutputFormatter().print_error(f"Dangerous arguments detected: {', '.join(invalid)}")
        sys.exit(1)

    if _is_rm(template) and config.get("confirm_dangerous", True):
        try:
            reply = input("Are you sure you want to delete? (y/N): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(1)
        if reply != 'y':
            print("Cancelled.")
            sys.exit(0)

    executor = CommandExecutor(timeout=timeout)
    success, output = executor.execute_with_template(template, resolved_args)

    if not success and "\nInstall: " in output:
        install_cmd = output.split("\nInstall: ", 1)[1].split("\n")[0].strip()
        print(output.split("\n")[0])
        try:
            reply = input(f"Install with '{install_cmd}'? (y/N): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(1)
        if reply == 'y':
            subprocess.run(shlex.split(install_cmd))
            success, output = executor.execute_with_template(template, resolved_args)

    if output:
        print(output)
    sys.exit(0 if success else 1)
