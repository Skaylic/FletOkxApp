# ui/account_view.py

import flet as ft
import pandas as pd
from datetime import datetime


class AccountView(ft.Column):
    def __init__(self, okx_client):
        super().__init__()
        self.okx_client = okx_client
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO

        # Карточки с общей информацией
        self.balance_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Общий баланс", size=12),
                    ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD),
                ], spacing=5),
                padding=20,
            ),
            width=200,
        )

        self.pnl_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Дневной PnL", size=12),
                    ft.Text("$0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                ], spacing=5),
                padding=20,
            ),
            width=200,
        )

        self.positions_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Активные позиции", size=12),
                    ft.Text("0", size=24, weight=ft.FontWeight.BOLD),
                ], spacing=5),
                padding=20,
            ),
            width=200,
        )

        # Таблица балансов
        self.balance_data = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Валюта")),
                ft.DataColumn(ft.Text("Баланс"), numeric=True),
                ft.DataColumn(ft.Text("Доступно"), numeric=True),
                ft.DataColumn(ft.Text("Заморожено"), numeric=True),
                ft.DataColumn(ft.Text("Эквивалент USD"), numeric=True),
            ],
            rows=[],
        )

        self.controls = [
            ft.Row([
                ft.Text("Аккаунт", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "Обновить",
                    icon=ft.Icons.REFRESH,
                    on_click=self.update_account_data
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Row([
                self.balance_card,
                self.pnl_card,
                self.positions_card,
            ], spacing=20),

            ft.Divider(),

            ft.Text("Детали баланса", size=18),
            ft.Container(
                content=self.balance_data,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=10,
                padding=10,
            ),
        ]

        self.update_account_data(None)

    def update_account_data(self, e):
        """Обновление данных аккаунта"""
        try:
            # Получаем баланс через account менеджер
            result = self.okx_client.account.get_balance()

            if result and result.get('code') == '0':
                data = result.get('data', [])
                total_usd = 0
                self.balance_data.rows.clear()

                for account_data in data:
                    for detail in account_data.get('details', []):
                        ccy = detail.get('ccy', '')
                        avail = float(detail.get('availBal', 0))
                        frozen = float(detail.get('frozenBal', 0))
                        balance = float(detail.get('cashBal', avail + frozen))

                        # Для примера считаем что все валюты стоят 1 USD
                        # В реальном приложении нужно получить текущие курсы
                        usd_value = balance
                        total_usd += usd_value

                        if balance > 0 or frozen > 0:
                            self.balance_data.rows.append(
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text(ccy)),
                                    ft.DataCell(ft.Text(f"{balance:.8f}")),
                                    ft.DataCell(ft.Text(f"{avail:.8f}")),
                                    ft.DataCell(ft.Text(f"{frozen:.8f}")),
                                    ft.DataCell(ft.Text(f"${usd_value:.2f}")),
                                ])
                            )

                # Обновляем карточки
                self.balance_card.content.content.controls[1].value = f"${total_usd:.2f}"

                # Получаем информацию о позициях
                positions_result = self.okx_client.account.get_positions()
                if positions_result and positions_result.get('code') == '0':
                    positions = positions_result.get('data', [])
                    active_positions = len([p for p in positions if float(p.get('pos', 0)) > 0])
                    self.positions_card.content.content.controls[1].value = str(active_positions)

                self.update()

                if e:
                    e.page.show_snack_bar(
                        ft.SnackBar(ft.Text("Данные аккаунта обновлены!"))
                    )

            else:
                error_msg = result.get('msg', 'Неизвестная ошибка') if result else 'Нет ответа'
                self.show_error(error_msg)

        except Exception as ex:
            self.show_error(f"Ошибка: {str(ex)}")

    def show_error(self, message):
        """Показать ошибку"""
        # В реальном приложении нужно добавить доступ к page
        print(f"Ошибка: {message}")
