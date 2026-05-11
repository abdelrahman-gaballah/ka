import json
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).parent.parent.absolute()

_BUILTIN_LANGS = frozenset({'en', 'ar'})


class LanguageManager:
    def __init__(self):
        self.langs_dir = PROJECT_ROOT / "langs"
        self.available_langs = self._scan_available_languages()

    def _scan_available_languages(self) -> Dict[str, str]:
        languages = {}
        if not self.langs_dir.exists():
            return languages
        for lang_file in self.langs_dir.glob("*.json"):
            if lang_file.name == "template.json":
                continue
            lang_code = lang_file.stem
            try:
                data = json.loads(lang_file.read_text(encoding='utf-8'))
                languages[lang_code] = data.get('name', lang_code)
            except (json.JSONDecodeError, IOError):
                pass
        return languages

    def get_language_name(self, lang_code: str) -> str:
        return self.available_langs.get(lang_code, lang_code)

    def get_current_language(self, config: Dict) -> str:
        lang = config.get('language', 'en')
        return lang if lang in self.available_langs else 'en'

    def list_languages(self) -> List[Dict[str, str]]:
        return [{'code': code, 'name': name} for code, name in self.available_langs.items()]

    def load_language_file(self, lang_code: str) -> Dict:
        lang_path = self.langs_dir / f"{lang_code}.json"
        try:
            return json.loads(lang_path.read_text(encoding='utf-8'))
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def create_language_template(self, lang_code: str, lang_name: str) -> bool:
        template_path = self.langs_dir / "template.json"
        if not template_path.exists():
            return False
        try:
            template = json.loads(template_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            return False
        template['language'] = lang_code
        template['name'] = lang_name
        try:
            (self.langs_dir / f"{lang_code}.json").write_text(
                json.dumps(template, indent=2, ensure_ascii=False), encoding='utf-8')
            return True
        except IOError:
            return False

    def delete_language(self, lang_code: str) -> bool:
        if lang_code in _BUILTIN_LANGS:
            return False
        lang_path = self.langs_dir / f"{lang_code}.json"
        if not lang_path.exists():
            return False
        try:
            lang_path.unlink()
            return True
        except IOError:
            return False

    def get_command_translation(self, lang_code: str, command_name: str, field: str = 'cmd') -> Optional[str]:
        lang_data = self.load_language_file(lang_code)
        for category in lang_data.get('categories', {}).values():
            for cmd, cmd_data in category.get('commands', {}).items():
                if cmd == command_name:
                    return cmd_data.get(field)
        return None


def get_language_list() -> List[str]:
    return list(LanguageManager().available_langs.keys())


def is_language_available(lang_code: str) -> bool:
    return lang_code in LanguageManager().available_langs
