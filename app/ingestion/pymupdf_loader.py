# app/ingestion/pymupdf_loader.py

import fitz  # PyMuPDF
from typing import List, Dict
from langchain_core.documents import Document
from utils.logger import logger

def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extract text from PDF using PyMuPDF with better accuracy
    
    Returns:
        List of dicts with page_content, page_number, and metadata
    """
    logger.info(f"📄 Extracting text from: {pdf_path}")
    
    try:
        doc = fitz.open(pdf_path)
        pages_content = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text with layout preservation
            text = page.get_text("text")
            
            # Alternative: Extract text with layout (better for tables)
            # text = page.get_text("blocks")
            
            if text.strip():
                pages_content.append({
                    "page_content": text,
                    "page_number": page_num + 1,
                    "total_pages": len(doc)
                })
        
        logger.info(f"✅ Extracted text from {len(pages_content)} pages")
        return pages_content
        
    except Exception as e:
        logger.error(f"❌ Failed to extract text: {e}")
        raise

def chunk_text_by_pages(
    pages_content: List[Dict],
    source_name: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Create chunks from extracted pages
    
    Args:
        pages_content: List of page dictionaries
        source_name: Name of the source document
        chunk_size: Maximum chunk size in characters
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of LangChain Documents
    """
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    logger.info("🔨 Creating chunks from pages...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
        length_function=len,
    )
    
    documents = []
    
    for page_data in pages_content:
        page_content = page_data["page_content"]
        page_num = page_data["page_number"]
        
        # Clean the text
        cleaned_text = clean_text(page_content)
        
        if len(cleaned_text) < 50:  # Skip very short pages
            continue
        
        # Split into chunks
        chunks = splitter.split_text(cleaned_text)
        
        # Create documents
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 100:  # Skip tiny chunks
                continue
                
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": source_name,
                    "page": page_num,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            )
            documents.append(doc)
    
    logger.info(f"✅ Created {len(documents)} document chunks")
    return documents

def clean_text(text: str) -> str:
    """Clean extracted text"""
    import re
    
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page numbers and common artifacts
    text = re.sub(r'\n\d+\n', ' ', text)
    
    # Remove multiple dots (common in TOCs)
    text = re.sub(r'\.{3,}', ' ', text)
    
    return text.strip()

def load_and_process_pdf(pdf_path: str, source_name: str = None) -> List[Document]:
    """
    Complete PDF loading and processing pipeline
    
    Args:
        pdf_path: Path to PDF file
        source_name: Name to use in metadata (defaults to filename)
        
    Returns:
        List of processed Document objects
    """
    import os
    
    if source_name is None:
        source_name = os.path.basename(pdf_path)
    
    # Extract text from PDF
    pages_content = extract_text_from_pdf(pdf_path)
    
    # Create chunks
    documents = chunk_text_by_pages(pages_content, source_name)
    
    return documents