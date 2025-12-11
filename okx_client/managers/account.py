#okx_client/managers/account.py
"""
Менеджер для работы с данными аккаунта OKX API
"""
from typing import Dict, Optional


class AccountManager:
    """Управление данными аккаунта"""

    def __init__(self, account_api):
        self.account = account_api

    def get_balance(self, ccy: Optional[str] = None) -> Dict:
        """
        Получение баланса

        Args:
            ccy: Код валюты (например, 'BTC', 'USDT')
        """
        try:
            print(f"📊 Запрос баланса (ccy: {ccy})...")

            if ccy:
                result = self.account.get_account_balance(ccy=ccy)
            else:
                result = self.account.get_account_balance()

            if result.get('code') == '0':
                print("✓ Баланс получен успешно")
                return result
            else:
                error_msg = result.get('msg', 'Неизвестная ошибка')
                error_code = result.get('code', 'N/A')
                print(f"✗ Ошибка API при запросе баланса: Код {error_code}, {error_msg}")
                return result

        except TypeError as e:
            if "encoding without a string argument" in str(e):
                print("✗ КРИТИЧЕСКАЯ ОШИБКА: Проблема с секретным ключом")
            return {'code': '-1', 'msg': f"TypeError: {str(e)}"}
        except Exception as e:
            print(f"✗ Неожиданная ошибка при запросе баланса: {e}")
            return {'code': '-1', 'msg': str(e)}

    def get_positions(self, inst_type: str = "SWAP") -> Dict:
        """Получение позиций"""
        try:
            result = self.account.get_positions(instType=inst_type)
            return result
        except Exception as e:
            print(f"✗ Ошибка при запросе позиций: {e}")
            return {'code': '-1', 'msg': str(e)}

    def get_account_config(self) -> Dict:
        """Получение конфигурации аккаунта"""
        try:
            return self.account.get_account_config()
        except Exception as e:
            print(f"✗ Ошибка при запросе конфигурации аккаунта: {e}")
            return {'code': '-1', 'msg': str(e)}
