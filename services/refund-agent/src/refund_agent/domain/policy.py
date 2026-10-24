# services/refund-agent/src/refund_agent/domain/policy.py
from datetime import datetime
from refund_agent.domain.models import (
    RefundRequest,
    Order,
    RefundEvaluation,
    RefundReason,
    ItemCondition,
    OrderStatus,
)


class RefundPolicyEngine:
    RETURN_WINDOW_DAYS: int = 30
    RESTOCKING_FEE_RATE: float = 0.15

    @classmethod
    def evaluate(cls, request: RefundRequest, order: Order) -> RefundEvaluation:
        if order.status != OrderStatus.DELIVERED:
            return RefundEvaluation(
                is_eligible=False,
                reason_code="ORDER_NOT_DELIVERED",
                explanation=f"Order status is '{order.status.value}'. Only delivered orders can be refunded.",
            )

        days_since_purchase = (
            datetime.now() - order.purchase_date.replace(tzinfo=None)
        ).days
        if days_since_purchase > cls.RETURN_WINDOW_DAYS:
            return RefundEvaluation(
                is_eligible=False,
                reason_code="EXCEEDED_RETURN_WINDOW",
                explanation=f"Order was purchased {days_since_purchase} days ago (limit is {cls.RETURN_WINDOW_DAYS} days).",
            )

        item = next((i for i in order.items if i.item_id == request.item_id), None)
        if not item:
            return RefundEvaluation(
                is_eligible=False,
                reason_code="ITEM_NOT_FOUND",
                explanation=f"Item '{request.item_id}' is not present in order '{order.order_id}'.",
            )

        base_amount = item.price * item.quantity
        restocking_fee = 0.0

        if request.reason in [RefundReason.DEFECTIVE, RefundReason.WRONG_ITEM]:
            restocking_fee = 0.0
        elif (
            request.condition == ItemCondition.OPENED_LIKE_NEW
            and request.reason == RefundReason.BUYERS_REMORSE
        ):
            restocking_fee = base_amount * cls.RESTOCKING_FEE_RATE
        elif request.condition == ItemCondition.USED:
            return RefundEvaluation(
                is_eligible=False,
                reason_code="INELIGIBLE_CONDITION",
                explanation="Non-defective used items cannot be refunded.",
            )

        final_refund = max(0.0, base_amount - restocking_fee)

        return RefundEvaluation(
            is_eligible=True,
            refund_amount=round(final_refund, 2),
            restocking_fee=round(restocking_fee, 2),
            reason_code="APPROVED",
            explanation="Request meets all policy requirements.",
        )
