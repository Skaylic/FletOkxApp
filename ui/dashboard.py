import flet as ft
from datetime import datetime


class DashboardView(ft.Column):
    def __init__(self, okx_client):
        super().__init__()
        self.okx_client = okx_client
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO

        self.controls = [
            ft.Text("Дашборд", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(f"Добро пожаловать в OKX Dashboard! Время: {datetime.now().strftime('%H:%M:%S')}"),
            ft.Divider(),

            ft.Text("Быстрый доступ", size=18),
            ft.Row([
                ft.ElevatedButton(
                    "Баланс",
                    icon=ft.Icons.ACCOUNT_BALANCE_WALLET,
                    on_click=lambda e: print("Переход к балансу"),
                    width=150,
                    height=100
                ),
                ft.ElevatedButton(
                    "Рынок",
                    icon=ft.Icons.TRENDING_UP,
                    on_click=lambda e: print("Переход к рынку"),
                    width=150,
                    height=100
                ),
                ft.ElevatedButton(
                    "Торговля",
                    icon=ft.Icons.SHOPPING_CART,
                    on_click=lambda e: print("Переход к торговле"),
                    width=150,
                    height=100
                ),
            ], spacing=20),

            ft.Divider(),

            ft.Text("Последние обновления", size=18),
            ft.Container(
                content=ft.Column([
                    ft.Text("• Система инициализирована", color=ft.Colors.GREEN),
                    ft.Text("• Баланс загружен", color=ft.Colors.GREEN),
                    ft.Text("• Готов к работе", color=ft.Colors.GREEN),
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=10,
            ),
        ]
