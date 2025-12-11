# main.py
import flet as ft
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('okx_dashboard.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """Проверка необходимых зависимостей"""
    try:
        import flet
        import okx
        import sqlalchemy
        import pandas
        import plotly
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Не установлена зависимость: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False


def main(page: ft.Page):
    """Основная функция приложения"""
    try:
        from ui.main_app import OKXDesktopApp
        app = OKXDesktopApp(page)

    except Exception as e:
        logger.error(f"Ошибка запуска приложения: {e}", exc_info=True)
        page.add(ft.Text(f"Критическая ошибка: {str(e)}", color=ft.Colors.RED))
        page.update()


if __name__ == "__main__":
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)

    # Запускаем Flet приложение
    ft.app(
        target=main,
        view=ft.AppView.FLET_APP,
        assets_dir="assets"
    )
