# services/refund-agent/src/refund_agent/agent/workflow.py
from langgraph.graph import StateGraph, END
from refund_agent.agent.state import RefundAgentState
from refund_agent.domain.policy import RefundPolicyEngine
from refund_agent.domain.models import RefundResult
from refund_agent.services.crm_service import CRMService
from refund_agent.services.payment_gateway import PaymentGatewayService

crm = CRMService()
payment = PaymentGatewayService()


def fetch_order_node(state: RefundAgentState) -> RefundAgentState:
    order = crm.get_order(state["request"].order_id)
    state["order"] = order
    return state


def evaluate_rules_node(state: RefundAgentState) -> RefundAgentState:
    if not state["order"]:
        state["result"] = RefundResult(
            order_id=state["request"].order_id,
            amount_refunded=0.0,
            status="REJECTED",
            message="Order ID not found in system.",
        )
        return state

    state["evaluation"] = RefundPolicyEngine.evaluate(state["request"], state["order"])
    return state


def process_payout_node(state: RefundAgentState) -> RefundAgentState:
    if state.get("result"):
        return state

    evaluation = state["evaluation"]
    if not evaluation.is_eligible:
        state["result"] = RefundResult(
            order_id=state["request"].order_id,
            amount_refunded=0.0,
            status="REJECTED",
            message=evaluation.explanation,
        )
    else:
        txn_id = payment.execute_refund(
            state["request"].order_id, evaluation.refund_amount
        )
        state["result"] = RefundResult(
            refund_id=txn_id,
            order_id=state["request"].order_id,
            amount_refunded=evaluation.refund_amount,
            status="SUCCESS",
            message=f"Refund processed. Amount: ${evaluation.refund_amount:.2f} (Restocking fee: ${evaluation.restocking_fee:.2f}).",
        )
    return state


builder = StateGraph(RefundAgentState)
builder.add_node("fetch_order", fetch_order_node)
builder.add_node("evaluate_rules", evaluate_rules_node)
builder.add_node("process_payout", process_payout_node)

builder.set_entry_point("fetch_order")
builder.add_edge("fetch_order", "evaluate_rules")
builder.add_edge("evaluate_rules", "process_payout")
builder.add_edge("process_payout", END)

refund_agent_graph = builder.compile()
