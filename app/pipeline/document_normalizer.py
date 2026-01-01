# app/pipeline/document_normalizer.py

import re
from typing import List
from langchain_core.documents import Document

def clean_text(text: str) -> str:
    """
    Clean OCR / PDF extracted text more aggressively.
    """
    if not text:
        return ""
    
    # Remove excessive newlines
    text = re.sub(r"\n+", " ", text)
    
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    
    # Remove weird characters that look like OCR errors
    # Keep only: letters, numbers, punctuation, spaces
    text = re.sub(r"[^\w\s.,!?;:()\-\"\'%$€]", "", text)
    
    # Remove standalone single characters (likely OCR errors)
    text = re.sub(r"\s[a-zA-Z]\s", " ", text)
    
    return text.strip()

def build_documents(
    chunks,
    source_name: str,
) -> List[Document]:
    """
    Convert Unstructured chunks into LangChain Documents.
    """
    documents: List[Document] = []
    
    for chunk in chunks:
        raw_text = getattr(chunk, "text", "")
        cleaned_text = clean_text(raw_text)
        
        # Drop garbage / very small chunks
        if len(cleaned_text) < 100:  # Increased minimum length
            continue
        
        # Skip if text looks corrupted (too many single letters)
        words = cleaned_text.split()
        if len([w for w in words if len(w) == 1]) / len(words) > 0.3:
            continue
        
        metadata = {
            "source": source_name,
            "page": getattr(chunk.metadata, "page_number", None),
            "category": getattr(chunk, "category", None),
        }
        
        documents.append(
            Document(
                page_content=cleaned_text,
                metadata=metadata,
            )
        )
    
    return documents