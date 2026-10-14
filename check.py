from pathlib import Path


def _path():
    folder = Path(__file__).parent / 'macro'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / 'macro.txt'


def check():
    file = _path()
    if not file.exists():
        file.write_text('kanami 1 true w w s s a a d d\nteam ctrl+2 false w a s d w a s d\n', encoding='utf-8')
    text = file.read_text(encoding='utf-8')
    return [line.split() for line in text.splitlines() if line.strip()]


def save(macros):
    file = _path()
    file.write_text('\n'.join(' '.join(map(str, m)) for m in macros), encoding='utf-8')