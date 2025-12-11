# ui/trading_view.py
import flet as ft


class TradingView(ft.Column):
    def __init__(self, okx_client):
        super().__init__()
        self.okx_client = okx_client
        self.expand = True

        # Выбор инструмента
        self.instrument_dropdown = ft.Dropdown(
            label="Инструмент",
            width=200,
            options=[],
            on_change=self.on_instrument_change
        )

        # Информация об инструменте
        self.instrument_info = ft.Text("Выберите инструмент", size=12, color=ft.Colors.GREY)

        # Форма для ордера
        self.order_type = ft.Dropdown(
            label="Тип ордера",
            options=[
                ft.dropdown.Option("market", "Рыночный"),
                ft.dropdown.Option("limit", "Лимитный"),
                ft.dropdown.Option("post_only", "Post Only"),
            ],
            value="limit",
            width=150
        )

        self.side = ft.SegmentedButton(
            selected={"buy"},
            segments=[
                ft.Segment(value="buy", label=ft.Row([
                    ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.GREEN),
                    ft.Text("Купить")
                ])),
                ft.Segment(value="sell", label=ft.Row([
                    ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.RED),
                    ft.Text("Продать")
                ])),
            ],
        )

        self.quantity = ft.TextField(
            label="Количество",
            width=150,
            suffix_text="BTC"
        )

        self.price = ft.TextField(
            label="Цена",
            width=150,
            value="0.0",
            suffix_text="USDT"
        )

        self.total_cost = ft.Text("Стоимость: $0.00", size=12)

        self.place_order_btn = ft.ElevatedButton(
            "Разместить ордер",
            icon=ft.Icons.SEND,
            on_click=self.place_order,
            bgcolor=ft.Colors.GREEN,
            style=ft.ButtonStyle(padding=20)
        )

        self.controls = [
            ft.Text("Торговля", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.instrument_dropdown,
                ft.Container(self.instrument_info, padding=10)
            ]),
            ft.Divider(),
            ft.Text("Новый ордер", size=18),
            ft.Row([
                ft.Column([
                    ft.Text("Тип ордера"),
                    self.order_type,
                ]),
                ft.Column([
                    ft.Text("Направление"),
                    self.side,
                ]),
                ft.Column([
                    ft.Text("Количество"),
                    self.quantity,
                ]),
                ft.Column([
                    ft.Text("Цена"),
                    self.price,
                ]),
                ft.Column([
                    ft.Text(" "),
                    self.total_cost,
                ]),
            ], wrap=True, spacing=20),
            ft.Container(self.place_order_btn, padding=20),
            ft.Divider(),
            ft.Text("Активные ордера", size=18),
            ft.Container(
                content=ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Инструмент")),
                        ft.DataColumn(ft.Text("Сторона")),
                        ft.DataColumn(ft.Text("Цена")),
                        ft.DataColumn(ft.Text("Количество")),
                        ft.DataColumn(ft.Text("Статус")),
                        ft.DataColumn(ft.Text("Действия")),
                    ],
                    rows=[],
                ),
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=10,
                padding=10,
            )
        ]

        # Обновляем расчет стоимости при изменении
        self.quantity.on_change = self.calculate_total
        self.price.on_change = self.calculate_total

        self.load_instruments()

    def on_instrument_change(self, e):
        """Обработчик изменения инструмента"""
        inst_id = self.instrument_dropdown.value
        if inst_id:
            self.quantity.suffix_text = inst_id.split('-')[0]  # BTC из BTC-USDT
            self.price.suffix_text = inst_id.split('-')[1]  # USDT из BTC-USDT
            self.update_ticker_info(inst_id)

    def calculate_total(self, e):
        """Расчет общей стоимости"""
        try:
            qty = float(self.quantity.value or 0)
            price = float(self.price.value or 0)
            total = qty * price
            self.total_cost.value = f"Стоимость: ${total:.2f}"
            self.update()
        except:
            self.total_cost.value = "Стоимость: $0.00"
            self.update()

    def load_instruments(self):
        """Загрузка доступных инструментов"""
        try:
            result = self.okx_client.public.get_instruments(instType="SPOT")
            if result and result.get('code') == '0':
                instruments = result.get('data', [])
                options = []
                for inst in instruments[:50]:  # Первые 50 инструментов
                    if inst['instId'].endswith('-USDT'):
                        options.append(
                            ft.dropdown.Option(inst['instId'])
                        )
                self.instrument_dropdown.options = options
                if options:
                    self.instrument_dropdown.value = options[0].key
                    self.on_instrument_change(None)
                self.update()
        except Exception as e:
            print(f"Ошибка загрузки инструментов: {e}")

    def update_ticker_info(self, inst_id):
        """Обновление информации о тикере"""
        try:
            result = self.okx_client.public.get_ticker(instId=inst_id)
            if result and result.get('code') == '0':
                ticker = result.get('data', [{}])[0]
                self.instrument_info.value = f"Последняя цена: {ticker.get('last', 'N/A')} | 24h Изм: {ticker.get('vol24h', 'N/A')}"
                if not self.price.value or self.price.value == "0.0":
                    self.price.value = ticker.get('last', '0.0')
                self.update()
        except Exception as e:
            print(f"Ошибка получения тикера: {e}")

    def place_order(self, e):
        """Размещение ордера"""
        if not all([self.instrument_dropdown.value, self.quantity.value]):
            e.page.show_snack_bar(
                ft.SnackBar(ft.Text("Заполните все поля"))
            )
            return

        try:
            # Определяем сторону
            side = list(self.side.selected)[0] if self.side.selected else "buy"

            order_data = {
                "instId": self.instrument_dropdown.value,
                "tdMode": "cash",  # Spot trading
                "side": side,
                "ordType": self.order_type.value,
                "sz": self.quantity.value,
            }

            if self.order_type.value == "limit":
                order_data["px"] = self.price.value

            # Используем trader (TradeManager) из вашего клиента
            result = self.okx_client.trader.place_order(**order_data)

            if result and result.get('code') == '0':
                ord_id = result['data'][0]['ordId']
                e.page.show_snack_bar(
                    ft.SnackBar(
                        ft.Text(f"Ордер размещен: {ord_id}"),
                        bgcolor=ft.Colors.GREEN
                    )
                )

                # Сброс формы
                self.quantity.value = ""
                self.price.value = "0.0"
                self.total_cost.value = "Стоимость: $0.00"
                self.update()

            else:
                msg = result.get('msg', 'Unknown error') if result else 'No response'
                e.page.show_snack_bar(
                    ft.SnackBar(
                        ft.Text(f"Ошибка: {msg}"),
                        bgcolor=ft.Colors.RED
                    )
                )

        except Exception as ex:
            e.page.show_snack_bar(
                ft.SnackBar(
                    ft.Text(f"Ошибка: {str(ex)}"),
                    bgcolor=ft.Colors.RED
                )
            )
