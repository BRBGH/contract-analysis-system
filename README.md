# Contract Analysis System (LangGraph)

A sophisticated AI-powered contract analysis system that uses LangGraph workflows to intelligently route queries and analyze PDF contracts using specialized agents.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different types of contract analysis
  - **Summarizer Agent**: Provides executive summaries
  - **RAG Q&A Agent**: Answers specific questions using retrieval-augmented generation
  - **Clause Finder Agent**: Locates specific contract clauses
  - **Risk Checker Agent**: Identifies potential risks and concerns

- **Intelligent Query Routing**: Automatically routes queries to the most appropriate agent
- **Vector Store Integration**: Uses ChromaDB for efficient document retrieval
- **Streamlit Web Interface**: User-friendly web application for contract analysis
- **PDF Processing**: Handles various PDF formats with robust text extraction

## 🏗️ Architecture

The system uses a LangGraph workflow that:
1. Processes PDF documents into chunks
2. Creates vector embeddings for semantic search
3. Routes user queries to specialized agents
4. Returns comprehensive analysis results

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- PDF files for analysis

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd bp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create a .env file or set environment variable
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

   **⚠️ Important**: Update `config.py` to use environment variables instead of hardcoded API keys for security.

## 🚀 Usage

### Web Interface (Recommended)

Launch the Streamlit application:
```bash
streamlit run streamlit_app.py
```

Then:
1. Upload a PDF contract
2. Ask questions about the contract
3. Get AI-powered analysis results

### Command Line Interface

Run the main script:
```bash
python main.py
```

Edit the `pdf_path` and `queries` in `main.py` to analyze your specific contracts.

### Programmatic Usage

```python
from main import analyze_contract

# Analyze a contract
result = analyze_contract("path/to/contract.pdf", "What are the payment terms?")
print(result)
```

## 📁 Project Structure

```
bp/
├── main.py                 # Main analysis function and CLI interface
├── streamlit_app.py        # Web interface using Streamlit
├── workflow.py             # LangGraph workflow definition
├── router.py               # Query routing logic
├── agents.py               # Specialized analysis agents
├── document_processor.py   # PDF processing utilities
├── vector_store.py         # ChromaDB vector store management
├── config.py               # Configuration settings
├── download_model.py       # Model download utilities
└── requirements.txt        # Python dependencies
```

## 🔧 Configuration

Key settings in `config.py`:
- **Model**: GPT-4o (configurable)
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters
- **Vector Store**: ChromaDB local storage

## 📝 Example Queries

- "Give me an executive summary of this contract"
- "What are the payment terms?"
- "Find all clauses related to termination"
- "What are the main risks in this contract?"
- "Who are the parties involved?"
- "What is the contract duration?"

## 🛡️ Security Notes

- **API Key Security**: The current `config.py` contains a hardcoded API key. For production use:
  ```python
  import os
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  ```
- Store sensitive data in environment variables or secure vaults
- Consider implementing rate limiting for production deployments

## 🧪 Development

To extend the system:

1. **Add new agents** in `agents.py`
2. **Update routing logic** in `router.py`
3. **Modify workflow** in `workflow.py`
4. **Enhance UI** in `streamlit_app.py`

## 🐛 Troubleshooting

**Common Issues:**
- **PDF Processing Errors**: Ensure PDF is text-readable (not scanned images)
- **API Rate Limits**: Implement retry logic or use different models
- **Memory Issues**: Reduce chunk size for large documents

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

---

**Built with**: LangGraph, OpenAI GPT-4o, ChromaDB, Streamlit
