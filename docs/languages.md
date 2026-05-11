# Language Support

Ka supports multiple languages for command descriptions and help text. Language files are JSON files in the `langs/` directory.

## Available Languages

| Code | Language | File |
|------|----------|------|
| en | English | `langs/en.json` |
| ar | العربية (Arabic) | `langs/ar.json` |

## How Languages Work

Each language file is a JSON structure with:
- `language`: Language code
- `name`: Display name
- `categories`: Groups of related commands, each containing:
  - `name`: Display name for the category
  - `commands`: Individual commands with `cmd`, `description`, and `args`

### Example Structure

```json
{
  "language": "en",
  "name": "English",
  "categories": {
    "system": {
      "name": "System Information",
      "commands": {
        "space": {
          "cmd": "df -h",
          "description": "Show disk space usage",
          "args": 0
        }
      }
    }
  }
}
```

## Adding a New Language

1. Run `./scripts/create_lang.sh` to generate a file from template
2. Translate all descriptions
3. Validate JSON: `python -m json.tool langs/yourfile.json`
4. Switch to it by setting `"language": "yourcode"` in `config.json`

See `contributing.md` for full contribution guidelines.

## Language File Reference

For detailed field-by-field explanation of the language JSON structure, see `langs/README.md`.
