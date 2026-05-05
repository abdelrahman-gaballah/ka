#!/usr/bin/env python3

"""
Ka - Easy Linux Commands
Module: executor.py - Execute system commands safely
"""

import subprocess
import sys
from typing import List, Tuple, Optional


class CommandExecutor:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
    
    def build_command(self, cmd_template: str, args: List[str]) -> Tuple[Optional[str], str]:
        result = cmd_template
        for arg in args:
            result = result.replace('{}', arg, 1)
        return result, ""
    
    def execute(self, command_str: str) -> Tuple[bool, str, str]:
        if self.dry_run:
            print(f"[DRY RUN] {command_str}")
            return True, "", ""
        
        try:
            result = subprocess.run(
                command_str,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                executable='/bin/bash'
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def execute_with_template(self, cmd_template: str, args: List[str]) -> Tuple[bool, str]:
        command_str, error = self.build_command(cmd_template, args)
        if error:
            return False, error
        success, out, err = self.execute(command_str)
        return success, (out + err).strip()


def execute_command_safe(cmd_template: str, args: List[str], dry_run: bool = False) -> bool:
    executor = CommandExecutor(dry_run=dry_run)
    success, output = executor.execute_with_template(cmd_template, args)
    if output:
        print(output)
    return success


def run_system_command(command: str, timeout: int = 30) -> Tuple[int, str, str]:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            executable='/bin/bash'
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def format_output(stdout: str, stderr: str, max_lines: int = 50) -> str:
    output = ""
    if stdout:
        lines = stdout.split('\n')
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines.append(f"... (output truncated)")
        output += '\n'.join(lines)
    if stderr:
        if output:
            output += '\n'
        output += f"[STDERR]\n{stderr}"
    return output.strip()