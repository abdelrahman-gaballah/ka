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
./ka --help
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
- Add docstrings to all functions and classes

### Example

```python
def load_language(lang_code: str) -> dict:
    """
    Load a language file from langs directory.

    Args:
        lang_code: Language code (e.g., 'en', 'ar')

    Returns:
        Dictionary containing language data
    """
    pass
```

### Code Organization

- `core/` - Core modules (do not modify unless necessary)
- `langs/` - Language files (add new languages here)
- `user/` - User customization (do not commit personal configs)
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

Always write tests for new features. Example:

```python
def test_new_feature():
    """Test that new feature works correctly."""
    result = my_function()
    assert result == expected_value
```

### Test Requirements

- All tests must pass before submitting a pull request
- New features must have at least 80% test coverage
- Bug fixes should include regression tests

## Submitting Changes

### Branch Naming

Use descriptive branch names:

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `lang/description` - Language additions

### Commit Messages

Follow the Conventional Commits specification:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions or fixes
- `chore`: Maintenance tasks

Examples:

```
feat(lang): add Spanish language support

- Add es.json with complete translations
- Update language manager to handle Spanish
- Add tests for Spanish language

Closes #42
```

```
fix(parser): handle empty command arguments

Previously empty arguments would cause IndexError.
Now returns empty list correctly.

Fixes #15
```

### Pull Request Process

1. Update your fork with upstream:

```bash
git checkout main
git pull upstream main
git push origin main
```

2. Create a feature branch:

```bash
git checkout -b feature/my-feature
```

3. Make your changes and commit them
4. Push to your fork:

```bash
git push origin feature/my-feature
```

5. Open a pull request on GitHub
6. Wait for review and address any feedback

### PR Requirements

- All tests must pass
- Code must follow style guidelines
- Include tests for new functionality
- Update documentation as needed
- One feature per pull request

## Reporting Issues

### Bug Reports

When reporting a bug, include:

- Ka version (`ka version`)
- Operating system and version
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any error messages or logs

Example:

```markdown
**Ka Version:** 0.1.0
**OS:** Ubuntu 22.04

**Steps to Reproduce:**
1. Run `ka invalid-command`
2. See error

**Expected:** Show "command not found" message
**Actual:** Traceback with KeyError

**Logs:**
Traceback (most recent call last):
  File "/usr/local/bin/ka", line 45, in <module>
    main()
...
```

### Security Issues

For security vulnerabilities, please email directly instead of creating a public issue.

## Feature Requests

Feature requests are welcome. Please include:

- Clear description of the feature
- Use case or problem it solves
- Any alternative solutions considered
- Example usage if applicable

## Adding Commands

To add a new command to the default language:

1. Edit `langs/en.json`
2. Add the command to the appropriate category
3. Test the command thoroughly
4. Update documentation

Example:

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

To add a new language:

1. Run the language creation script:

```bash
./scripts/create_lang.sh
```

2. Enter language code and name
3. Translate all descriptions in the new file
4. Test the language by switching to it
5. Update documentation to include the new language
6. Submit a pull request

### Language File Checklist

- [ ] All descriptions are translated
- [ ] JSON is valid (use `python -m json.tool` to validate)
- [ ] UTF-8 encoding is used
- [ ] Language code is 2-3 lowercase letters
- [ ] File is placed in `langs/` directory

## Documentation

### Where to Update Documentation

| Change Type | Documentation to Update |
|-------------|------------------------|
| New command | `commands.md`, `en.json` |
| New language | `languages.md`, `README.md` |
| Bug fix | None (unless behavior changes) |
| Feature | `usage.md`, `README.md` |

### Documentation Style

- Use clear, simple language
- Include examples where helpful
- Keep code blocks properly formatted
- Use headers to organize content

## Getting Help

- Open an issue on GitHub
- Join the discussion in pull requests
- Contact the maintainer directly

## Recognition

Contributors will be recognized in the README and release notes. Significant contributions may be highlighted separately.

Thank you for helping make Ka better!