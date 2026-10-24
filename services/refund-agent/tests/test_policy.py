# services/refund-agent/tests/test_policy.py
from datetime import datetime, timedelta
from refund_agent.domain.models import (
    Order,
    OrderItem,
    OrderStatus,
    RefundRequest,
    RefundReason,
    ItemCondition,
)
from refund_agent.domain.policy import RefundPolicyEngine


def test_defective_item_full_refund():
    order = Order(
        order_id="ORD-1",
        customer_id="CUST-1",
        purchase_date=datetime.now() - timedelta(days=5),
        status=OrderStatus.DELIVERED,
        items=[OrderItem(item_id="ITEM-1", name="Widget", price=50.0, quantity=1)],
        total_amount=50.0,
    )
    request = RefundRequest(
        order_id="ORD-1",
        item_id="ITEM-1",
        reason=RefundReason.DEFECTIVE,
        condition=ItemCondition.OPENED_LIKE_NEW,
    )

    evaluation = RefundPolicyEngine.evaluate(request, order)
    assert evaluation.is_eligible is True
    assert evaluation.refund_amount == 50.0
    assert evaluation.restocking_fee == 0.0


def test_buyers_remorse_restocking_fee():
    order = Order(
        order_id="ORD-1",
        customer_id="CUST-1",
        purchase_date=datetime.now() - timedelta(days=5),
        status=OrderStatus.DELIVERED,
        items=[OrderItem(item_id="ITEM-1", name="Widget", price=100.0, quantity=1)],
        total_amount=100.0,
    )
    request = RefundRequest(
        order_id="ORD-1",
        item_id="ITEM-1",
        reason=RefundReason.BUYERS_REMORSE,
        condition=ItemCondition.OPENED_LIKE_NEW,
    )

    evaluation = RefundPolicyEngine.evaluate(request, order)
    assert evaluation.is_eligible is True
    assert evaluation.refund_amount == 85.0
    assert evaluation.restocking_fee == 15.0
