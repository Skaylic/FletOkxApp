# ui/components/widgets.py
import flet as ft
from typing import Callable, Dict, List, Optional
from datetime import datetime


class StatusIndicator:
    """Индикатор статуса подключения"""

    def __init__(self):
        self.status = "disconnected"
        self.color_map = {
            "connected": ft.Colors.GREEN,
            "connecting": ft.Colors.YELLOW,
            "disconnected": ft.Colors.RED,
            "error": ft.Colors.RED_700
        }

    def build(self):
        self.container = ft.Container(
            width=12,
            height=12,
            border_radius=6,
            bgcolor=self.color_map[self.status],
            tooltip=self.get_tooltip()
        )
        return ft.Row([
            self.container,
            ft.Text(self.get_status_text(), size=12)
        ], spacing=5)

    def set_status(self, status: str):
        self.status = status
        self.container.bgcolor = self.color_map.get(status, ft.Colors.GREY)
        self.container.tooltip = self.get_tooltip()

    def get_tooltip(self):
        return {
            "connected": "Подключено",
            "connecting": "Подключение...",
            "disconnected": "Не подключено",
            "error": "Ошибка подключения"
        }.get(self.status, "Неизвестный статус")

    def get_status_text(self):
        return {
            "connected": "Online",
            "connecting": "Connecting...",
            "disconnected": "Offline",
            "error": "Error"
        }.get(self.status, "Unknown")


class MetricCard:
    """Карточка с метрикой"""

    def __init__(self, title: str, value: str, icon: str = None, color: ft.Colors = None):
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color or ft.Colors.BLUE

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(self.icon, color=self.color) if self.icon else ft.Container(),
                        ft.Text(self.title, size=14, color=ft.Colors.GREY)
                    ]),
                    ft.Text(self.value, size=24, weight=ft.FontWeight.BOLD)
                ]),
                padding=20
            )
        )

    def update_value(self, value: str, color: ft.Colors = None):
        pass  # Реализация обновления значения


class DataTableWidget:
    """Виджет таблицы данных"""

    def __init__(self, headers: List[str], data: List[Dict]):
        self.headers = headers
        self.data = data

    def build(self):
        columns = [ft.DataColumn(ft.Text(header)) for header in self.headers]
        rows = []

        for item in self.data:
            cells = []
            for header in self.headers:
                value = item.get(header, "")
                cells.append(ft.DataCell(ft.Text(str(value))))
            rows.append(ft.DataRow(cells=cells))

        return ft.Container(
            content=ft.DataTable(
                columns=columns,
                rows=rows,
                horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_800),
                vertical_lines=ft.BorderSide(1, ft.Colors.GREY_800)
            ),
            border_radius=5,
            padding=5
        )

    def update_data(self, data: List[Dict]):
        self.data = data
        # Здесь должна быть логика обновления таблицы


class OrderForm:
    """Форма ордера"""

    def __init__(self, on_place_order: Callable, on_cancel_all: Callable):
        self.on_place_order = on_place_order
        self.on_cancel_all = on_cancel_all

    def build(self):
        # Здесь реализация формы ордера
        return ft.Container(
            content=ft.Column([
                ft.Text("Новый ордер", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                # Поля формы
                ft.TextField(label="Цена"),
                ft.TextField(label="Количество"),
                ft.Dropdown(label="Тип ордера", options=[
                    ft.dropdown.Option("limit", "Лимитный"),
                    ft.dropdown.Option("market", "Рыночный")
                ]),
                ft.Row([
                    ft.ElevatedButton("Купить", color=ft.Colors.GREEN),
                    ft.ElevatedButton("Продать", color=ft.Colors.RED),
                    ft.ElevatedButton("Отмена всех", on_click=lambda e: self.on_cancel_all())
                ])
            ]),
            padding=20,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE
        )


class InstrumentSelector:
    """Селектор инструмента"""

    def __init__(self, on_instrument_select: Callable):
        self.on_instrument_select = on_instrument_select

    def build(self):
        return ft.Dropdown(
            label="Выберите инструмент",
            width=300,
            options=[],
            on_change=self.on_change
        )

    def on_change(self, e):
        self.on_instrument_select(e.control.value)

    def update_instruments(self, instruments: List[str]):
        self.options = [
            ft.dropdown.Option(inst, inst) for inst in instruments
        ]
