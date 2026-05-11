# Contributing to Ka

Thank you for your interest in contributing to Ka! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Code Guidelines](#code-guidelines)
5. [Testing](#testing)
6. [Submitting Changes](#submitting-changes)
7. [Reporting Issues](#reporting-issues)
8. [Feature Requests](#feature-requests)
9. [Adding Commands](#adding-commands)
10. [Adding Languages](#adding-languages)
11. [Documentation](#documentation)

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git
- Basic knowledge of Linux commands

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/ka.git
cd ka
```

3. Add upstream remote:

```bash
git remote add upstream https://github.com/abdelrahman-gaballah/ka.git
```

## Development Setup

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov pylint black
```

### Run Ka in Development Mode

```bash
python -m core.__main__ --help
```

### Build and Install Locally

```bash
pip install -e .
```

## Code Guidelines

### Python Style Guide

We follow PEP 8 with some exceptions:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters
- Use descriptive variable names
- Write docstrings only when code intent is not obvious (avoid repeating what type hints already say)

### Code Organization

- `core/` - Core modules
- `langs/` - Language JSON files
- `user/` - User customization templates
- `scripts/` - Installation and helper scripts
- `tests/` - Unit tests

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `command_name` |
| Functions | snake_case | `load_language()` |
| Classes | PascalCase | `CommandParser` |
| Constants | UPPER_SNAKE | `DEFAULT_LANGUAGE` |

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_loader.py
```

### Run with Coverage

```bash
pytest --cov=core tests/
```

### Write Tests

Always write tests for new features and bug fixes. New features must have at least 80% test coverage.

## Submitting Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `lang/description` - Language additions

### Commit Messages

Follow conventional commits: `type(scope): description`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Request Process

1. Update your fork, create a feature branch, commit changes
2. Push to your fork and open a pull request
3. Ensure all tests pass, style is consistent, and docs are updated

## Reporting Issues

Include: Ka version, OS, reproduction steps, expected vs actual behavior, logs.

For security issues, email the maintainer directly instead of creating a public issue.

## Feature Requests

Include: clear description, use case, alternatives considered, example usage.

## Adding Commands

Edit `langs/en.json`, add the command under the appropriate category, test, and update docs.

```json
{
  "categories": {
    "utilities": {
      "name": "Utilities",
      "commands": {
        "mycommand": {
          "cmd": "actual-command {}",
          "description": "Description of the command",
          "args": 1
        }
      }
    }
  }
}
```

## Adding Languages

1. Run `./scripts/create_lang.sh`
2. Enter language code (2-3 lowercase letters) and display name
3. Translate descriptions in the generated file
4. Test with `ka help` after switching language in config
5. Submit a pull request

See `langs/README.md` for detailed language file structure.

## Documentation

| Change Type | Documentation to Update |
|-------------|------------------------|
| New command | `commands.md`, `en.json` |
| New language | `languages.md`, `README.md` |
| Bug fix | None (unless behavior changes) |
| Feature | `usage.md`, `README.md` |

## Recognition

Contributors will be recognized in the README and release notes. Thank you for helping make Ka better!
