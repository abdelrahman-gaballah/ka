import os
import subprocess
import shlex
import shutil
from pathlib import Path
from typing import List, Tuple, Optional

SUDO_COMMANDS = frozenset({
    'apt', 'apt-get', 'dpkg', 'systemctl', 'service',
    'mount', 'umount', 'fdisk', 'mkfs',
    'chown', 'chmod', 'useradd', 'userdel', 'passwd',
    'modprobe', 'insmod', 'rmmod',
    'shutdown', 'reboot', 'halt', 'poweroff',
    'ufw', 'smartctl', 'sensors'
})

INTERACTIVE_COMMANDS = frozenset({
    'top', 'htop', 'nano', 'vim', 'vi', 'less', 'more',
    'btop', 'ranger', 'lf'
})

_INSTALL_HINTS = {
    'cal': 'sudo apt install bsdmainutils',
    'xclip': 'sudo apt install xclip',
    'docker': 'sudo apt install docker.io',
    'speedtest-cli': 'sudo apt install speedtest-cli',
    'trans': 'sudo apt install translate-shell',
    'sensors': 'sudo apt install lm-sensors',
    'upower': 'sudo apt install upower',
    'nmcli': 'sudo apt install network-manager',
    'xdg-open': 'sudo apt install xdg-utils',
    'gnome-screenshot': 'sudo apt install gnome-screenshot',
    'pactl': 'sudo apt install pulseaudio-utils',
    'brightnessctl': 'sudo apt install brightnessctl',
    'htop': 'sudo apt install htop',
    'btop': 'sudo snap install btop',
    'make': 'sudo apt install build-essential',
}

_SHELL_OPS = ('&&', '||', '|', '>', '<', '>>', '<<', ';', '$(')


def _needs_shell(template: str) -> bool:
    for op in _SHELL_OPS:
        if op in template:
            return True
    return False


def _first_cmd(template: str) -> str:
    return shlex.split(template)[0] if template else ""


def _needs_interactive(template: str) -> bool:
    return Path(_first_cmd(template)).name in INTERACTIVE_COMMANDS


def _needs_sudo(template: str) -> bool:
    parts = shlex.split(template) if template else []
    return bool(parts) and parts[0] in SUDO_COMMANDS


def _make_shell_cmd(template: str, args: List[str]) -> str:
    cmd = template
    for a in args:
        if '{}' in cmd:
            cmd = cmd.replace('{}', shlex.quote(a), 1)
    return cmd


def _make_list_cmd(template: str, args: List[str]) -> Tuple[Optional[List[str]], str]:
    try:
        parts = shlex.split(template)
    except ValueError as e:
        return None, f"Invalid command template: {e}"
    result: List[str] = []
    arg_idx = 0
    for part in parts:
        while '{}' in part:
            if arg_idx >= len(args):
                return None, f"Missing argument for '{{}}'"
            part = part.replace('{}', args[arg_idx], 1)
            arg_idx += 1
        result.append(part)
    result.extend(args[arg_idx:])
    return result, ""


def _hint(cmd_name: str) -> str:
    hint = _INSTALL_HINTS.get(cmd_name)
    return f"\nInstall: {hint}" if hint else ""


def _safe_exec(cmd, shell: bool = False, interactive: bool = False, timeout: int = 30) -> Tuple[bool, str]:
    try:
        if shell and not interactive:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return result.returncode == 0, (result.stdout + result.stderr).strip()
        if shell:
            subprocess.run(cmd, shell=True, timeout=timeout)
            return True, ""
        if interactive:
            subprocess.run(cmd, timeout=timeout)
            return True, ""
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, (result.stdout + result.stderr).strip()
    except FileNotFoundError:
        name = cmd[0] if isinstance(cmd, list) else cmd.split()[0]
        return False, f"Command not found: {name}{_hint(name)}"
    except PermissionError:
        return False, "Permission denied. Try running with sudo."
    except OSError as e:
        return False, str(e)


class CommandExecutor:
    def __init__(self, dry_run: bool = False, timeout: int = 30):
        self.dry_run = dry_run
        self.timeout = timeout

    def check_sudo_needed(self, cmd_parts: List[str]) -> bool:
        return bool(cmd_parts) and cmd_parts[0] in SUDO_COMMANDS

    def build_command(self, cmd_template: str, args: List[str]) -> Tuple[Optional[List[str]], str]:
        return _make_list_cmd(cmd_template, args)

    def execute_with_template(self, cmd_template: str, args: List[str]) -> Tuple[bool, str]:
        shell = _needs_shell(cmd_template)
        interactive = _needs_interactive(cmd_template)
        sudo = _needs_sudo(cmd_template)

        if shell:
            cmd_str = _make_shell_cmd(cmd_template, args)
            if sudo:
                cmd_str = shlex.quote(cmd_str)
                cmd_str = f"sudo sh -c {cmd_str}"
            if self.dry_run:
                print(f"[DRY RUN] {cmd_str}")
                return True, ""
            return _safe_exec(cmd_str, shell=True, interactive=interactive, timeout=self.timeout)

        cmd_list, error = _make_list_cmd(cmd_template, args)
        if error:
            return False, error
        if sudo:
            cmd_list = ['sudo'] + cmd_list
        if self.dry_run:
            print(f"[DRY RUN] {' '.join(cmd_list)}")
            return True, ""
        return _safe_exec(cmd_list, interactive=interactive, timeout=self.timeout)


def run_system_command(command: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds"
    except FileNotFoundError:
        return -1, "", f"Command not found: {command[0] if command else ''}"
    except PermissionError:
        return -1, "", "Permission denied"


def format_output(stdout: str, stderr: str, max_lines: int = 50) -> str:
    output = ""
    if stdout:
        lines = stdout.split('\n')
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines.append("... (output truncated)")
        output += '\n'.join(lines)
    if stderr:
        if output:
            output += '\n'
        output += f"[STDERR]\n{stderr}"
    return output.strip()
