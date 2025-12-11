# ui/orders_view.py
import flet as ft


class OrdersView(ft.Column):
    def __init__(self, okx_client):
        super().__init__()
        self.okx_client = okx_client
        self.expand = True

        self.controls = [
            ft.Text("Ордера", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Здесь будут активные и исторические ордера"),
            # Добавьте таблицу с ордерами
        ]
