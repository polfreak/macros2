import threading

from entities import CustomMap

try:
    import keyboard
except ImportError:
    keyboard = None


class MacroRunner:

    def __init__(self):
        self._handles = []
        self._running = False
        self._lock = threading.Lock()
        self._macros = []
        self._errors = []
        self._hotkey_map = CustomMap()

    @property
    def running(self):
        return self._running

    @property
    def available(self):
        return keyboard is not None

    @property
    def errors(self):
        return list(self._errors)

    @property
    def hotkey_map(self):
        return self._hotkey_map

    @property
    def macros(self):
        return list(self._macros)

    def start(self, macros):
        with self._lock:
            if self._running or keyboard is None:
                return
            self._macros = list(macros)
            self._errors = []
            self._hotkey_map = CustomMap()
            self._running = True
            self._register_all()

    def stop(self):
        with self._lock:
            if not self._running:
                return
            self._unregister_all()
            self._running = False

    def update(self, macros):
        with self._lock:
            self._macros = list(macros)
            if not self._running:
                return
            self._unregister_all()
            self._hotkey_map = CustomMap()
            self._register_all()

    def _register_all(self):
        for macro in self._macros:
            if not macro.hotkey:
                continue
            handler = self._make_handler(macro)
            try:
                handle = keyboard.add_hotkey(macro.hotkey, handler, suppress=False)
                self._handles.append(handle)
                self._hotkey_map.set(macro.hotkey, macro)
            except Exception as error:
                self._errors.append(str(error))

    def _unregister_all(self):
        for handle in self._handles:
            try:
                keyboard.remove_hotkey(handle)
            except Exception:
                pass
        self._handles.clear()

    def _make_handler(self, macro):
        def handler():
            if not self._running:
                return
            if not macro.enabled:
                return
            for command in macro.commands:
                if not command.value:
                    continue
                try:
                    keyboard.press_and_release(command.value)
                except Exception:
                    pass
        return handler


runner = MacroRunner()