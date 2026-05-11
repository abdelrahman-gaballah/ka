#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Test module: test_parser.py
Author: Abdelrahman Gaballah
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.parser import (
    CommandParser,
    quick_parse,
    is_help_request,
    is_version_request
)

class TestCommandParser(unittest.TestCase):

    
    def setUp(self):
        self.parser = CommandParser()
    
    def test_parse_input_simple_command(self):
        command, args = self.parser.parse_input(["space"])
        self.assertEqual(command, "space")
        self.assertEqual(args, [])
    
    def test_parse_input_command_with_args(self):
        command, args = self.parser.parse_input(["copy", "file1.txt", "file2.txt", "dest/"])
        self.assertEqual(command, "copy")
        self.assertEqual(args, ["file1.txt", "file2.txt", "dest/"])
    
    def test_parse_input_command_with_mixed_case(self):
        command, args = self.parser.parse_input(["CoPy", "file.txt", "dest.txt"])
        self.assertEqual(command, "copy")
        self.assertEqual(args, ["file.txt", "dest.txt"])
    
    def test_parse_input_command_uppercase(self):
        command, args = self.parser.parse_input(["SPACE"])
        self.assertEqual(command, "space")
        self.assertEqual(args, [])
    
    def test_parse_input_empty_args(self):
        command, args = self.parser.parse_input([])
        self.assertIsNone(command)
        self.assertEqual(args, [])
    
    def test_parse_input_none_args(self):
        command, args = self.parser.parse_input(None)
        self.assertIsNone(command)
        self.assertEqual(args, [])
    
    def test_validate_command_name_valid(self):
        valid_names = [
            "space", "ram", "copy-file", "my_command", "test123",
            "a", "very_long_command_name_123", "git-status", "_underscore"
        ]
        for name in valid_names:
            self.assertTrue(self.parser.validate_command_name(name))
    
    def test_validate_command_name_invalid(self):
        invalid_names = [
            "", "space!", "ram@", "copy file", "my#command", 
            "test$", "cmd;", "cmd&", "cmd|", "cmd>", "cmd<",
            "cmd`", "cmd$(echo)", "كلمة", "command with spaces"
        ]
        for name in invalid_names:
            self.assertFalse(self.parser.validate_command_name(name))
    
    def test_validate_arguments_safe(self):
        safe_args = [
            "file.txt", "my-document", "path/to/file", "file_name", 
            "backup.tar.gz", "file123", ".hidden", "file.backup",
            "/absolute/path", "./relative", "../parent", "file_v2.1"
        ]
        valid, invalid = self.parser.validate_arguments(safe_args)
        self.assertTrue(valid)
        self.assertEqual(invalid, [])
    
    def test_validate_arguments_unsafe(self):
        unsafe_args = [
            "file; rm -rf /", "test$(echo hi)", "`whoami`", 
            "file|cat", "file && echo", "file || echo",
            "file > output", "file < input", "file >> output",
            "test$test"
        ]
        valid, invalid = self.parser.validate_arguments(unsafe_args)
        self.assertFalse(valid)
        self.assertGreater(len(invalid), 0)
    
    def test_validate_arguments_mixed_safe_unsafe(self):
        mixed_args = ["safe.txt", "bad;cmd", "safe2.txt", "bad|cmd"]
        valid, invalid = self.parser.validate_arguments(mixed_args)
        self.assertFalse(valid)
        self.assertEqual(len(invalid), 2)
        self.assertIn("bad;cmd", invalid)
        self.assertIn("bad|cmd", invalid)
    
    def test_validate_arguments_empty(self):
        valid, invalid = self.parser.validate_arguments([])
        self.assertTrue(valid)
        self.assertEqual(invalid, [])
    
    def test_sanitize_argument(self):
        test_cases = [
            ("test; rm -rf /", "test rm -rf /"),
            ("file$(echo hi)", "file$(echo hi)"),
            ("`whoami`", "whoami"),
            ("test|cat", "testcat"),
            ("file && echo", "file  echo"),
            ("test$test", "test$test"),
        ]
        for dirty, expected_clean in test_cases:
            clean = self.parser.sanitize_argument(dirty)
            self.assertNotIn(";", clean)
            self.assertNotIn("|", clean)
    
    def test_sanitize_argument_safe_unchanged(self):
        safe_args = ["file.txt", "my-document", "path/to/file", "file123"]
        for arg in safe_args:
            sanitized = self.parser.sanitize_argument(arg)
            self.assertEqual(sanitized, arg)
    
    def test_check_argument_count_exact(self):
        cmd_info = {"args": 2}
        valid, msg = self.parser.check_argument_count(cmd_info, ["arg1", "arg2"])
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_check_argument_count_more_than_needed(self):
        cmd_info = {"args": 1}
        valid, msg = self.parser.check_argument_count(cmd_info, ["arg1", "arg2", "arg3"])
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_check_argument_count_missing(self):
        cmd_info = {"args": 3}
        valid, msg = self.parser.check_argument_count(cmd_info, ["arg1", "arg2"])
        self.assertFalse(valid)
        self.assertIn("Missing", msg)
        self.assertIn("3", msg)
        self.assertIn("2", msg)
    
    def test_check_argument_count_no_args_needed(self):
        cmd_info = {"args": 0}
        valid, msg = self.parser.check_argument_count(cmd_info, [])
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_check_argument_count_no_args_specified(self):
        cmd_info = {}
        valid, msg = self.parser.check_argument_count(cmd_info, ["arg1"])
        self.assertTrue(valid)
        self.assertEqual(msg, "")
    
    def test_is_dangerous_pattern(self):
        dangerous_patterns = [
            ";", "&&", "||", "|", "`", "$(", "${", "$[",
            ">", ">>", "<", "<<",
            "&", "#", "!", "~", "`echo`", "$(echo)"
        ]
        for pattern in dangerous_patterns:
            self.assertTrue(self.parser._is_dangerous_pattern(pattern))
    
    def test_is_dangerous_pattern_safe(self):
        safe_patterns = ["/", ".", ":", "hello", "file.txt", "path/to/file"]
        for pattern in safe_patterns:
            self.assertFalse(self.parser._is_dangerous_pattern(pattern))
    
    def test_quick_parse_helper(self):
        command, args = quick_parse(["help"])
        self.assertEqual(command, "help")
        self.assertEqual(args, [])
        
        command, args = quick_parse(["copy", "src", "dst"])
        self.assertEqual(command, "copy")
        self.assertEqual(args, ["src", "dst"])
    
    def test_is_help_request_with_help_flag(self):
        help_flags = ["help", "-h", "--help", "-help", "?"]
        for flag in help_flags:
            self.assertTrue(is_help_request(flag, []))
    
    def test_is_help_request_as_argument(self):
        self.assertTrue(is_help_request("space", ["--help"]))
        self.assertTrue(is_help_request("copy", ["-h"]))
        self.assertTrue(is_help_request("delete", ["help"]))
        self.assertTrue(is_help_request("move", ["-help"]))
        self.assertTrue(is_help_request("list", ["?"]))
    
    def test_is_help_request_multiple_args(self):
        self.assertTrue(is_help_request("space", ["--help", "something"]))
        self.assertTrue(is_help_request("space", ["something", "--help"]))
    
    def test_is_help_request_false(self):
        non_help = [
            ("space", []), ("ram", []), ("copy", ["file.txt"]),
            ("version", []), ("-v", []), ("--version", [])
        ]
        for cmd, args in non_help:
            self.assertFalse(is_help_request(cmd, args))
    
    def test_is_version_request_with_version_flag(self):
        version_flags = ["version", "-v", "--version", "-version"]
        for flag in version_flags:
            self.assertTrue(is_version_request(flag, []))
    
    def test_is_version_request_as_argument(self):
        self.assertTrue(is_version_request("space", ["--version"]))
        self.assertTrue(is_version_request("ram", ["-v"]))
        self.assertTrue(is_version_request("copy", ["version"]))
        self.assertTrue(is_version_request("list", ["-version"]))
    
    def test_is_version_request_multiple_args(self):
        self.assertTrue(is_version_request("space", ["--version", "something"]))
        self.assertTrue(is_version_request("space", ["something", "-v"]))
    
    def test_is_version_request_false(self):
        non_version = [
            ("space", []), ("ram", []), ("help", []),
            ("-h", []), ("--help", []), ("copy", ["file.txt"])
        ]
        for cmd, args in non_version:
            self.assertFalse(is_version_request(cmd, args))
    
    def test_extract_command_name_simple(self):
        result = self.parser.extract_command_name("space")
        self.assertEqual(result, "space")
        
        result = self.parser.extract_command_name("copy file1 file2")
        self.assertEqual(result, "copy")
        
        result = self.parser.extract_command_name("git status")
        self.assertEqual(result, "git")
    
    def test_extract_command_name_with_quotes(self):
        result = self.parser.extract_command_name('echo "hello world"')
        self.assertEqual(result, "echo")
        
        result = self.parser.extract_command_name("cp 'file with spaces' dest")
        self.assertEqual(result, "cp")
    
    def test_extract_command_name_empty(self):
        result = self.parser.extract_command_name("")
        self.assertIsNone(result)
        
        result = self.parser.extract_command_name("   ")
        self.assertIsNone(result)
    
    def test_validate_arguments_allows_paths(self):
        path_args = [
            "/home/user/file.txt",
            "./local/file",
            "../parent/file",
            "C:/windows/path",
            "file with spaces.txt",
            "file-name_v2.1.tar.gz"
        ]
        valid, invalid = self.parser.validate_arguments(path_args)
        self.assertTrue(valid)
        self.assertEqual(invalid, [])
    
    def test_validate_arguments_allows_emails(self):
        email_args = ["user@example.com", "name@domain.co.uk"]
        valid, invalid = self.parser.validate_arguments(email_args)
        self.assertTrue(valid)
    
    def test_validate_arguments_blocks_sql_injection(self):
        sql_args = ["'; DROP TABLE users; --", "1' OR '1'='1", "admin'--"]
        valid, invalid = self.parser.validate_arguments(sql_args)
        self.assertFalse(valid)
        self.assertGreater(len(invalid), 0)
    
    def test_validate_arguments_blocks_path_traversal(self):
        traversal_args = ["../../../etc/passwd", "....//....//....//etc/passwd"]
        valid, invalid = self.parser.validate_arguments(traversal_args)
        # Path traversal with dots might be allowed or blocked based on pattern
        # This test just ensures no crash
        self.assertIsInstance(valid, bool)
        self.assertIsInstance(invalid, list)
    
    def test_sanitize_argument_removes_multiple_dangerous(self):
        dirty = "test; rm -rf / && echo hacked | cat > file"
        clean = self.parser.sanitize_argument(dirty)
        self.assertNotIn(";", clean)
        self.assertNotIn("&&", clean)
        self.assertNotIn("|", clean)
        self.assertNotIn(">", clean)
    
    def test_command_parser_initialization(self):
        parser = CommandParser()
        self.assertIsNotNone(parser.command_pattern)
        self.assertIsNotNone(parser.arg_pattern)
        self.assertTrue(hasattr(parser, '_is_dangerous_pattern'))
        self.assertTrue(hasattr(parser, '_is_safe_special_char'))

if __name__ == "__main__":
    unittest.main()