#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Test module: test_executor.py
Author: Abdelrahman Gaballah
"""

import unittest
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.executor import (
    CommandExecutor,
    execute_command_safe,
    run_system_command,
    format_output
)

class TestCommandExecutor(unittest.TestCase):
    """Test cases for CommandExecutor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.executor = CommandExecutor(dry_run=True)
    
    def test_build_command_no_placeholders(self):
        """Test building command with no placeholders."""
        cmd_parts, error = self.executor.build_command("ls -la", [])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["ls", "-la"])
        self.assertEqual(error, "")
    
    def test_build_command_no_placeholders_with_args(self):
        """Test building command with no placeholders but extra args."""
        cmd_parts, error = self.executor.build_command("ls -la", ["extra", "args"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["ls", "-la", "extra", "args"])
        self.assertEqual(error, "")
    
    def test_build_command_with_one_placeholder(self):
        """Test building command with one placeholder."""
        cmd_parts, error = self.executor.build_command("cat {}", ["file.txt"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["cat", "file.txt"])
        self.assertEqual(error, "")
    
    def test_build_command_with_multiple_placeholders(self):
        """Test building command with multiple placeholders."""
        cmd_parts, error = self.executor.build_command("cp {} {}", ["file1.txt", "file2.txt"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["cp", "file1.txt", "file2.txt"])
        self.assertEqual(error, "")
    
    def test_build_command_with_three_placeholders(self):
        """Test building command with three placeholders."""
        cmd_parts, error = self.executor.build_command("mv {} {} {}", ["file1.txt", "file2.txt", "dest/"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["mv", "file1.txt", "file2.txt", "dest/"])
        self.assertEqual(error, "")
    
    def test_build_command_missing_argument(self):
        """Test building command when argument is missing."""
        cmd_parts, error = self.executor.build_command("cp {} {}", ["file1.txt"])
        self.assertIsNone(cmd_parts)
        self.assertIn("Missing argument", error)
    
    def test_build_command_multiple_missing_arguments(self):
        """Test building command when multiple arguments are missing."""
        cmd_parts, error = self.executor.build_command("cp {} {} {}", ["file1.txt"])
        self.assertIsNone(cmd_parts)
        self.assertIn("Missing argument", error)
    
    def test_build_command_extra_arguments(self):
        """Test that extra arguments are appended."""
        cmd_parts, error = self.executor.build_command("echo Hello", ["extra1", "extra2"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["echo", "Hello", "extra1", "extra2"])
    
    def test_build_command_with_mixed_placeholders(self):
        """Test building command with mixed placeholders and text."""
        cmd_parts, error = self.executor.build_command("echo {} world {}", ["hello", "!"])
        self.assertEqual(cmd_parts, ["echo", "hello", "world", "!"])
    
    def test_build_command_with_quoted_template(self):
        """Test building command with quoted parts in template."""
        cmd_parts, error = self.executor.build_command('echo "Hello {}"', ["world"])
        self.assertEqual(cmd_parts, ["echo", "Hello world"])
    
    def test_execute_dry_run(self):
        """Test dry run mode doesn't actually execute."""
        success, output = self.executor.execute_with_template("echo test", [])
        self.assertTrue(success)
        self.assertEqual(output, "")
    
    def test_execute_dry_run_with_output(self):
        """Test dry run mode with command that would produce output."""
        success, output = self.executor.execute_with_template("ls -la", [])
        self.assertTrue(success)
        self.assertEqual(output, "")
    
    def test_execute_with_real_executor_success(self):
        """Test real executor with successful command."""
        real_executor = CommandExecutor(dry_run=False)
        
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "test output\n"
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            success, output = real_executor.execute_with_template("echo test", [])
            self.assertTrue(success)
            self.assertEqual(output, "test output")
    
    def test_execute_with_real_executor_failure(self):
        """Test real executor with failing command."""
        real_executor = CommandExecutor(dry_run=False)
        
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "command failed"
            mock_run.return_value = mock_result
            
            success, output = real_executor.execute_with_template("false", [])
            self.assertFalse(success)
            self.assertEqual(output, "command failed")
    
    def test_execute_with_real_executor_exception(self):
        """Test real executor with exception."""
        real_executor = CommandExecutor(dry_run=False)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Something went wrong")
            
            success, output = real_executor.execute_with_template("some command", [])
            self.assertFalse(success)
            self.assertIn("Something went wrong", output)
    
    def test_check_sudo_needed_true(self):
        """Test detecting commands that need sudo."""
        sudo_commands = [
            ["apt", "update"],
            ["apt-get", "install"],
            ["dpkg", "-i"],
            ["systemctl", "restart", "docker"],
            ["service", "nginx", "restart"],
            ["mount", "/dev/sda1", "/mnt"],
            ["umount", "/mnt"],
            ["fdisk", "-l"],
            ["mkfs", "ext4", "/dev/sdb1"],
            ["chown", "user:user", "file"],
            ["chmod", "755", "file"],
            ["useradd", "newuser"],
            ["userdel", "olduser"],
            ["passwd", "user"],
            ["modprobe", "nvidia"],
            ["insmod", "module.ko"],
            ["rmmod", "module"]
        ]
        
        for cmd in sudo_commands:
            self.assertTrue(self.executor.check_sudo_needed(cmd))
    
    def test_check_sudo_needed_false(self):
        """Test commands that don't need sudo."""
        normal_commands = [
            ["ls", "-la"],
            ["echo", "hello"],
            ["cat", "file.txt"],
            ["grep", "pattern", "file"],
            ["find", ".", "-name", "*.txt"],
            ["ps", "aux"],
            ["top", "-bn1"],
            ["df", "-h"],
            ["free", "-h"],
            ["date"],
            ["whoami"],
            ["pwd"],
            ["cd", "/home"],
            ["mkdir", "newdir"],
            ["rm", "file.txt"],
            ["cp", "src", "dst"],
            ["mv", "old", "new"],
            ["touch", "file"],
            ["ln", "-s", "target", "link"]
        ]
        
        for cmd in normal_commands:
            self.assertFalse(self.executor.check_sudo_needed(cmd))
    
    def test_check_sudo_needed_empty_command(self):
        """Test checking sudo for empty command."""
        self.assertFalse(self.executor.check_sudo_needed([]))
    
    def test_run_system_command_success(self):
        """Test running system command successfully."""
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "success output"
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            code, stdout, stderr = run_system_command(["echo", "test"])
            self.assertEqual(code, 0)
            self.assertEqual(stdout, "success output")
            self.assertEqual(stderr, "")
    
    def test_run_system_command_with_stderr(self):
        """Test running system command that produces stderr."""
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "error occurred"
            mock_run.return_value = mock_result
            
            code, stdout, stderr = run_system_command(["ls", "/nonexistent"])
            self.assertEqual(code, 1)
            self.assertEqual(stdout, "")
            self.assertEqual(stderr, "error occurred")
    
    def test_run_system_command_timeout(self):
        """Test system command timeout."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="sleep", timeout=30)
            
            code, stdout, stderr = run_system_command(["sleep", "100"])
            self.assertEqual(code, -1)
            self.assertIn("timed out", stderr)
            self.assertIn("30", stderr)
    
    def test_run_system_command_not_found(self):
        """Test command not found error."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            
            code, stdout, stderr = run_system_command(["nonexistentcommand123"])
            self.assertEqual(code, -1)
            self.assertIn("not found", stderr)
    
    def test_run_system_command_permission_denied(self):
        """Test permission denied error."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = PermissionError()
            
            code, stdout, stderr = run_system_command(["/root/secret"])
            self.assertEqual(code, -1)
            self.assertIn("Permission", stderr)
    
    def test_format_output_with_stdout_only(self):
        """Test formatting output with only stdout."""
        result = format_output("line1\nline2\nline3", "")
        self.assertIn("line1", result)
        self.assertIn("line2", result)
        self.assertIn("line3", result)
        self.assertNotIn("STDERR", result)
    
    def test_format_output_with_stderr_only(self):
        """Test formatting output with only stderr."""
        result = format_output("", "error message")
        self.assertIn("STDERR", result)
        self.assertIn("error message", result)
    
    def test_format_output_with_both(self):
        """Test formatting output with both stdout and stderr."""
        result = format_output("stdout content", "stderr content")
        self.assertIn("stdout content", result)
        self.assertIn("STDERR", result)
        self.assertIn("stderr content", result)
    
    def test_format_output_empty(self):
        """Test formatting empty output."""
        result = format_output("", "")
        self.assertEqual(result, "")
    
    def test_format_output_truncation(self):
        """Test output truncation when too many lines."""
        many_lines = "\n".join([f"line {i}" for i in range(100)])
        result = format_output(many_lines, "", max_lines=10)
        
        self.assertIn("truncated", result)
        self.assertIn("line 0", result)
        self.assertIn("line 9", result)
        self.assertNotIn("line 10", result)
    
    def test_format_output_no_truncation(self):
        """Test output not truncated when within limit."""
        few_lines = "\n".join([f"line {i}" for i in range(5)])
        result = format_output(few_lines, "", max_lines=10)
        
        self.assertNotIn("truncated", result)
        self.assertIn("line 0", result)
        self.assertIn("line 4", result)
    
    def test_format_output_with_unicode(self):
        """Test formatting output with Unicode characters."""
        unicode_output = "مرحبا بالعالم\n😀🎉\nEnglish text"
        result = format_output(unicode_output, "")
        self.assertIn("مرحبا بالعالم", result)
        self.assertIn("😀🎉", result)
        self.assertIn("English text", result)
    
    def test_execute_command_safe_helper_success(self):
        """Test execute_command_safe helper function success."""
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "ok"
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            result = execute_command_safe("echo test", [])
            self.assertTrue(result)
    
    def test_execute_command_safe_helper_failure(self):
        """Test execute_command_safe helper function failure."""
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_result.stdout = ""
            mock_result.stderr = "error"
            mock_run.return_value = mock_result
            
            result = execute_command_safe("false", [])
            self.assertFalse(result)
    
    def test_execute_command_safe_helper_dry_run(self):
        """Test execute_command_safe helper with dry run."""
        with patch('core.executor.CommandExecutor') as MockExecutor:
            mock_executor = MagicMock()
            mock_executor.execute_with_template.return_value = (True, "")
            MockExecutor.return_value = mock_executor
            
            result = execute_command_safe("echo test", [], dry_run=True)
            self.assertTrue(result)
            MockExecutor.assert_called_with(dry_run=True)
    
    def test_executor_initialization(self):
        """Test CommandExecutor initialization."""
        executor = CommandExecutor(dry_run=True)
        self.assertTrue(executor.dry_run)
        
        executor = CommandExecutor(dry_run=False)
        self.assertFalse(executor.dry_run)
    
    def test_build_command_with_special_characters_in_args(self):
        """Test building command with special characters in arguments."""
        cmd_parts, error = self.executor.build_command("echo {}", ["Hello World!"])
        self.assertEqual(cmd_parts, ["echo", "Hello World!"])

if __name__ == "__main__":
    unittest.main()