from abc import ABC, abstractmethod


class Entity(ABC):

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def validate(self):
        pass


class Command(Entity):

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def serialize(self):
        return self._value

    def validate(self):
        return len(self._value) > 0

    def __eq__(self, other):
        if not isinstance(other, Command):
            return NotImplemented
        return self._value == other._value

    def __lt__(self, other):
        if not isinstance(other, Command):
            return NotImplemented
        return self._value < other._value

    def __hash__(self):
        return hash(self._value)

    def __repr__(self):
        return "Command(" + repr(self._value) + ")"

    def __str__(self):
        return self._value


class Macro(Entity):

    def __init__(self, name, hotkey, enabled=False, commands=None):
        self._name = name
        self._hotkey = hotkey
        self._enabled = bool(enabled)
        if commands is None:
            self._commands = []
        else:
            self._commands = list(commands)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def hotkey(self):
        return self._hotkey

    @hotkey.setter
    def hotkey(self, value):
        self._hotkey = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = bool(value)

    @property
    def commands(self):
        return self._commands

    @commands.setter
    def commands(self, value):
        self._commands = list(value)

    def add_command(self, command):
        self._commands.append(command)

    def remove_command(self, index):
        if 0 <= index < len(self._commands):
            del self._commands[index]

    def serialize(self):
        parts = [self._name, self._hotkey, "true" if self._enabled else "false"]
        for command in self._commands:
            parts.append(command.serialize())
        return " ".join(parts)

    def validate(self):
        return len(self._name) > 0 and len(self._hotkey) > 0

    def __eq__(self, other):
        if not isinstance(other, Macro):
            return NotImplemented
        return self._name == other._name and self._hotkey == other._hotkey

    def __lt__(self, other):
        if not isinstance(other, Macro):
            return NotImplemented
        return self._name < other._name

    def __hash__(self):
        return hash((self._name, self._hotkey))

    def __repr__(self):
        return "Macro(" + repr(self._name) + ", " + repr(self._hotkey) + ")"

    def __str__(self):
        return self._name + " [" + self._hotkey + "]"


class User(Entity):

    def __init__(self, login):
        self._login = login

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    def serialize(self):
        return self._login

    def validate(self):
        return len(self._login) > 0

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self._login == other._login

    def __lt__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self._login < other._login

    def __hash__(self):
        return hash(self._login)

    def __repr__(self):
        return "User(" + repr(self._login) + ")"

    def __str__(self):
        return self._login


class ReportEntry(Entity):

    def __init__(self, login, time_in, time_out=None):
        self._login = login
        self._time_in = time_in
        self._time_out = time_out

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    @staticmethod
    def format_time(value):
        if value is None:
            return ""
        return value.strftime("%d.%m.%Y %H:%M:%S")

    def serialize(self):
        return self._login + " | " + self.format_time(self._time_in) + " | " + self.format_time(self._time_out)

    def validate(self):
        return len(self._login) > 0

    def __eq__(self, other):
        if not isinstance(other, ReportEntry):
            return NotImplemented
        return self._login == other._login

    def __lt__(self, other):
        if not isinstance(other, ReportEntry):
            return NotImplemented
        return self._login < other._login

    def __hash__(self):
        return hash(self._login)

    def __repr__(self):
        return "ReportEntry(" + repr(self._login) + ")"

    def __str__(self):
        return self.serialize()


class CustomMap(Entity):

    def __init__(self):
        self._keys = []
        self._values = []

    def set(self, key, value):
        for i in range(len(self._keys)):
            if self._keys[i] == key:
                self._values[i] = value
                return
        self._keys.append(key)
        self._values.append(value)

    def get(self, key, default=None):
        for i in range(len(self._keys)):
            if self._keys[i] == key:
                return self._values[i]
        return default

    def contains(self, key):
        for k in self._keys:
            if k == key:
                return True
        return False

    def remove(self, key):
        for i in range(len(self._keys)):
            if self._keys[i] == key:
                del self._keys[i]
                del self._values[i]
                return True
        return False

    def keys(self):
        return list(self._keys)

    def values(self):
        return list(self._values)

    def size(self):
        return len(self._keys)

    def serialize(self):
        parts = []
        for i in range(len(self._keys)):
            parts.append(str(self._keys[i]) + "=" + str(self._values[i]))
        return ";".join(parts)

    def validate(self):
        return len(self._keys) == len(self._values)

    def __eq__(self, other):
        if not isinstance(other, CustomMap):
            return NotImplemented
        return self._keys == other._keys and self._values == other._values

    def __lt__(self, other):
        if not isinstance(other, CustomMap):
            return NotImplemented
        return self.size() < other.size()

    def __hash__(self):
        return hash(self.size())

    def __repr__(self):
        return "CustomMap(" + str(self.size()) + ")"

    def __str__(self):
        return self.serialize()