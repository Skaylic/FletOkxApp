"""
Менеджер для работы с публичными данными OKX API
"""
from typing import Dict, List
from datetime import datetime


class PublicDataManager:
    """Управление публичными данными (без аутентификации)"""

    def __init__(self, public_api, market_api):
        self.public = public_api
        self.market = market_api

    def get_instruments(self, inst_type: str = "SPOT") -> Dict:
        """Получение списка инструментов"""
        try:
            result = self.public.get_instruments(instType=inst_type)
            if result.get('code') == '0':
                print(f"✓ Получено {len(result['data'])} инструментов типа {inst_type}")
                return result
            else:
                print(f"✗ Ошибка получения инструментов: {result.get('msg')}")
                return result
        except Exception as e:
            print(f"✗ Исключение при запросе инструментов: {e}")
            return {'code': '-1', 'msg': str(e), 'data': []}

    def get_candlesticks(self, inst_id: str, bar: str = "1m", limit: int = 100) -> List[List[str]]:
        """Получение свечных данных"""
        try:
            result = self.market.get_candlesticks(instId=inst_id, bar=bar, limit=limit)
            if result.get('code') == '0':
                return result.get('data', [])
            else:
                print(f"✗ Ошибка получения свечей: {result.get('msg')}")
                return []
        except Exception as e:
            print(f"✗ Исключение при запросе свечей: {e}")
            return []

    def get_mark_price(self, inst_type: str, inst_id: str) -> Dict:
        """Получение маркировочной цены"""
        try:
            return self.public.get_mark_price(instType=inst_type, instId=inst_id)
        except Exception as e:
            print(f"✗ Ошибка при запросе маркировочной цены: {e}")
            return {'code': '-1', 'msg': str(e)}

    def get_ticker(self, inst_id: str) -> Dict:
        """Получение информации о тикере"""
        try:
            return self.market.get_ticker(instId=inst_id)
        except Exception as e:
            print(f"✗ Ошибка при запросе тикера: {e}")
            return {'code': '-1', 'msg': str(e)}
