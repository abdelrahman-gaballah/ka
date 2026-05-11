__version__ = '0.1.0'
__author__ = 'Abdelrahman Gaballah'
__description__ = 'Easy Linux Commands for beginners'

from core.loader import load_json_file, load_language, load_user_custom, \
    load_user_modified, merge_commands, get_all_commands, find_command
from core.parser import CommandParser, quick_parse, is_help_request, is_version_request
from core.executor import CommandExecutor, run_system_command, format_output
from core.formatter import OutputFormatter
from core.lang_manager import LanguageManager, get_language_list, is_language_available
from core.user_manager import UserManager, get_user_manager
from core.discoverer import ProgramDiscoverer, discover_system, get_installed_programs_list
from core.utils import get_project_root, ensure_dir, file_exists, read_file, write_file, \
    append_to_file, load_json_safe, save_json_safe, merge_dicts, get_timestamp, log_message, \
    run_command, is_command_available, get_shell, get_user_home, confirm_action, clear_screen, \
    print_colored, exit_with_error, exit_with_success, validate_command_name, get_version, get_ka_path
