from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

class RouterDecision(BaseModel):
    """Router decision structure"""
    agent_type: str = Field(description="The agent type: summariser, rag_qa, clause_finder, or risk_checker")
    reasoning: str = Field(description="Why this agent was chosen")
    confidence: float = Field(description="Confidence score 0-1")

def create_router_llm():
    """Create LLM for router"""
    return ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=OPENAI_TEMPERATURE
    )

def route_query(query: str) -> str:
    """Route user query to appropriate agent"""
    llm = create_router_llm()
    
    system_prompt = """You are a routing agent for a contract analysis system. 
    Based on the user query, decide which specialist agent should handle it:

    1. 'summariser': For requests asking for contract summaries, overviews, executive summaries
    2. 'rag_qa': For specific questions about contract details, general Q&A
    3. 'clause_finder': For finding specific clauses, sections, or terms
    4. 'risk_checker': For risk analysis, compliance checks, identifying problematic clauses

    Return only the agent type as a single word."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Route this query: {query}")
    ]
    
    # Get structured response
    structured_llm = llm.with_structured_output(RouterDecision)
    try:
        response = structured_llm.invoke(messages)
        print(f"Router decision: {response.agent_type} (confidence: {response.confidence})")
        print(f"Reasoning: {response.reasoning}")
        return response.agent_type
    except:
        # Fallback to simple routing
        query_lower = query.lower()
        if any(word in query_lower for word in ['summary', 'overview', 'summarize', 'executive']):
            return 'summariser'
        elif any(word in query_lower for word in ['find', 'clause', 'section', 'locate']):
            return 'clause_finder'
        elif any(word in query_lower for word in ['risk', 'danger', 'problem', 'compliance']):
            return 'risk_checker'
        else:
            return 'rag_qa'