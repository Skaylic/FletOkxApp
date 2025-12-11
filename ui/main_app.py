# ui/main_app.py
import flet as ft
import logging
from datetime import datetime
import importlib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


class OKXDesktopApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "OKX Dashboard"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.width = 1400
        self.page.window.height = 900
        self.page.window.min_width = 1200
        self.page.window.min_height = 800

        self.okx_client = None
        self.initialize_ui()
        self.check_and_init_client()

    def check_and_init_client(self):
        """Проверка и инициализация клиента"""
        try:
            from okx_client.config import Config
            from okx_client.client import OKXClient

            # Проверяем наличие конфигурации
            if not Config.API_KEY or not Config.API_SECRET or not Config.PASSPHRASE:
                self.show_config_dialog()
                return

            # Инициализируем клиента
            self.okx_client = OKXClient()

            # Перезагружаем интерфейс с клиентом
            self.initialize_main_interface()

        except Exception as e:
            logger.error(f"Ошибка инициализации клиента: {e}")
            self.show_error_dialog(f"Ошибка инициализации: {str(e)}")
            self.show_config_dialog()

    def initialize_ui(self):
        """Начальная инициализация UI (до клиента)"""
        self.appbar = ft.AppBar(
            title=ft.Text("OKX Trading Dashboard"),
            center_title=False,
            bgcolor=ft.Colors.SURFACE,
        )

        self.content_area = ft.Container(
            content=ft.Column([
                ft.ProgressRing(),
                ft.Text("Инициализация...")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            alignment=ft.alignment.center
        )

        self.page.add(self.appbar, self.content_area)
        self.page.update()

    def initialize_main_interface(self):
        """Инициализация основного интерфейса после получения клиента"""
        # Очищаем страницу
        self.page.clean()

        # Обновляем AppBar
        self.appbar.actions = [
            ft.IconButton(ft.Icons.REFRESH, on_click=self.refresh_data),
            ft.IconButton(ft.Icons.SETTINGS, on_click=self.open_settings),
            ft.IconButton(ft.Icons.ACCOUNT_CIRCLE),
        ]

        # Навигационная панель
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD,
                    selected_icon=ft.Icons.DASHBOARD_OUTLINED,
                    label="Дашборд"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.ACCOUNT_BALANCE,
                    selected_icon=ft.Icons.ACCOUNT_BALANCE_OUTLINED,
                    label="Аккаунт"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.TRENDING_UP,
                    selected_icon=ft.Icons.TRENDING_UP_OUTLINED,
                    label="Рынок"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SHOPPING_CART,
                    selected_icon=ft.Icons.SHOPPING_CART_OUTLINED,
                    label="Торговля"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.LIST_ALT,
                    selected_icon=ft.Icons.LIST_ALT_OUTLINED,
                    label="Ордера"
                ),
            ],
            on_change=self.on_nav_change
        )

        # Статус бар
        self.status_bar = ft.Container(
            content=ft.Row([
                ft.Text("✅ Подключено", color=ft.Colors.GREEN),
                ft.Divider(height=20),
                ft.Text("Последнее обновление: --:--:--"),
                ft.Divider(height=20),
                ft.Text(f"Режим: {'Тестовый' if self.okx_client.demo_mode else 'Рабочий'}"),
            ], alignment=ft.MainAxisAlignment.START),
            padding=10,
            bgcolor=ft.Colors.SURFACE,
            height=40
        )

        # Основной контент
        self.content_area = ft.Container(
            expand=True,
            padding=20
        )

        # Загружаем начальный view
        self.load_dashboard()

        # Собираем layout
        self.page.add(
            self.appbar,
            ft.Row([
                self.nav_rail,
                ft.VerticalDivider(width=1),
                ft.Column([
                    self.content_area,
                    self.status_bar
                ], expand=True)
            ], expand=True)
        )

        self.page.update()

    def on_nav_change(self, e):
        """Обработчик смены раздела"""
        index = e.control.selected_index
        if index == 0:
            self.load_dashboard()
        elif index == 1:
            self.load_account_view()
        elif index == 2:
            self.load_market_view()
        elif index == 3:
            self.load_trading_view()
        elif index == 4:
            self.load_orders_view()

    def load_dashboard(self):
        """Загрузка дашборда"""
        from ui.dashboard import DashboardView
        self.content_area.content = DashboardView(self.okx_client)
        self.page.update()

    def load_account_view(self):
        """Загрузка представления аккаунта"""
        from ui.account_view import AccountView
        self.content_area.content = AccountView(self.okx_client)
        self.page.update()

    def load_market_view(self):
        """Загрузка представления рынка"""
        from ui.market_view import MarketView
        self.content_area.content = MarketView(self.okx_client)
        self.page.update()

    def load_trading_view(self):
        """Загрузка представления торговли"""
        from ui.trading_view import TradingView
        self.content_area.content = TradingView(self.okx_client)
        self.page.update()

    def load_orders_view(self):
        """Загрузка представления ордеров"""
        from ui.orders_view import OrdersView
        self.content_area.content = OrdersView(self.okx_client)
        self.page.update()

    def refresh_data(self, e):
        """Обновление всех данных"""
        self.status_bar.content.controls[2].value = f"Последнее обновление: {datetime.now().strftime('%H:%M:%S')}"
        # Обновляем текущий view
        current_index = self.nav_rail.selected_index
        if current_index == 0:
            self.load_dashboard()
        elif current_index == 1:
            self.load_account_view()
        # ... другие view
        self.page.update()

    def open_settings(self, e):
        """Открытие настроек"""
        from ui.config_dialog import ConfigDialog
        dialog = ConfigDialog(self.page, self.on_config_saved)
        dialog.show()

    def on_config_saved(self):
        """Callback после сохранения конфигурации"""
        # Перезагружаем конфиг и клиента
        importlib.reload(sys.modules['okx_client.config'])
        self.check_and_init_client()

    def show_config_dialog(self):
        """Показать диалог конфигурации"""
        from ui.config_dialog import ConfigDialog
        dialog = ConfigDialog(self.page, self.on_config_saved)
        self.content_area.content = dialog
        self.page.update()

    def show_error_dialog(self, message):
        """Показать диалог с ошибкой"""
        dlg = ft.AlertDialog(
            title=ft.Text("Ошибка"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.page.close(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
