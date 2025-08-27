from typing import List, Dict, Any
from config import CHUNK_SIZE, CHUNK_OVERLAP
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pypdf

def process_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Parse PDF and return chunks with metadata"""
    print(f"Processing PDF: {pdf_path}")
    
    # Parse PDF with pypdf (simpler, no network dependencies)
    with open(pdf_path, 'rb') as file:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    # Split text into chunks
    text_chunks = text_splitter.split_text(text)
    
    chunks = []
    for i, chunk in enumerate(text_chunks):
        chunks.append({
            'content': chunk,
            'chunk_id': f"chunk_{i}",
            'page_number': 1,  # Will be estimated from chunk position
            'element_type': 'text'
        })
    
    print(f"Created {len(chunks)} chunks")
    return chunks