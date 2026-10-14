import flet as ft

from components import (
    ActionButton,
    InputField,
    LabelText,
    MainColumn,
    MainRow,
    TitleText,
)
from entities import Command


class CommandRow(ft.Row):

    def __init__(self, index, command, on_delete, on_change):
        super().__init__()
        self.spacing = 8
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self._index = index
        self._field = InputField(
            value=command.value,
            label="команда " + str(index),
            width=300,
            on_change=lambda e: on_change(index, e.control.value),
        )
        self.controls = [
            self._field,
            ActionButton("удалить", on_click=lambda e: on_delete(index)),
        ]

    @property
    def field(self):
        return self._field

    @property
    def index(self):
        return self._index


class Redactor:

    def __init__(self, page, macro, on_back=None):
        self._page = page
        self._macro = macro
        self._on_back = on_back
        self._name_field = InputField(value=macro.name, label="название", width=400)
        self._hotkey_field = InputField(value=macro.hotkey, label="сочетание", width=400)
        self._commands_column = MainColumn(spacing=10, expand=True)
        self._status = LabelText("")

    @property
    def macro(self):
        return self._macro

    @property
    def page(self):
        return self._page

    def show(self):
        self._page.title = "redactor"
        self._page.clean()
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.refresh()
        self._page.add(
            MainColumn(
                controls=[
                    TitleText("редактор макроса"),
                    self._name_field,
                    self._hotkey_field,
                    self._commands_column,
                    MainRow(
                        controls=[
                            ActionButton("добавить действие", on_click=self.add_command),
                            ActionButton("назад", on_click=self.go_back),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    self._status,
                ],
                spacing=15,
                expand=True,
            )
        )

    def delete_command(self, index):
        self._macro.remove_command(index)
        self.refresh()

    def change_command(self, index, value):
        if 0 <= index < len(self._macro.commands):
            self._macro.commands[index].value = value

    def add_command(self, e):
        self._macro.add_command(Command(""))
        self.refresh()

    def go_back(self, e):
        self._macro.name = self._name_field.value
        self._macro.hotkey = self._hotkey_field.value
        if self._on_back:
            self._on_back()

    def refresh(self):
        self._commands_column.controls.clear()
        for i in range(len(self._macro.commands)):
            self._commands_column.controls.append(
                CommandRow(
                    i,
                    self._macro.commands[i],
                    self.delete_command,
                    self.change_command,
                )
            )
        self._page.update()