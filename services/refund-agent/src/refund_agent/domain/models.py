# services/refund-agent/src/refund_agent/domain/models.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class OrderStatus(str, Enum):
    DELIVERED = "delivered"
    SHIPPED = "shipped"
    PROCESSING = "processing"
    CANCELLED = "cancelled"


class ItemCondition(str, Enum):
    UNOPENED = "unopened"
    OPENED_LIKE_NEW = "opened_like_new"
    DAMAGED_DEFECTIVE = "damaged_defective"
    USED = "used"


class RefundReason(str, Enum):
    DEFECTIVE = "defective"
    WRONG_ITEM = "wrong_item"
    BUYERS_REMORSE = "buyers_remorse"
    LATE_DELIVERY = "late_delivery"


class OrderItem(BaseModel):
    item_id: str
    name: str
    price: float
    quantity: int


class Order(BaseModel):
    order_id: str
    customer_id: str
    purchase_date: datetime
    status: OrderStatus
    items: List[OrderItem]
    total_amount: float


class RefundRequest(BaseModel):
    order_id: str
    item_id: str
    reason: RefundReason
    condition: ItemCondition
    customer_notes: Optional[str] = None


class RefundEvaluation(BaseModel):
    is_eligible: bool
    refund_amount: float = 0.0
    restocking_fee: float = 0.0
    reason_code: str
    explanation: str


class RefundResult(BaseModel):
    refund_id: Optional[str] = None
    order_id: str
    amount_refunded: float
    status: str
    message: str
