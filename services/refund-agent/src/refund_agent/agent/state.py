# services/refund-agent/src/refund_agent/agent/state.py
from typing import TypedDict, Optional
from refund_agent.domain.models import (
    RefundRequest,
    Order,
    RefundEvaluation,
    RefundResult,
)


class RefundAgentState(TypedDict):
    request: RefundRequest
    order: Optional[Order]
    evaluation: Optional[RefundEvaluation]
    result: Optional[RefundResult]
