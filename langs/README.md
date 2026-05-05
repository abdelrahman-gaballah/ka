# Language Files for Ka

This directory contains language definition files for Ka. Each file defines a language and all its commands.

## File Structure

Each language file is a JSON file with the following structure:

```json
{
  "language": "en",
  "name": "English",
  "categories": {
    "category_id": {
      "name": "Display Name of Category",
      "commands": {
        "command_name": {
          "cmd": "actual system command",
          "description": "Short description of what the command does",
          "args": 0
        }
      }
    }
  }
}
```

## Fields Explanation

| Field | Type | Description |
|-------|------|-------------|
| `language` | string | Language code (e.g., 'en', 'ar', 'fr') |
| `name` | string | Display name of the language |
| `categories` | object | Container for all command categories |
| `categories.{id}.name` | string | Display name of the category |
| `categories.{id}.commands` | object | Commands belonging to this category |
| `commands.{name}.cmd` | string | The actual shell command to execute |
| `commands.{name}.description` | string | Human-readable description |
| `commands.{name}.args` | integer | Number of required arguments (0 for no args) |

## Argument Placeholders

Use `{}` as a placeholder for user arguments:

- `"cmd": "cp {} {}"` - expects 2 arguments
- `"cmd": "echo {}"` - expects 1 argument
- `"args": 2` must match the number of `{}` placeholders

## Adding a New Language

1. Copy `template.json` to `{language_code}.json` (e.g., `fr.json`)
2. Change `"language"` and `"name"` fields
3. Translate all `description` fields
4. Keep command names in English (they are the shortcuts)
5. Save the file

## Example: Adding French (fr.json)

```json
{
  "language": "fr",
  "name": "Français",
  "categories": {
    "system_info": {
      "name": "Informations Système",
      "commands": {
        "space": {
          "cmd": "df -h",
          "description": "Afficher l'utilisation du disque",
          "args": 0
        }
      }
    }
  }
}
```

## Testing a Language File

After creating a language file, test it with:

```bash
python -m json.tool langs/your_lang.json
```

Then set it in `config.json`:

```json
{
  "language": "your_lang"
}
```

## Current Languages

| File | Language | Status |
|------|----------|--------|
| `en.json` | English | Complete |
| `ar.json` | العربية | Complete |
| `template.json` | Template | For reference |

## Contributing

To add a new language, create a pull request with the new file. Please ensure all descriptions are translated and the JSON is valid.
```