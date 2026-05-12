#!/usr/bin/env python3

# Author: Abdelrahman Gaballah

import unittest
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.executor import (
    CommandExecutor,
    run_system_command,
    format_output
)

class TestCommandExecutor(unittest.TestCase):

    
    def setUp(self):
        self.executor = CommandExecutor(dry_run=True)
    
    def test_build_command_no_placeholders(self):
        cmd_parts, error = self.executor.build_command("ls -la", [])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["ls", "-la"])
        self.assertEqual(error, "")
    
    def test_build_command_no_placeholders_with_args(self):
        cmd_parts, error = self.executor.build_command("ls -la", ["extra", "args"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["ls", "-la", "extra", "args"])
        self.assertEqual(error, "")
    
    def test_build_command_with_one_placeholder(self):
        cmd_parts, error = self.executor.build_command("cat {}", ["file.txt"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["cat", "file.txt"])
        self.assertEqual(error, "")
    
    def test_build_command_with_multiple_placeholders(self):
        cmd_parts, error = self.executor.build_command("cp {} {}", ["file1.txt", "file2.txt"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["cp", "file1.txt", "file2.txt"])
        self.assertEqual(error, "")
    
    def test_build_command_with_three_placeholders(self):
        cmd_parts, error = self.executor.build_command("mv {} {} {}", ["file1.txt", "file2.txt", "dest/"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["mv", "file1.txt", "file2.txt", "dest/"])
        self.assertEqual(error, "")
    
    def test_build_command_missing_argument(self):
        cmd_parts, error = self.executor.build_command("cp {} {}", ["file1.txt"])
        self.assertIsNone(cmd_parts)
        self.assertIn("Missing argument", error)
    
    def test_build_command_multiple_missing_arguments(self):
        cmd_parts, error = self.executor.build_command("cp {} {} {}", ["file1.txt"])
        self.assertIsNone(cmd_parts)
        self.assertIn("Missing argument", error)
    
    def test_build_command_extra_arguments(self):
        cmd_parts, error = self.executor.build_command("echo Hello", ["extra1", "extra2"])
        self.assertIsNotNone(cmd_parts)
        self.assertEqual(cmd_parts, ["echo", "Hello", "extra1", "extra2"])
    
    def test_build_command_with_mixed_placeholders(self):
        cmd_parts, error = self.executor.build_command("echo {} world {}", ["hello", "!"])
        self.assertEqual(cmd_parts, ["echo", "hello", "world", "!"])
    
    def test_build_command_with_quoted_template(self):
        cmd_parts, error = self.executor.build_command('echo "Hello {}"', ["world"])
        self.assertEqual(cmd_parts, ["echo", "Hello world"])
    
    def test_execute_dry_run(self):
        success, output = self.executor.execute_with_template("echo test", [])
        self.assertTrue(success)
        self.assertEqual(output, "")
    
    def test_execute_dry_run_with_output(self):
        success, output = self.executor.execute_with_template("ls -la", [])
        self.assertTrue(success)
        self.assertEqual(output, "")
    
    def test_execute_with_real_executor_success(self):
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
        real_executor = CommandExecutor(dry_run=False)
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = OSError("Something went wrong")
            
            success, output = real_executor.execute_with_template("some command", [])
            self.assertFalse(success)
            self.assertIn("Something went wrong", output)
    
    def test_check_sudo_needed_true(self):
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
        self.assertFalse(self.executor.check_sudo_needed([]))
    
    def test_run_system_command_success(self):
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
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="sleep", timeout=30)
            
            code, stdout, stderr = run_system_command(["sleep", "100"])
            self.assertEqual(code, -1)
            self.assertIn("timed out", stderr)
            self.assertIn("30", stderr)
    
    def test_run_system_command_not_found(self):
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()
            
            code, stdout, stderr = run_system_command(["nonexistentcommand123"])
            self.assertEqual(code, -1)
            self.assertIn("not found", stderr)
    
    def test_run_system_command_permission_denied(self):
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = PermissionError()
            
            code, stdout, stderr = run_system_command(["/root/secret"])
            self.assertEqual(code, -1)
            self.assertIn("Permission", stderr)
    
    def test_format_output_with_stdout_only(self):
        result = format_output("line1\nline2\nline3", "")
        self.assertIn("line1", result)
        self.assertIn("line2", result)
        self.assertIn("line3", result)
        self.assertNotIn("STDERR", result)
    
    def test_format_output_with_stderr_only(self):
        result = format_output("", "error message")
        self.assertIn("STDERR", result)
        self.assertIn("error message", result)
    
    def test_format_output_with_both(self):
        result = format_output("stdout content", "stderr content")
        self.assertIn("stdout content", result)
        self.assertIn("STDERR", result)
        self.assertIn("stderr content", result)
    
    def test_format_output_empty(self):
        result = format_output("", "")
        self.assertEqual(result, "")
    
    def test_format_output_truncation(self):
        many_lines = "\n".join([f"line {i}" for i in range(100)])
        result = format_output(many_lines, "", max_lines=10)
        
        self.assertIn("truncated", result)
        self.assertIn("line 0", result)
        self.assertIn("line 9", result)
        self.assertNotIn("line 10", result)
    
    def test_format_output_no_truncation(self):
        few_lines = "\n".join([f"line {i}" for i in range(5)])
        result = format_output(few_lines, "", max_lines=10)
        
        self.assertNotIn("truncated", result)
        self.assertIn("line 0", result)
        self.assertIn("line 4", result)
    
    def test_format_output_with_unicode(self):
        unicode_output = "مرحبا بالعالم\n😀🎉\nEnglish text"
        result = format_output(unicode_output, "")
        self.assertIn("مرحبا بالعالم", result)
        self.assertIn("😀🎉", result)
        self.assertIn("English text", result)
    
    def test_executor_initialization(self):
        executor = CommandExecutor(dry_run=True)
        self.assertTrue(executor.dry_run)
        
        executor = CommandExecutor(dry_run=False)
        self.assertFalse(executor.dry_run)
    
    def test_build_command_with_special_characters_in_args(self):
        cmd_parts, error = self.executor.build_command("echo {}", ["Hello World!"])
        self.assertEqual(cmd_parts, ["echo", "Hello World!"])

if __name__ == "__main__":
    unittest.main()