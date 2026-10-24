# services/refund-agent/src/refund_agent/services/crm_service.py
from datetime import datetime, timedelta
from typing import Optional
from refund_agent.domain.models import Order, OrderItem, OrderStatus


class CRMService:
    def get_order(self, order_id: str) -> Optional[Order]:
        if order_id == "ORD-100":
            return Order(
                order_id="ORD-100",
                customer_id="CUST-123",
                purchase_date=datetime.now() - timedelta(days=10),
                status=OrderStatus.DELIVERED,
                items=[
                    OrderItem(
                        item_id="ITEM-1",
                        name="Wireless Headphones",
                        price=100.0,
                        quantity=1,
                    )
                ],
                total_amount=100.0,
            )
        return None
