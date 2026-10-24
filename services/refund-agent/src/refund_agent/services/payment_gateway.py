# services/refund-agent/src/refund_agent/services/payment_gateway.py
import uuid


class PaymentGatewayService:
    def execute_refund(self, order_id: str, amount: float) -> str:
        return f"txn_ref_{uuid.uuid4().hex[:8]}"
