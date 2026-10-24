# services/refund-agent/src/refund_agent/main.py
from fastapi import FastAPI
from refund_agent.domain.models import RefundRequest, RefundResult
from refund_agent.agent.workflow import refund_agent_graph

app = FastAPI(title="Refund AI Agent Service")


@app.post("/api/v1/refunds", response_model=RefundResult)
async def process_refund(request: RefundRequest):
    initial_state = {
        "request": request,
        "order": None,
        "evaluation": None,
        "result": None,
    }
    final_state = refund_agent_graph.invoke(initial_state)
    return final_state["result"]
