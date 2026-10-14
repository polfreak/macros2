from datetime import datetime
from pathlib import Path

from entities import ReportEntry


class Reporter:

    def __init__(self, folder_name="macro", file_name="report.txt"):
        self._folder = Path(__file__).parent / folder_name
        self._file = self._folder / file_name
        self._entries = []
        self._user = None
        self._time_in = None

    @property
    def entries(self):
        return list(self._entries)

    @property
    def user(self):
        return self._user

    @property
    def folder(self):
        return self._folder

    @property
    def file(self):
        return self._file

    def set_user(self, user):
        self._user = user
        self._time_in = datetime.now()

    def finish(self):
        if self._user is None:
            return
        entry = ReportEntry(self._user.login, self._time_in, datetime.now())
        self._entries.append(entry)
        self._write()

    def _write(self):
        self._folder.mkdir(parents=True, exist_ok=True)

        fmt = ReportEntry.format_time
        lines = []
        for entry in self._entries:
            lines.append(f"{entry.login} {fmt(entry.time_in)} {fmt(entry.time_out)}")

        self._file.write_text("\n".join(lines), encoding="utf-8")


reporter = Reporter()