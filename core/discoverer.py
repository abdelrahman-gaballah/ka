import os
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent.absolute()

_COMMON_PROGRAMS = {
    'docker': {
        'check': 'docker --version',
        'suggestions': {
            'docker ps': 'docker ps', 'docker stop': 'docker stop {}',
            'docker start': 'docker start {}', 'docker rm': 'docker rm {}',
            'docker images': 'docker images'
        }
    },
    'git': {
        'check': 'git --version',
        'suggestions': {
            'git status': 'git status', 'git pull': 'git pull',
            'git push': 'git push', 'git add': 'git add {}',
            'git commit': 'git commit -m "{}"'
        }
    },
    'python3': {
        'check': 'python3 --version',
        'suggestions': {'python run': 'python3 {}', 'python repl': 'python3'}
    },
    'node': {
        'check': 'node --version',
        'suggestions': {'node run': 'node {}', 'npm install': 'npm install {}'}
    },
    'ffmpeg': {
        'check': 'ffmpeg -version',
        'suggestions': {
            'convert video': 'ffmpeg -i {} {}.mp4',
            'extract audio': 'ffmpeg -i {} -q:a 0 -map a {}.mp3'
        }
    },
    'curl': {
        'check': 'curl --version',
        'suggestions': {'download': 'curl -O {}', 'get': 'curl {}'}
    },
    'wget': {
        'check': 'wget --version',
        'suggestions': {'wget download': 'wget {}', 'wget resume': 'wget -c {}'}
    },
    'ssh': {
        'check': 'ssh -V',
        'suggestions': {'ssh connect': 'ssh {}@{}', 'ssh key': 'ssh-keygen -t rsa -b 4096'}
    },
    'systemctl': {
        'check': 'systemctl --version',
        'suggestions': {
            'service start': 'sudo systemctl start {}',
            'service stop': 'sudo systemctl stop {}',
            'service status': 'systemctl status {}',
            'service enable': 'sudo systemctl enable {}'
        }
    }
}

_NOTABLE_PROGRAMS = ['nvim', 'vim', 'nano', 'htop', 'btop', 'neofetch',
                     'ranger', 'lf', 'yazi', 'zoxide', 'fzf', 'ripgrep', 'fd']

_CACHE_TTL = 86400


class ProgramDiscoverer:
    def __init__(self):
        self.discovered_dir = PROJECT_ROOT / "discovered"
        self.programs_path = self.discovered_dir / "programs.json"
        self.cache_path = self.discovered_dir / "cache.json"
        self.discovered_dir.mkdir(exist_ok=True)

    def _run_check(self, command: str) -> bool:
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False

    def _scan_path_for_executables(self) -> Set[str]:
        executables = set()
        for dir_path in os.environ.get('PATH', '').split(':'):
            path = Path(dir_path)
            if path.exists() and path.is_dir():
                try:
                    for item in path.iterdir():
                        if item.is_file() and os.access(item, os.X_OK):
                            executables.add(item.name)
                except (PermissionError, OSError):
                    continue
        return executables

    def discover_installed_programs(self, use_cache: bool = True) -> Dict:
        if use_cache and self.cache_path.exists():
            try:
                cache = json.loads(self.cache_path.read_text(encoding='utf-8'))
                if time.time() - cache.get('timestamp', 0) < _CACHE_TTL:
                    return cache.get('programs', {})
            except (json.JSONDecodeError, IOError):
                pass

        discovered = {}
        for prog_name, prog_info in _COMMON_PROGRAMS.items():
            check_cmd = prog_info.get('check', '')
            installed = bool(check_cmd and self._run_check(check_cmd))
            discovered[prog_name] = {
                'installed': installed,
                'suggestions': prog_info.get('suggestions', {}) if installed else {}
            }

        path_executables = self._scan_path_for_executables()
        for prog in _NOTABLE_PROGRAMS:
            if prog in path_executables and prog not in discovered:
                discovered[prog] = {
                    'installed': True,
                    'suggestions': {f'{prog} run': prog, f'{prog} help': f'{prog} --help'}
                }

        cache_data = {'timestamp': int(time.time()), 'programs': discovered}
        try:
            self.cache_path.write_text(json.dumps(cache_data, indent=2), encoding='utf-8')
            self.programs_path.write_text(json.dumps(discovered, indent=2), encoding='utf-8')
        except IOError:
            pass

        return discovered

    def save_discovered_programs(self, discovered: Dict) -> bool:
        try:
            self.programs_path.write_text(json.dumps(discovered, indent=2), encoding='utf-8')
            return True
        except IOError:
            return False

    def load_discovered_programs(self) -> Dict:
        if not self.programs_path.exists():
            return {}
        try:
            return json.loads(self.programs_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            return {}

    def get_program_suggestions(self, program_name: str) -> Dict:
        return self.load_discovered_programs().get(program_name, {}).get('suggestions', {})

    def refresh_discovery(self) -> Dict:
        discovered = self.discover_installed_programs(use_cache=False)
        self.save_discovered_programs(discovered)
        return discovered

    def generate_shortcut_for_program(self, program_name: str,
                                       shortcut_name: str,
                                       cmd_template: str) -> Optional[str]:
        discovered = self.load_discovered_programs()
        if not discovered.get(program_name, {}).get('installed', False):
            return None
        return json.dumps({
            "cmd": cmd_template,
            "description": f"Shortcut for {program_name}",
            "args": cmd_template.count('{}')
        }, indent=2)


def discover_system() -> Dict:
    return ProgramDiscoverer().refresh_discovery()


def get_installed_programs_list() -> List[str]:
    discoverer = ProgramDiscoverer()
    return [prog for prog, info in discoverer.load_discovered_programs().items()
            if info.get('installed', False)]
