#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: discoverer.py - Discover installed programs and suggest shortcuts
Author: Abdelrahman Gaballah
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

class ProgramDiscoverer:
    """
    Discover installed programs on the system and suggest shortcuts.
    """
    
    def __init__(self):
        """Initialize the program discoverer."""
        self.discovered_dir = PROJECT_ROOT / "discovered"
        self.programs_path = self.discovered_dir / "programs.json"
        self.cache_path = self.discovered_dir / "cache.json"
        
        # Ensure discovered directory exists
        self.discovered_dir.mkdir(exist_ok=True)
        
        # Common programs that users might want shortcuts for
        self.common_programs = {
            'docker': {
                'check': 'docker --version',
                'suggestions': {
                    'docker ps': 'docker ps',
                    'docker stop': 'docker stop {}',
                    'docker start': 'docker start {}',
                    'docker rm': 'docker rm {}',
                    'docker images': 'docker images'
                }
            },
            'git': {
                'check': 'git --version',
                'suggestions': {
                    'git status': 'git status',
                    'git pull': 'git pull',
                    'git push': 'git push',
                    'git add': 'git add {}',
                    'git commit': 'git commit -m "{}"'
                }
            },
            'python3': {
                'check': 'python3 --version',
                'suggestions': {
                    'python run': 'python3 {}',
                    'python repl': 'python3'
                }
            },
            'node': {
                'check': 'node --version',
                'suggestions': {
                    'node run': 'node {}',
                    'npm install': 'npm install {}'
                }
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
                'suggestions': {
                    'download': 'curl -O {}',
                    'get': 'curl {}'
                }
            },
            'wget': {
                'check': 'wget --version',
                'suggestions': {
                    'wget download': 'wget {}',
                    'wget resume': 'wget -c {}'
                }
            },
            'ssh': {
                'check': 'ssh -V',
                'suggestions': {
                    'ssh connect': 'ssh {}@{}',
                    'ssh key': 'ssh-keygen -t rsa -b 4096'
                }
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
    
    def _run_check(self, command: str) -> bool:
        """
        Run a check command to see if a program is installed.
        
        Args:
            command: Command to run
        
        Returns:
            True if command succeeds, False otherwise
        """
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False
    
    def _scan_path_for_executables(self) -> Set[str]:
        """
        Scan PATH directories for executable files.
        
        Returns:
            Set of executable names found in PATH
        """
        executables = set()
        path_dirs = os.environ.get('PATH', '').split(':')
        
        for dir_path in path_dirs:
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
        """
        Discover installed programs on the system.
        
        Args:
            use_cache: If True, use cached results if available and recent
        
        Returns:
            Dictionary of discovered programs
        """
        # Check cache if enabled
        if use_cache and self.cache_path.exists():
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    # Cache valid for 1 day
                    if cache.get('timestamp', 0) > 0:
                        return cache.get('programs', {})
            except (json.JSONDecodeError, IOError):
                pass
        
        discovered = {}
        
        # Check common programs
        for prog_name, prog_info in self.common_programs.items():
            check_cmd = prog_info.get('check', '')
            if check_cmd and self._run_check(check_cmd):
                discovered[prog_name] = {
                    'installed': True,
                    'suggestions': prog_info.get('suggestions', {})
                }
            else:
                discovered[prog_name] = {
                    'installed': False,
                    'suggestions': {}
                }
        
        # Also scan PATH for other executables
        path_executables = self._scan_path_for_executables()
        
        # Add notable executables not in common list
        notable_programs = ['nvim', 'vim', 'nano', 'htop', 'btop', 'neofetch', 
                           'ranger', 'lf', 'yazi', 'zoxide', 'fzf', 'ripgrep', 'fd']
        
        for prog in notable_programs:
            if prog in path_executables and prog not in discovered:
                discovered[prog] = {
                    'installed': True,
                    'suggestions': {
                        f'{prog} run': prog,
                        f'{prog} help': f'{prog} --help'
                    }
                }
        
        # Save to cache
        cache_data = {
            'timestamp': int(Path.cwd().stat().st_ctime) if use_cache else 0,
            'programs': discovered
        }
        
        try:
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except IOError:
            pass
        
        return discovered
    
    def save_discovered_programs(self, discovered: Dict) -> bool:
        """
        Save discovered programs to programs.json.
        
        Args:
            discovered: Dictionary of discovered programs
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.programs_path, 'w', encoding='utf-8') as f:
                json.dump(discovered, f, indent=2)
            return True
        except IOError:
            return False
    
    def load_discovered_programs(self) -> Dict:
        """
        Load discovered programs from programs.json.
        
        Returns:
            Dictionary of discovered programs
        """
        if not self.programs_path.exists():
            return {}
        
        try:
            with open(self.programs_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def get_program_suggestions(self, program_name: str) -> Dict:
        """
        Get shortcut suggestions for a specific program.
        
        Args:
            program_name: Name of the program
        
        Returns:
            Dictionary of suggested shortcuts
        """
        discovered = self.load_discovered_programs()
        
        if program_name in discovered:
            return discovered[program_name].get('suggestions', {})
        
        return {}
    
    def refresh_discovery(self) -> Dict:
        """
        Force refresh of program discovery.
        
        Returns:
            Fresh dictionary of discovered programs
        """
        discovered = self.discover_installed_programs(use_cache=False)
        self.save_discovered_programs(discovered)
        return discovered
    
    def generate_shortcut_for_program(self, program_name: str, 
                                       shortcut_name: str, 
                                       cmd_template: str) -> Optional[str]:
        """
        Generate a ka shortcut for a discovered program.
        
        Args:
            program_name: Name of the program
            shortcut_name: Name of the shortcut to create
            cmd_template: Command template for the shortcut
        
        Returns:
            JSON string for adding to custom.json, or None if error
        """
        discovered = self.load_discovered_programs()
        
        if program_name not in discovered:
            return None
        
        if not discovered[program_name].get('installed', False):
            return None
        
        shortcut_entry = {
            "cmd": cmd_template,
            "description": f"Shortcut for {program_name}",
            "args": cmd_template.count('{}')
        }
        
        return json.dumps(shortcut_entry, indent=2)

def discover_system() -> Dict:
    """
    Quick helper to discover system programs.
    
    Returns:
        Dictionary of discovered programs
    """
    discoverer = ProgramDiscoverer()
    return discoverer.refresh_discovery()

def get_installed_programs_list() -> List[str]:
    """
    Quick helper to get list of installed program names.
    
    Returns:
        List of installed program names
    """
    discoverer = ProgramDiscoverer()
    discovered = discoverer.load_discovered_programs()
    
    installed = []
    for prog, info in discovered.items():
        if info.get('installed', False):
            installed.append(prog)
    
    return installed