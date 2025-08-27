from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.vectorstores import Chroma
from typing import List, Dict, Any
from vector_store import search_similar_chunks
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE

def create_agent_llm():
    """Create LLM for agents"""
    return ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=OPENAI_TEMPERATURE
    )

def summariser_agent(chunks: List[Dict[str, Any]]) -> str:
    """Generate executive summary"""
    llm = create_agent_llm()
    
    # Use first 10 chunks for context
    context = "\n".join([chunk['content'] for chunk in chunks[:10]])
    
    system_prompt = """You are a contract summarisation specialist. 
    Create a bullet-point executive summary covering:
    - Parties involved
    - Scope of work/purpose  
    - Contract term/duration
    - Financial terms
    - Key risks
    
    Use ONLY bullet points, be concise and factual."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Summarise this contract:\n\n{context}")
    ]
    
    response = llm.invoke(messages)
    return response.content

def rag_qa_agent(query: str, vector_store: Chroma) -> str:
    """Answer questions using RAG"""
    llm = create_agent_llm()
    
    # Search for relevant chunks
    results = search_similar_chunks(vector_store, query, k=5)
    
    context = ""
    citations = []
    for doc, score in results:
        context += f"\n[{doc.metadata['chunk_id']}] {doc.page_content}\n"
        citations.append(doc.metadata['chunk_id'])
    
    system_prompt = """You are a contract Q&A specialist. Answer questions based on the provided contract context.
    Always cite your sources using the chunk IDs in square brackets [chunk_id].
    If you cannot find relevant information, say so clearly."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]
    
    response = llm.invoke(messages)
    return response.content

def clause_finder_agent(topic: str, vector_store: Chroma) -> str:
    """Find clauses matching the topic"""
    # Search for relevant clauses
    results = search_similar_chunks(vector_store, topic, k=8)
    
    if not results:
        return f"No clauses found matching '{topic}'"
    
    # Format results
    output = f"**CLAUSES MATCHING '{topic.upper()}'**\n\n"
    
    for i, (doc, score) in enumerate(results):
        if score > 0.3:  # Relevance threshold
            output += f"**Match {i+1}:** {doc.metadata['chunk_id']} (Page {doc.metadata['page_number']})\n"
            output += f"**Relevance Score:** {score:.2f}\n"
            output += f"**Content:** {doc.page_content}\n\n---\n\n"
    
    return output.strip()

def risk_checker_agent(chunks: List[Dict[str, Any]]) -> str:
    """Identify risky clauses"""
    llm = create_agent_llm()
    
    risk_keywords = [
        'penalty', 'terminate', 'breach', 'default', 'liability', 
        'indemnify', 'force majeure', 'confidential', 'non-compete',
        'intellectual property', 'warranty', 'guarantee', 'damages'
    ]
    
    risky_chunks = []
    for chunk in chunks:
        if any(keyword in chunk['content'].lower() for keyword in risk_keywords):
            risky_chunks.append(chunk)
    
    if not risky_chunks:
        return "No significant risks identified in the contract."
    
    context = ""
    for chunk in risky_chunks[:5]:
        context += f"[{chunk['chunk_id']}] {chunk['content']}\n\n"
    
    system_prompt = """You are a contract risk assessment specialist.
    Analyze the provided clauses and identify risks. For each risk:
    - Identify the clause ID
    - Categorize risk type (financial, legal, operational, compliance)
    - Assess severity (LOW/MEDIUM/HIGH/CRITICAL)
    - Provide description and mitigation advice
    
    Focus on compliance and commercial risks."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze these clauses for risks:\n\n{context}")
    ]
    
    response = llm.invoke(messages)
    return f"**RISK ASSESSMENT**\n\n{response.content}"