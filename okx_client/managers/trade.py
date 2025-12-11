"""
Менеджер для торговых операций OKX API
"""
from datetime import datetime
from typing import Dict, Optional
from sqlalchemy.orm import Session

from okx_client.models import Order


class TradeManager:
    """Управление торговыми операциями"""

    def __init__(self, trade_api, db_session: Session):
        self.trade = trade_api
        self.db = db_session

    def place_order(self, inst_id: str, td_mode: str, side: str,
                    ord_type: str, sz: str, px: Optional[str] = None,
                    cl_ord_id: Optional[str] = None) -> Dict:
        """Размещение ордера"""
        params = {
            'instId': inst_id,
            'tdMode': td_mode,
            'side': side,
            'ordType': ord_type,
            'sz': sz,
        }

        if px and ord_type == 'limit':
            params['px'] = px
        if cl_ord_id:
            params['clOrdId'] = cl_ord_id

        print(f"📝 Размещение ордера: {params}")

        try:
            result = self.trade.place_order(**params)

            if result.get('code') == '0' and result.get('data'):
                self._save_order_to_db(result['data'][0], inst_id, side, ord_type, sz, px)

            return result
        except Exception as e:
            print(f"✗ Ошибка при размещении ордера: {e}")
            return {'code': '-1', 'msg': str(e)}

    def _save_order_to_db(self, order_data: Dict, symbol: str,
                          side: str, order_type: str, quantity: str,
                          price: Optional[str] = None):
        """Сохранение ордера в базу данных"""
        try:
            order = Order(
                order_id=order_data.get('ordId', 'N/A'),
                symbol=symbol,
                side=side,
                order_type=order_type,
                price=float(price) if price else None,
                quantity=float(quantity),
                status=order_data.get('state', 'pending')
            )
            self.db.add(order)
            self.db.commit()
            print(f"💾 Ордер {order.order_id} сохранен в БД")
        except Exception as e:
            print(f"✗ Ошибка сохранения ордера в БД: {e}")
            self.db.rollback()

    def get_order_details(self, inst_id: str, ord_id: str) -> Dict:
        """Получение деталей ордера"""
        try:
            result = self.trade.get_order_details(instId=inst_id, ordId=ord_id)

            if result.get('code') == '0' and result.get('data'):
                self._update_order_in_db(result['data'][0])

            return result
        except Exception as e:
            print(f"✗ Ошибка при запросе деталей ордера: {e}")
            return {'code': '-1', 'msg': str(e)}

    def _update_order_in_db(self, order_data: Dict):
        """Обновление ордера в базе данных"""
        try:
            order_id = order_data.get('ordId')
            order = self.db.query(Order).filter_by(order_id=order_id).first()

            if order:
                order.status = order_data.get('state', order.status)
                avg_px = order_data.get('avgPx')
                if avg_px:
                    order.price = float(avg_px)
                order.updated_at = datetime.utcnow()
                self.db.commit()
                print(f"🔄 Ордер {order_id} обновлен в БД. Статус: {order.status}")
            else:
                print(f"⚠️ Ордер {order_id} не найден в БД")
        except Exception as e:
            print(f"✗ Ошибка обновления ордера в БД: {e}")
            self.db.rollback()

    def get_local_orders(self, symbol: Optional[str] = None) -> list[type[Order]]:
        """Получение ордеров из локальной БД"""
        query = self.db.query(Order)
        if symbol:
            query = query.filter(Order.symbol == symbol)
        return query.order_by(Order.created_at.desc()).all()

    def cancel_order(self, inst_id: str, ord_id: str) -> Dict:
        """Отмена ордера"""
        try:
            result = self.trade.cancel_order(instId=inst_id, ordId=ord_id)
            return result
        except Exception as e:
            print(f"✗ Ошибка при отмене ордера: {e}")
            return {'code': '-1', 'msg': str(e)}
