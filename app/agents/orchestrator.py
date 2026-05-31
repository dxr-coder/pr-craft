from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.agents.coder import code
from app.agents.planner import plan
from app.agents.reviewer import review


class AgentState(TypedDict):
    issue: str
    plan: str
    code: str
    review: str
    attempts: int


MAX_ATTEMPTS = 3


def plan_node(state: AgentState) -> dict:
    plan_result = plan(state["issue"])
    return {"plan": plan_result, "attempts": state["attempts"] + 1}


def code_node(state: AgentState) -> dict:
    code_result = code(state["plan"])
    return {"code": code_result}


def review_node(state: AgentState) -> dict:
    review_result = review(state["code"])
    return {"review": review_result}


def should_continue(state: AgentState) -> str:
    if "PASS" in state["review"]:
        return "end"
    if state["attempts"] >= MAX_ATTEMPTS:
        return "end"
    return "fix"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("plan", plan_node)
    graph.add_node("code", code_node)
    graph.add_node("review", review_node)

    graph.add_edge(START, "plan")
    graph.add_edge("plan", "code")
    graph.add_edge("code", "review")

    graph.add_conditional_edges("review", should_continue, {"end": END, "fix": "code"})
    return graph.compile()
