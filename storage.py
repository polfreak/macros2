from pathlib import Path

from entities import Command, Macro


class Storage:

    def __init__(self, folder_name="macro", file_name="macro.txt"):
        self._folder = Path(__file__).parent / folder_name
        self._file = self._folder / file_name

    @property
    def folder(self):
        return self._folder

    @property
    def file(self):
        return self._file

    def _ensure(self):
        self._folder.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def default_lines():
        return [
            "kanami 1 true w w s s a a d d",
            "team ctrl+2 false w a s d w a s d",
        ]

    def load(self):
        self._ensure()
        if not self._file.exists():
            self._file.write_text("\n".join(self.default_lines()), encoding="utf-8")
        text = self._file.read_text(encoding="utf-8")
        macros = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            name = parts[0]
            hotkey = parts[1]
            enabled = parts[2] == "true"
            commands = []
            for token in parts[3:]:
                commands.append(Command(token))
            macros.append(Macro(name, hotkey, enabled, commands))
        return macros

    def save(self, macros):
        self._ensure()
        lines = []
        for macro in macros:
            lines.append(macro.serialize())
        self._file.write_text("\n".join(lines), encoding="utf-8")