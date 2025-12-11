import flet as ft
import os
import json
from pathlib import Path


class ConfigDialog(ft.Column):
    def __init__(self, page: ft.Page, on_save_callback=None):
        super().__init__()
        self.page = page
        self.on_save_callback = on_save_callback
        self.expand = True

        self.api_key = ft.TextField(
            label="API Key",
            width=400,
            password=True,
            can_reveal_password=True
        )

        self.secret_key = ft.TextField(
            label="Secret Key",
            width=400,
            password=True,
            can_reveal_password=True
        )

        self.passphrase = ft.TextField(
            label="Passphrase",
            width=400,
            password=True,
            can_reveal_password=True
        )

        self.demo_mode = ft.Checkbox(
            label="Демо режим (testnet)",
            value=True
        )

        self.test_connection_btn = ft.ElevatedButton(
            "Проверить подключение",
            on_click=self.test_connection,
            icon=ft.Icons.CONNECTED_TV
        )

        self.save_btn = ft.ElevatedButton(
            "Сохранить и запустить",
            on_click=self.save_config,
            icon=ft.Icons.SAVE,
            disabled=True
        )

        self.connection_status = ft.Text("Введите данные API", color=ft.Colors.GREY)

        self.controls = [
            ft.Text("Настройка подключения к OKX", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Получите API ключи на сайте OKX:", size=12, color=ft.Colors.GREY),
            ft.Divider(),
            self.api_key,
            self.secret_key,
            self.passphrase,
            self.demo_mode,
            ft.Divider(),
            ft.Row([
                self.test_connection_btn,
                self.save_btn
            ], spacing=20),
            ft.Container(
                content=self.connection_status,
                padding=10,
                bgcolor=ft.Colors.SURFACE,
                border_radius=5
            ),
            ft.Text("Примечание: ключи хранятся только локально в файле .env",
                    size=10, color=ft.Colors.GREY)
        ]

        self.load_existing_config()

    def load_existing_config(self):
        """Загрузка существующей конфигурации"""
        try:
            from okx_client.config import Config
            if Config.API_KEY and Config.API_KEY != "your_api_key_here":
                self.api_key.value = Config.API_KEY
                self.secret_key.value = Config.API_SECRET
                self.passphrase.value = Config.PASSPHRASE
                self.demo_mode.value = Config.DEMO_MODE
                self.test_connection_btn.disabled = False
        except:
            pass

    def test_connection(self, e):
        """Тестирование подключения"""
        if not all([self.api_key.value, self.secret_key.value, self.passphrase.value]):
            self.connection_status.value = "❌ Заполните все поля"
            self.connection_status.color = ft.Colors.RED
            self.page.update()
            return

        self.connection_status.value = "⏳ Проверка подключения..."
        self.connection_status.color = ft.Colors.BLUE
        self.test_connection_btn.disabled = True
        self.page.update()

        try:
            from okx_client.client import OKXClient
            client = OKXClient(
                api_key=self.api_key.value,
                secret_key=self.secret_key.value,
                passphrase=self.passphrase.value,
                demo_mode=self.demo_mode.value
            )

            # Пробуем получить баланс
            result = client.account.get_balance()
            if result and result.get('code') == '0':
                self.connection_status.value = f"✅ Подключение успешно! Режим: {'Демо' if self.demo_mode.value else 'Реальный'}"
                self.connection_status.color = ft.Colors.GREEN
                self.save_btn.disabled = False
            else:
                self.connection_status.value = f"⚠️ Ошибка: {result.get('msg', 'Неизвестная ошибка')}"
                self.connection_status.color = ft.Colors.ORANGE

        except Exception as ex:
            self.connection_status.value = f"❌ Ошибка подключения: {str(ex)}"
            self.connection_status.color = ft.Colors.RED

        self.test_connection_btn.disabled = False
        self.page.update()

    def save_config(self, e):
        """Сохранение конфигурации"""
        config_data = {
            "API_KEY": self.api_key.value,
            "API_SECRET": self.secret_key.value,
            "PASSPHRASE": self.passphrase.value,
            "DEMO_MODE": str(self.demo_mode.value),
            "DATABASE_URL": "sqlite:///okx_data.db"
        }

        # Создаем папку dashboard если её нет
        Path("dashboard").mkdir(exist_ok=True)

        # Сохраняем в .env
        env_path = os.path.join("dashboard", ".env")
        with open(env_path, 'w') as f:
            for key, value in config_data.items():
                f.write(f"{key}={value}\n")

        # Сохраняем в config.json для удобства
        config_path = os.path.join("dashboard", "config.json")
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)

        # Также сохраняем в корневой .env для обратной совместимости
        with open('.env', 'w') as f:
            for key, value in config_data.items():
                f.write(f"{key}={value}\n")

        # Показываем уведомление
        self.page.show_snack_bar(
            ft.SnackBar(ft.Text("Конфигурация сохранена!"))
        )

        # Вызываем callback если есть
        if self.on_save_callback:
            self.on_save_callback()
