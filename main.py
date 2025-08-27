from document_processor import process_pdf
from vector_store import create_vector_store
from workflow import create_workflow, ContractState

def analyze_contract(pdf_path: str, user_query: str) -> str:
    """Main function to analyze contract"""
    print("🔄 Starting contract analysis...")
    
    print("📄 Processing PDF...")
    chunks = process_pdf(pdf_path)
    
    print("🗃️ Creating vector store...")
    cname = pdf_path.split("/")[-1].replace(".pdf", "")
    vector_store = create_vector_store(chunks, COLLECTION_NAME = cname)
    
    print("🔧 Setting up workflow...")
    workflow = create_workflow()
    
    print(f"🤖 Analyzing query: '{user_query}'")
    
    initial_state = ContractState(
        user_query=user_query,
        agent_type=None,
        chunks=chunks,
        vector_store=vector_store,
        response=None,
        messages=[]
    )
    
    result = workflow.invoke(initial_state)
    
    return result["response"]

def main():
    """Example usage"""
    pdf_path = "/Users/sritejabanisetti/Desktop/work/langgraph/test_2025.pdf"  
    
    queries = [
        #"Give me an executive summary of this contract",
        #"What are the payment terms?", 
        #"Find all clauses related to termination",
        "What are the main risks in this contract?"
    ]
    
    print("🚀 Contract Analysis System")
    print("=" * 50)
    
    for query in queries:
        print(f"\n💬 Query: {query}")
        print("-" * 30)
        try:
            response = analyze_contract(pdf_path, query)
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
        print("\n" + "="*50)

if __name__ == "__main__":
    main()