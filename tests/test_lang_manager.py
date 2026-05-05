#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Test module: test_lang_manager.py
Author: Abdelrahman Gaballah
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lang_manager import (
    LanguageManager,
    get_language_list,
    is_language_available
)

class TestLanguageManager(unittest.TestCase):
    """Test cases for LanguageManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(self.temp_dir)
        
        # Create mock directories
        (self.project_root / "langs").mkdir()
        
        # Create mock language files
        self.en_data = {
            "language": "en",
            "name": "English",
            "categories": {
                "system": {
                    "name": "System Info",
                    "commands": {
                        "space": {"cmd": "df -h", "description": "Disk space", "args": 0},
                        "ram": {"cmd": "free -h", "description": "RAM usage", "args": 0},
                        "cpu": {"cmd": "top -bn1 | grep Cpu", "description": "CPU usage", "args": 0}
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
        
        self.ar_data = {
            "language": "ar",
            "name": "العربية",
            "categories": {
                "system": {
                    "name": "معلومات النظام",
                    "commands": {
                        "space": {"cmd": "df -h", "description": "مساحة التخزين", "args": 0},
                        "ram": {"cmd": "free -h", "description": "ذاكرة الوصول", "args": 0},
                        "cpu": {"cmd": "top -bn1 | grep Cpu", "description": "استخدام المعالج", "args": 0}
                    }
                },
                "network": {
                    "name": "الشبكة",
                    "commands": {
                        "ip": {"cmd": "ip a", "description": "عنوان IP", "args": 0},
                        "ping": {"cmd": "ping -c 4 {}", "description": "اختبار اتصال", "args": 1}
                    }
                }
            }
        }
        
        self.es_data = {
            "language": "es",
            "name": "Español",
            "categories": {
                "system": {
                    "name": "Información del Sistema",
                    "commands": {
                        "space": {"cmd": "df -h", "description": "Espacio en disco", "args": 0},
                        "ram": {"cmd": "free -h", "description": "Uso de RAM", "args": 0}
                    }
                }
            }
        }
        
        # Write mock language files
        self.en_path = self.project_root / "langs" / "en.json"
        self.ar_path = self.project_root / "langs" / "ar.json"
        self.es_path = self.project_root / "langs" / "es.json"
        self.template_path = self.project_root / "langs" / "template.json"
        
        with open(self.en_path, 'w', encoding='utf-8') as f:
            json.dump(self.en_data, f, ensure_ascii=False)
        
        with open(self.ar_path, 'w', encoding='utf-8') as f:
            json.dump(self.ar_data, f, ensure_ascii=False)
        
        with open(self.es_path, 'w', encoding='utf-8') as f:
            json.dump(self.es_data, f, ensure_ascii=False)
        
        with open(self.template_path, 'w', encoding='utf-8') as f:
            json.dump({"language": "TEMPLATE", "name": "Template", "categories": {}}, f)
        
        # Mock the PROJECT_ROOT
        self.mock_root_patcher = patch('core.lang_manager.PROJECT_ROOT', self.project_root)
        self.mock_root = self.mock_root_patcher.start()
        
        self.lang_manager = LanguageManager()
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.mock_root_patcher.stop()
        shutil.rmtree(self.temp_dir)
    
    def test_scan_available_languages(self):
        """Test scanning available languages returns correct codes and names."""
        langs = self.lang_manager.available_langs
        self.assertIn('en', langs)
        self.assertIn('ar', langs)
        self.assertIn('es', langs)
        self.assertEqual(langs['en'], 'English')
        self.assertEqual(langs['ar'], 'العربية')
        self.assertEqual(langs['es'], 'Español')
    
    def test_scan_available_languages_ignores_template(self):
        """Test that template.json is not counted as a language."""
        langs = self.lang_manager.available_langs
        self.assertNotIn('template', langs)
    
    def test_get_language_name_valid(self):
        """Test getting language display name for existing languages."""
        name = self.lang_manager.get_language_name('en')
        self.assertEqual(name, 'English')
        
        name = self.lang_manager.get_language_name('ar')
        self.assertEqual(name, 'العربية')
        
        name = self.lang_manager.get_language_name('es')
        self.assertEqual(name, 'Español')
    
    def test_get_language_name_invalid(self):
        """Test getting language name for non-existent language returns code."""
        name = self.lang_manager.get_language_name('xx')
        self.assertEqual(name, 'xx')
        
        name = self.lang_manager.get_language_name('')
        self.assertEqual(name, '')
    
    def test_get_current_language_from_config(self):
        """Test getting current language from config dictionary."""
        config = {'language': 'en'}
        lang = self.lang_manager.get_current_language(config)
        self.assertEqual(lang, 'en')
        
        config = {'language': 'ar'}
        lang = self.lang_manager.get_current_language(config)
        self.assertEqual(lang, 'ar')
        
        config = {'language': 'es'}
        lang = self.lang_manager.get_current_language(config)
        self.assertEqual(lang, 'es')
    
    def test_get_current_language_missing_key(self):
        """Test fallback to English when language key is missing."""
        config = {}
        lang = self.lang_manager.get_current_language(config)
        self.assertEqual(lang, 'en')
    
    def test_get_current_language_fallback_to_en(self):
        """Test fallback to English when configured language is not available."""
        config = {'language': 'nonexistent_lang'}
        lang = self.lang_manager.get_current_language(config)
        self.assertEqual(lang, 'en')
    
    def test_list_languages_returns_correct_format(self):
        """Test list_languages returns list of dicts with code and name."""
        languages = self.lang_manager.list_languages()
        self.assertEqual(len(languages), 3)
        
        for lang in languages:
            self.assertIn('code', lang)
            self.assertIn('name', lang)
        
        codes = [l['code'] for l in languages]
        names = [l['name'] for l in languages]
        
        self.assertIn('en', codes)
        self.assertIn('ar', codes)
        self.assertIn('es', codes)
        self.assertIn('English', names)
        self.assertIn('العربية', names)
        self.assertIn('Español', names)
    
    def test_load_language_file_exists(self):
        """Test loading existing language file returns correct data."""
        data = self.lang_manager.load_language_file('en')
        self.assertEqual(data['language'], 'en')
        self.assertEqual(data['name'], 'English')
        self.assertIn('categories', data)
        self.assertIn('system', data['categories'])
        self.assertIn('network', data['categories'])
    
    def test_load_language_file_not_exists(self):
        """Test loading non-existent language file returns empty dict."""
        data = self.lang_manager.load_language_file('nonexistent_lang')
        self.assertEqual(data, {})
    
    def test_load_language_file_invalid_json(self):
        """Test loading invalid JSON file returns empty dict."""
        invalid_path = self.project_root / "langs" / "invalid.json"
        with open(invalid_path, 'w', encoding='utf-8') as f:
            f.write("{invalid json content")
        
        # Need to rescan to pick up the invalid file
        self.lang_manager._scan_available_languages()
        data = self.lang_manager.load_language_file('invalid')
        self.assertEqual(data, {})
    
    def test_create_language_template_success(self):
        """Test creating new language file from template successfully."""
        success = self.lang_manager.create_language_template('fr', 'Français')
        self.assertTrue(success)
        
        fr_path = self.project_root / "langs" / "fr.json"
        self.assertTrue(fr_path.exists())
        
        with open(fr_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data['language'], 'fr')
        self.assertEqual(data['name'], 'Français')
        self.assertIn('categories', data)
    
    def test_create_language_template_german(self):
        """Test creating German language file."""
        success = self.lang_manager.create_language_template('de', 'Deutsch')
        self.assertTrue(success)
        
        de_path = self.project_root / "langs" / "de.json"
        self.assertTrue(de_path.exists())
        
        with open(de_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data['language'], 'de')
        self.assertEqual(data['name'], 'Deutsch')
    
    def test_create_language_template_japanese(self):
        """Test creating Japanese language file."""
        success = self.lang_manager.create_language_template('ja', '日本語')
        self.assertTrue(success)
        
        ja_path = self.project_root / "langs" / "ja.json"
        self.assertTrue(ja_path.exists())
        
        with open(ja_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertEqual(data['language'], 'ja')
        self.assertEqual(data['name'], '日本語')
    
    def test_create_language_template_template_missing(self):
        """Test creating language file when template.json is missing."""
        self.template_path.unlink()
        
        success = self.lang_manager.create_language_template('pt', 'Português')
        self.assertFalse(success)
    
    def test_create_language_template_already_exists(self):
        """Test creating language file that already exists."""
        success = self.lang_manager.create_language_template('en', 'English')
        self.assertTrue(success)  # Should overwrite or create? Depends on implementation
        
        en_path = self.project_root / "langs" / "en.json"
        self.assertTrue(en_path.exists())
    
    def test_delete_language_user_created(self):
        """Test deleting a user-created language file."""
        test_path = self.project_root / "langs" / "test_lang.json"
        with open(test_path, 'w', encoding='utf-8') as f:
            json.dump({"language": "test", "name": "Test Language"}, f)
        
        success = self.lang_manager.delete_language('test_lang')
        self.assertTrue(success)
        self.assertFalse(test_path.exists())
    
    def test_delete_builtin_language_not_allowed(self):
        """Test that deleting built-in languages (en, ar) is not allowed."""
        success_en = self.lang_manager.delete_language('en')
        self.assertFalse(success_en)
        
        success_ar = self.lang_manager.delete_language('ar')
        self.assertFalse(success_ar)
    
    def test_delete_nonexistent_language(self):
        """Test deleting non-existent language file returns False."""
        success = self.lang_manager.delete_language('nonexistent_lang')
        self.assertFalse(success)
    
    def test_get_command_translation_cmd(self):
        """Test getting command translation for cmd field."""
        cmd_info = self.lang_manager.get_command_translation('en', 'space', 'cmd')
        self.assertEqual(cmd_info, 'df -h')
        
        cmd_info = self.lang_manager.get_command_translation('en', 'ping', 'cmd')
        self.assertEqual(cmd_info, 'ping -c 4 {}')
    
    def test_get_command_translation_description(self):
        """Test getting command translation for description field."""
        desc = self.lang_manager.get_command_translation('en', 'space', 'description')
        self.assertEqual(desc, 'Disk space')
        
        desc = self.lang_manager.get_command_translation('en', 'ram', 'description')
        self.assertEqual(desc, 'RAM usage')
    
    def test_get_command_translation_arabic(self):
        """Test getting command translations in Arabic."""
        desc = self.lang_manager.get_command_translation('ar', 'space', 'description')
        self.assertEqual(desc, 'مساحة التخزين')
        
        desc = self.lang_manager.get_command_translation('ar', 'ram', 'description')
        self.assertEqual(desc, 'ذاكرة الوصول')
        
        desc = self.lang_manager.get_command_translation('ar', 'ping', 'description')
        self.assertEqual(desc, 'اختبار اتصال')
    
    def test_get_command_translation_returns_none_for_nonexistent_command(self):
        """Test that non-existent command returns None."""
        result = self.lang_manager.get_command_translation('en', 'nonexistent_command_xyz')
        self.assertIsNone(result)
    
    def test_get_command_translation_returns_none_for_nonexistent_language(self):
        """Test that non-existent language returns None for command."""
        result = self.lang_manager.get_command_translation('xx', 'space')
        self.assertIsNone(result)
    
    def test_get_command_translation_returns_none_for_invalid_field(self):
        """Test that invalid field returns None."""
        result = self.lang_manager.get_command_translation('en', 'space', 'invalid_field')
        self.assertIsNone(result)
    
    def test_get_language_list_helper(self):
        """Test get_language_list helper function returns list of codes."""
        result = get_language_list()
        self.assertIsInstance(result, list)
        self.assertIn('en', result)
        self.assertIn('ar', result)
        self.assertIn('es', result)
    
    def test_is_language_available_helper_true(self):
        """Test is_language_available helper returns True for existing languages."""
        self.assertTrue(is_language_available('en'))
        self.assertTrue(is_language_available('ar'))
        self.assertTrue(is_language_available('es'))
    
    def test_is_language_available_helper_false(self):
        """Test is_language_available helper returns False for non-existent languages."""
        self.assertFalse(is_language_available('xx'))
        self.assertFalse(is_language_available('nonexistent'))
        self.assertFalse(is_language_available(''))
    
    def test_language_manager_initialization(self):
        """Test LanguageManager initializes correctly."""
        mgr = LanguageManager()
        self.assertIsNotNone(mgr.langs_dir)
        self.assertIsNotNone(mgr.available_langs)
        self.assertIsInstance(mgr.available_langs, dict)
    
    def test_scan_available_languages_with_corrupt_file(self):
        """Test scanning handles corrupt JSON files gracefully."""
        corrupt_path = self.project_root / "langs" / "corrupt.json"
        with open(corrupt_path, 'w', encoding='utf-8') as f:
            f.write("this is not valid json")
        
        mgr = LanguageManager()
        langs = mgr.available_langs
        self.assertNotIn('corrupt', langs)
        self.assertIn('en', langs)
    
    def test_load_language_file_with_unicode(self):
        """Test loading language file with Unicode characters."""
        unicode_data = {
            "language": "ja",
            "name": "日本語",
            "categories": {
                "test": {
                    "name": "テスト",
                    "commands": {
                        "test": {"cmd": "echo", "description": "テスト説明", "args": 0}
                    }
                }
            }
        }
        
        unicode_path = self.project_root / "langs" / "ja.json"
        with open(unicode_path, 'w', encoding='utf-8') as f:
            json.dump(unicode_data, f, ensure_ascii=False)
        
        data = self.lang_manager.load_language_file('ja')
        self.assertEqual(data['name'], '日本語')
        self.assertEqual(data['categories']['test']['name'], 'テスト')

if __name__ == "__main__":
    unittest.main()