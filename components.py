from abc import ABC, abstractmethod

import flet as ft


class Component(ABC):

    @abstractmethod
    def component_kind(self):
        pass


class TitleText(ft.Text, Component):

    def __init__(self, value):
        super().__init__(value=value, size=22, weight=ft.FontWeight.BOLD)

    def component_kind(self):
        return "TitleText"


class LabelText(ft.Text, Component):

    def __init__(self, value):
        super().__init__(value=value, size=14)

    def component_kind(self):
        return "LabelText"


class HintText(ft.Text, Component):

    def __init__(self, value):
        super().__init__(value=value, size=12, color=ft.Colors.GREY_500)

    def component_kind(self):
        return "HintText"


class InputField(ft.TextField, Component):

    def __init__(self, value="", label="", width=300, on_change=None):
        super().__init__(value=value, label=label, width=width, on_change=on_change)

    def component_kind(self):
        return "InputField"


class ActionButton(ft.Button, Component):

    def __init__(self, text, on_click=None, width=None):
        super().__init__(
            content=ft.Text(text, color=ft.Colors.WHITE),
            on_click=on_click,
            width=width,
        )

    def set_text(self, text):
        self.content.value = text

    def component_kind(self):
        return "ActionButton"


class ToggleSwitch(ft.Switch, Component):

    def __init__(self, value=False, label="", on_change=None):
        super().__init__(value=value, label=label, on_change=on_change)

    def component_kind(self):
        return "ToggleSwitch"


class MainColumn(ft.Column, Component):

    def __init__(self, controls=None, spacing=10, scroll=ft.ScrollMode.AUTO, expand=False):
        super().__init__(
            controls=controls if controls else [],
            spacing=spacing,
            scroll=scroll,
            expand=expand,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def component_kind(self):
        return "MainColumn"


class MainRow(ft.Row, Component):

    def __init__(self, controls=None, spacing=8, alignment=ft.MainAxisAlignment.START):
        super().__init__(
            controls=controls if controls else [],
            spacing=spacing,
            alignment=alignment,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def component_kind(self):
        return "MainRow"


class Separator(ft.Divider, Component):

    def __init__(self, height=1):
        super().__init__(height=height)

    def component_kind(self):
        return "Separator"


class StatusIcon(ft.Icon, Component):

    def __init__(self, icon_name, color=ft.Colors.GREEN):
        super().__init__(name=icon_name, color=color)

    def component_kind(self):
        return "StatusIcon"


class ProgressIndicator(ft.ProgressBar, Component):

    def __init__(self, value=0.0, width=200):
        super().__init__(value=value, width=width)

    def component_kind(self):
        return "ProgressIndicator"


class InfoBanner(ft.Container, Component):

    def __init__(self, text, color=ft.Colors.BLUE_100):
        super().__init__(
            content=ft.Text(text),
            padding=10,
            bgcolor=color,
            border_radius=5,
        )

    def component_kind(self):
        return "InfoBanner"