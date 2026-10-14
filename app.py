import flet as ft

from components import (
    ActionButton,
    InputField,
    LabelText,
    MainColumn,
    MainRow,
    ToggleSwitch,
    TitleText,
)
from entities import Macro
from redactor import Redactor
from runner import runner
from session import session
from storage import Storage


class Menu:

    def __init__(self, page):
        self._page = page
        self._storage = Storage()
        self._macros = self._storage.load()
        self._toggle_button = ActionButton("выключить" if runner.running else "включить")
        self._toggle_button.on_click = self.toggle_runner
        self._status = LabelText("")
        self._list_column = MainColumn(spacing=10, expand=True)

    @property
    def page(self):
        return self._page

    @property
    def storage(self):
        return self._storage

    @property
    def macros(self):
        return self._macros

    @macros.setter
    def macros(self, value):
        self._macros = list(value)

    def show(self):
        self._page.title = "menu"
        self._page.clean()
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.refresh()
        self._page.add(
            MainRow(
                controls=[
                    ActionButton("добавить макрос", on_click=self.add_macro),
                    self._toggle_button,
                    ActionButton("закрыть", on_click=self.close_app),
                ],
            ),
            MainRow(
                controls=[self._list_column],
                alignment=ft.MainAxisAlignment.START,
            ),
            self._status,
        )

    def refresh(self):
        self._list_column.controls.clear()
        for macro in self._macros:
            self._list_column.controls.append(self.make_macro_row(macro))
        self._page.update()

    def make_macro_row(self, macro):
        return MainRow(
            controls=[
                ActionButton("удалить", on_click=lambda e, m=macro: self.remove_macro(m)),
                ActionButton("изменить", on_click=lambda e, m=macro: self.open_editor(m)),
                InputField(
                    value=macro.name,
                    label="макрос",
                    width=200,
                    on_change=lambda e, m=macro: self.rename_macro(m, e.control.value),
                ),
                InputField(
                    value=macro.hotkey,
                    label="сочетание",
                    width=200,
                    on_change=lambda e, m=macro: self.rebind_macro(m, e.control.value),
                ),
                ToggleSwitch(
                    value=macro.enabled,
                    label="включено",
                    on_change=lambda e, m=macro: self.set_enabled(m, e.control.value),
                ),
            ],
        )

    def toggle_runner(self, e):
        if runner.running:
            runner.stop()
            self._toggle_button.set_text("включить")
            self._status.value = ""
        else:
            if not runner.available:
                self._status.value = "модуль keyboard недоступен"
                self._page.update()
                return
            runner.start(self._macros)
            if runner.errors:
                self._status.value = "ошибки: " + "; ".join(runner.errors)
            else:
                self._status.value = "макросы активны"
            self._toggle_button.set_text("выключить")
        self._page.update()

    def open_editor(self, macro):
        def back():
            self._storage.save(self._macros)
            runner.update(self._macros)
            self.show()
        Redactor(self._page, macro, on_back=back).show()

    def add_macro(self, e):
        macro = Macro("новый_макрос", "", False, [])
        self._macros.append(macro)
        self._storage.save(self._macros)
        runner.update(self._macros)
        self.open_editor(macro)

    def rename_macro(self, macro, value):
        macro.name = value

    def rebind_macro(self, macro, value):
        macro.hotkey = value

    def set_enabled(self, macro, value):
        macro.enabled = value
        self._storage.save(self._macros)
        runner.update(self._macros)

    def remove_macro(self, macro):
        if macro in self._macros:
            self._macros.remove(macro)
        self._storage.save(self._macros)
        runner.update(self._macros)
        self.show()

    async def close_app(self, e):
        runner.stop()
        self._storage.save(self._macros)
        session.finish()
        await self._page.window.close()


def menu(page):
    session.start()
    Menu(page).show()