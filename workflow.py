from typing import TypedDict, Annotated, List, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
import operator

# Import our modules
from document_processor import process_pdf
from vector_store import create_vector_store
from router import route_query
from agents import summariser_agent, rag_qa_agent, clause_finder_agent, risk_checker_agent

class ContractState(TypedDict):
    """State passed between nodes"""
    user_query: str
    agent_type: Optional[str]
    chunks: List[Any]
    vector_store: Any
    response: Optional[str]
    messages: Annotated[List, operator.add]

def router_node(state: ContractState) -> ContractState:
    """Router node - decides which agent to use"""
    agent_type = route_query(state["user_query"])
    return {
        **state,
        "agent_type": agent_type,
        "messages": [f"Routing to: {agent_type}"]
    }

def summariser_node(state: ContractState) -> ContractState:
    """Summariser node"""
    response = summariser_agent(state["chunks"])
    return {
        **state,
        "response": response,
        "messages": ["Generated summary"]
    }

def rag_qa_node(state: ContractState) -> ContractState:
    """RAG Q&A node"""
    response = rag_qa_agent(state["user_query"], state["vector_store"])
    return {
        **state,
        "response": response,
        "messages": ["Answered question using RAG"]
    }

def clause_finder_node(state: ContractState) -> ContractState:
    """Clause finder node"""
    response = clause_finder_agent(state["user_query"], state["vector_store"])
    return {
        **state,
        "response": response,
        "messages": ["Found matching clauses"]
    }

def risk_checker_node(state: ContractState) -> ContractState:
    """Risk checker node"""
    response = risk_checker_agent(state["chunks"])
    return {
        **state,
        "response": response,
        "messages": ["Analyzed contract risks"]
    }

def route_condition(state: ContractState) -> str:
    """Determine which agent to route to"""
    return state["agent_type"]

def create_workflow() -> StateGraph:
    """Create the LangGraph workflow"""
    workflow = StateGraph(ContractState)
    
    workflow.add_node("router", router_node)
    workflow.add_node("summariser", summariser_node)
    workflow.add_node("rag_qa", rag_qa_node)
    workflow.add_node("clause_finder", clause_finder_node)
    workflow.add_node("risk_checker", risk_checker_node)
    
    workflow.set_entry_point("router")
    
    workflow.add_conditional_edges(
        "router",
        route_condition,
        {
            "summariser": "summariser",
            "rag_qa": "rag_qa", 
            "clause_finder": "clause_finder",
            "risk_checker": "risk_checker"
        }
    )
    
    workflow.add_edge("summariser", END)
    workflow.add_edge("rag_qa", END)
    workflow.add_edge("clause_finder", END)
    workflow.add_edge("risk_checker", END)
    
    return workflow.compile()