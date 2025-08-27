import streamlit as st
import streamlit.components.v1
import tempfile
import os
from pathlib import Path
import traceback

# Import the main functionality
from main import analyze_contract

def main():
    st.set_page_config(
        page_title="Contract Analysis System (LangGraph)",
        page_icon="📄",
        layout="wide"
    )
    
    # Initialize session state for architecture view
    if 'show_architecture' not in st.session_state:
        st.session_state.show_architecture = False
    
    st.title("📄 Contract Analysis System (LangGraph)")
    st.markdown("Upload a PDF contract and ask questions about it using AI-powered analysis.")
    
    # Sidebar for instructions
    with st.sidebar:
        # Architecture toggle button
        if st.button("🏗️ Toggle Architecture Diagram", use_container_width=True):
            st.session_state.show_architecture = not st.session_state.show_architecture
        
        st.markdown("---")
        
        if not st.session_state.show_architecture:
            st.header("ℹ️ How to use")
            st.markdown("""
            1. **Upload a PDF** contract document
            2. **Ask a question** about the contract
            3. **Get AI-powered analysis** using specialized agents
            
            **Example questions:**
            - Give me an executive summary
            - What are the payment terms?
            - Find termination clauses
            - What are the main risks?
            """)
            
            st.header("🤖 AI Agents")
            st.markdown("""
            The system uses different specialized agents:
            - **Summarizer**: For executive summaries
            - **QA Agent**: For general questions
            - **Clause Finder**: For finding specific clauses
            - **Risk Checker**: For identifying risks
            """)
        else:
            st.header("🏗️ Architecture Info")
            st.markdown("""
            **Multi-Agent System Architecture:**
            
            🔄 **Router Agent**: Classifies user queries and routes them to appropriate specialists
            
            🤖 **Specialized Agents**:
            - **Summarizer**: Creates executive summaries
            - **RAG Q&A**: Answers specific questions with citations
            - **Clause Finder**: Searches for specific contract clauses
            - **Risk Checker**: Identifies potential risks and compliance issues
            
            💾 **Storage**: Vector database for semantic search and document chunks for context
            """)
    
    # Show either architecture diagram or main app
    if st.session_state.show_architecture:
        st.header("🏗️ System Architecture")
        
        # Display the SVG
        svg_path = "contract-analysis-svg.svg"
        if os.path.exists(svg_path):
            # Use Streamlit's native image display with larger width
            st.image(svg_path, use_container_width=True)
            
            # Add a note about zooming
            st.info("💡 Tip: Click on the image to view it in full size, or use the download button below to get the SVG file.")
            
            # Alternative: Also provide a download option
            with open(svg_path, 'rb') as f:
                st.download_button(
                    label="📥 Download Architecture Diagram",
                    data=f.read(),
                    file_name="contract-analysis-architecture.svg",
                    mime="image/svg+xml"
                )
        else:
            st.error("Architecture diagram not found. Please ensure the SVG file is in the correct location.")
        
        st.markdown("---")
        st.info("👆 Click the 'Toggle Architecture Diagram' button in the sidebar to return to the main interface.")
        
    else:
        # Main content area
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📤 Upload Contract")
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type="pdf",
                help="Upload a contract document in PDF format"
            )
            
            if uploaded_file is not None:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                # Display file info
                file_details = {
                    "Filename": uploaded_file.name,
                    "File size": f"{uploaded_file.size} bytes"
                }
                st.json(file_details)
        
        with col2:
            st.header("❓ Ask a Question")
            
            user_query = st.text_area(
                "Enter your question about the contract:",
                placeholder="Examples:\n• Give me an executive summary\n• What are the payment terms?\n• Find termination clauses\n• What are the main risks?",
                height=150,
                help="Ask any question about the uploaded contract. The AI will analyze it and provide detailed answers."
            )
        
        # Analysis section
        st.header("🔍 Analysis")
        
        if st.button("🚀 Analyze Contract", type="primary", use_container_width=True):
            if uploaded_file is None:
                st.error("❌ Please upload a PDF file first.")
            elif not user_query or user_query.strip() == "":
                st.error("❌ Please enter a question.")
            else:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    with st.spinner("🔄 Processing contract and analyzing..."):
                        # Create progress indicators
                        progress_text = st.empty()
                        progress_bar = st.progress(0)
                        
                        progress_text.text("📄 Processing PDF...")
                        progress_bar.progress(25)
                        
                        progress_text.text("🗃️ Creating vector store...")
                        progress_bar.progress(50)
                        
                        progress_text.text("🤖 Analyzing with AI...")
                        progress_bar.progress(75)
                        
                        # Run the analysis
                        response = analyze_contract(tmp_file_path, user_query)
                        
                        progress_text.text("✅ Analysis complete!")
                        progress_bar.progress(100)
                    
                    # Display results
                    st.success("✅ Analysis completed!")
                    
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📝 Response", "📊 Details"])
                    
                    with tab1:
                        st.markdown("### 🤖 AI Response")
                        st.markdown(response)
                        
                        # Copy to clipboard button
                        st.button("📋 Copy Response", on_click=lambda: st.write("Response copied to clipboard!"))
                    
                    with tab2:
                        st.markdown("### 📊 Analysis Details")
                        st.info(f"**Question:** {user_query}")
                        st.info(f"**File:** {uploaded_file.name}")
                        st.info(f"**Response Length:** {len(response)} characters")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred during analysis:")
                    st.error(str(e))
                    
                    # Show detailed error in expander
                    with st.expander("🔍 Show detailed error"):
                        st.code(traceback.format_exc())
                
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
        
        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: gray;'>
                🔒 Your documents are processed securely and not stored permanently.
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
