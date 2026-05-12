#!/usr/bin/env python3

# Author: Abdelrahman Gaballah

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.loader import (
    load_json_file,
    load_language,
    load_user_custom,
    load_user_modified,
    merge_commands,
    get_all_commands,
    find_command
)

class TestLoader(unittest.TestCase):

    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(self.temp_dir)
        
        (self.project_root / "langs").mkdir()
        (self.project_root / "user").mkdir()
        
        # Mock the PROJECT_ROOT and CONFIG_DIR in loader
        self.mock_root_patcher = patch('core.loader.PROJECT_ROOT', self.project_root)
        self.mock_root = self.mock_root_patcher.start()
        self.mock_config_patcher = patch('core.loader.CONFIG_DIR', self.project_root)
        self.mock_config = self.mock_config_patcher.start()
        
        self.valid_lang_data = {
            "language": "en",
            "name": "English",
            "categories": {
                "system": {
                    "name": "System Info",
                    "commands": {
                        "space": {"cmd": "df -h", "description": "Disk space", "args": 0},
                        "ram": {"cmd": "free -h", "description": "RAM usage", "args": 0}
                    }
                },
                "network": {
                    "name": "Network",
                    "commands": {
                        "ip": {"cmd": "ip a", "description": "IP address", "args": 0},
                        "ping": {"cmd": "ping -c 4 {}", "description": "Ping host", "args": 1}
                    }
                }
            }
        }
        
        self.user_custom_data = {
            "categories": {
                "my_commands": {
                    "name": "My Commands",
                    "commands": {
                        "mybackup": {"cmd": "rsync -av", "description": "Backup files", "args": 2},
                        "myclean": {"cmd": "sudo apt autoremove", "description": "Clean system", "args": 0}
                    }
                }
            }
        }
        
        self.user_modified_data = {
            "categories": {
                "system": {
                    "commands": {
                        "space": {"cmd": "df -h --total", "description": "Total disk space", "args": 0}
                    }
                }
            }
        }
    
    def tearDown(self):
        self.mock_root_patcher.stop()
        self.mock_config_patcher.stop()
        shutil.rmtree(self.temp_dir)
    
    def test_load_json_file_exists(self):
        test_file = self.project_root / "test.json"
        test_data = {"key": "value", "number": 42, "nested": {"inner": "data"}}
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        result = load_json_file(test_file)
        self.assertEqual(result, test_data)
        self.assertEqual(result["key"], "value")
        self.assertEqual(result["nested"]["inner"], "data")
    
    def test_load_json_file_not_exists(self):
        test_file = self.project_root / "nonexistent.json"
        result = load_json_file(test_file)
        self.assertEqual(result, {})
    
    def test_load_json_file_invalid_json(self):
        test_file = self.project_root / "invalid.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("{invalid json content without proper format")
        
        result = load_json_file(test_file)
        self.assertEqual(result, {})
    
    def test_load_json_file_empty_file(self):
        test_file = self.project_root / "empty.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        result = load_json_file(test_file)
        self.assertEqual(result, {})
    
    def test_load_language_exists(self):
        lang_file = self.project_root / "langs" / "en.json"
        
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(self.valid_lang_data, f)
        
        result = load_language("en")
        self.assertEqual(result, self.valid_lang_data)
        self.assertEqual(result["language"], "en")
        self.assertEqual(result["name"], "English")
        self.assertIn("system", result["categories"])
        self.assertIn("space", result["categories"]["system"]["commands"])
    
    def test_load_language_not_exists(self):
        result = load_language("nonexistent_language_xyz")
        self.assertEqual(result, {})
    
    def test_load_language_with_special_chars(self):
        lang_file = self.project_root / "langs" / "ar.json"
        arabic_data = {
            "language": "ar",
            "name": "العربية",
            "categories": {
                "system": {
                    "name": "معلومات النظام",
                    "commands": {
                        "space": {"cmd": "df -h", "description": "مساحة التخزين", "args": 0}
                    }
                }
            }
        }
        
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(arabic_data, f, ensure_ascii=False)
        
        result = load_language("ar")
        self.assertEqual(result["name"], "العربية")
        self.assertEqual(result["categories"]["system"]["name"], "معلومات النظام")
    
    def test_load_user_custom_exists(self):
        custom_file = self.project_root / "user" / "custom.json"
        
        with open(custom_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_custom_data, f)
        
        result = load_user_custom()
        self.assertEqual(result, self.user_custom_data)
        self.assertIn("my_commands", result["categories"])
        self.assertIn("mybackup", result["categories"]["my_commands"]["commands"])
    
    def test_load_user_custom_not_exists(self):
        result = load_user_custom()
        self.assertEqual(result, {})
    
    def test_load_user_modified_exists(self):
        modified_file = self.project_root / "user" / "modified.json"
        
        with open(modified_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_modified_data, f)
        
        result = load_user_modified()
        self.assertEqual(result, self.user_modified_data)
        self.assertIn("system", result["categories"])
        self.assertIn("space", result["categories"]["system"]["commands"])
    
    def test_load_user_modified_not_exists(self):
        result = load_user_modified()
        self.assertEqual(result, {})
    
    def test_merge_commands_basic(self):
        result = merge_commands(self.valid_lang_data, {}, {})
        
        self.assertIn("categories", result)
        self.assertIn("system", result["categories"])
        self.assertIn("network", result["categories"])
        self.assertIn("space", result["categories"]["system"]["commands"])
        self.assertIn("ram", result["categories"]["system"]["commands"])
        self.assertIn("ip", result["categories"]["network"]["commands"])
        self.assertIn("ping", result["categories"]["network"]["commands"])
    
    def test_merge_commands_with_user_custom(self):
        result = merge_commands(self.valid_lang_data, self.user_custom_data, {})
        
        self.assertIn("system", result["categories"])
        self.assertIn("network", result["categories"])
        
        self.assertIn("my_commands", result["categories"])
        self.assertEqual(result["categories"]["my_commands"]["name"], "My Commands")
        self.assertIn("mybackup", result["categories"]["my_commands"]["commands"])
        self.assertIn("myclean", result["categories"]["my_commands"]["commands"])
        
        self.assertEqual(len(result["categories"]), 3)
    
    def test_merge_commands_with_user_modified_override(self):
        result = merge_commands(self.valid_lang_data, {}, self.user_modified_data)
        
        cmd_info = result["categories"]["system"]["commands"]["space"]
        self.assertEqual(cmd_info["cmd"], "df -h --total")
        self.assertEqual(cmd_info["description"], "Total disk space")
        
        self.assertEqual(result["categories"]["system"]["commands"]["ram"]["cmd"], "free -h")
        self.assertEqual(result["categories"]["network"]["commands"]["ip"]["cmd"], "ip a")
    
    def test_merge_commands_with_both_custom_and_modified(self):
        result = merge_commands(self.valid_lang_data, self.user_custom_data, self.user_modified_data)
        
        self.assertEqual(result["categories"]["system"]["commands"]["space"]["cmd"], "df -h --total")
        
        self.assertIn("my_commands", result["categories"])
        self.assertIn("mybackup", result["categories"]["my_commands"]["commands"])
        
        self.assertIn("ram", result["categories"]["system"]["commands"])
        self.assertIn("ip", result["categories"]["network"]["commands"])
    
    def test_merge_commands_empty_lang_data(self):
        result = merge_commands({}, self.user_custom_data, {})
        
        self.assertIn("categories", result)
        self.assertIn("my_commands", result["categories"])
        self.assertIn("mybackup", result["categories"]["my_commands"]["commands"])
    
    def test_merge_commands_all_empty(self):
        result = merge_commands({}, {}, {})
        
        self.assertIn("categories", result)
        self.assertEqual(len(result["categories"]), 0)
    
    def test_get_all_commands(self):
        result = get_all_commands(self.valid_lang_data)
        
        self.assertEqual(len(result), 4)
        self.assertIn("space", result)
        self.assertIn("ram", result)
        self.assertIn("ip", result)
        self.assertIn("ping", result)
        
        self.assertEqual(result["space"]["cmd"], "df -h")
        self.assertEqual(result["space"]["description"], "Disk space")
        self.assertEqual(result["space"]["category"], "System Info")
        self.assertEqual(result["space"]["args"], 0)
        
        self.assertEqual(result["ping"]["cmd"], "ping -c 4 {}")
        self.assertEqual(result["ping"]["args"], 1)
        self.assertEqual(result["ping"]["category"], "Network")
    
    def test_get_all_commands_with_custom_categories(self):
        merged = merge_commands(self.valid_lang_data, self.user_custom_data, {})
        result = get_all_commands(merged)
        
        self.assertIn("mybackup", result)
        self.assertEqual(result["mybackup"]["category"], "My Commands")
        self.assertEqual(result["mybackup"]["cmd"], "rsync -av")
        self.assertEqual(result["mybackup"]["args"], 2)
    
    def test_get_all_commands_empty(self):
        result = get_all_commands({})
        self.assertEqual(result, {})
        
        result = get_all_commands({"categories": {}})
        self.assertEqual(result, {})
    
    def test_find_command_exists(self):
        result = find_command("space", self.valid_lang_data)
        self.assertIsNotNone(result)
        self.assertEqual(result["cmd"], "df -h")
        self.assertEqual(result["description"], "Disk space")
        
        result = find_command("ping", self.valid_lang_data)
        self.assertIsNotNone(result)
        self.assertEqual(result["cmd"], "ping -c 4 {}")
        self.assertEqual(result["args"], 1)
    
    def test_find_command_case_sensitive(self):
        result = find_command("SPACE", self.valid_lang_data)
        self.assertIsNone(result)
        
        result = find_command("Space", self.valid_lang_data)
        self.assertIsNone(result)
    
    def test_find_command_not_exists(self):
        result = find_command("nonexistent_command_xyz", self.valid_lang_data)
        self.assertIsNone(result)
    
    def test_find_command_in_merged_data(self):
        merged = merge_commands(self.valid_lang_data, self.user_custom_data, self.user_modified_data)
        
        result = find_command("space", merged)
        self.assertEqual(result["cmd"], "df -h --total")
        
        result = find_command("mybackup", merged)
        self.assertEqual(result["cmd"], "rsync -av")
        
        result = find_command("ip", merged)
        self.assertEqual(result["cmd"], "ip a")
    
    def test_load_json_file_unicode(self):
        test_file = self.project_root / "unicode.json"
        test_data = {"message": "مرحبا بالعالم", "emoji": "😀🎉"}
        
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
        
        result = load_json_file(test_file)
        self.assertEqual(result["message"], "مرحبا بالعالم")
        self.assertEqual(result["emoji"], "😀🎉")
    
    def test_load_language_with_complex_structure(self):
        complex_data = {
            "language": "test",
            "name": "Test Language",
            "categories": {
                "category1": {
                    "name": "First Category",
                    "commands": {
                        "cmd1": {"cmd": "echo 1", "description": "One", "args": 0},
                        "cmd2": {"cmd": "echo {}", "description": "Two", "args": 1}
                    }
                },
                "category2": {
                    "name": "Second Category",
                    "commands": {
                        "cmd3": {"cmd": "ls {}", "description": "List", "args": 1}
                    }
                }
            }
        }
        
        lang_file = self.project_root / "langs" / "complex.json"
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(complex_data, f)
        
        result = load_language("complex")
        self.assertEqual(len(result["categories"]), 2)
        self.assertEqual(len(result["categories"]["category1"]["commands"]), 2)
        self.assertEqual(len(result["categories"]["category2"]["commands"]), 1)

if __name__ == "__main__":
    unittest.main()