# app/ingestion/pdf_loader.py

import os
from typing import List
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from utils.logger import logger

def partition_document(file_path: str):
    """
    Extract elements from a PDF using Unstructured.
    Handles text, tables, and images.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"{file_path} does not exist.")
    
    logger.info(f"📄 Partitioning document: {file_path}")
    
    try:
        elements = partition_pdf(
            filename=file_path,
            strategy="hi_res",               # High accuracy parsing
            infer_table_structure=True,      # Keeps tables structured
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            languages=["eng"],               # Specify English for better OCR
            # Add these for better text extraction:
            include_page_breaks=True,
            ocr_languages="eng",             # OCR language
        )
        
        logger.info(f"✅ Extracted {len(elements)} elements from PDF")
        return elements
        
    except Exception as e:
        logger.error(f"❌ Failed to partition document {file_path}: {e}")
        return []

def create_chunks_by_title(
    elements: List, 
    max_characters: int = 1500,           # Reduced for better chunks
    new_after_n_chars: int = 1200,        # Adjusted
    combine_text_under_n_chars: int = 300  # Adjusted
):
    """
    Splits PDF elements into intelligent chunks based on titles.
    """
    logger.info("🔨 Creating chunks based on titles...")
    
    try:
        chunks = chunk_by_title(
            elements,
            max_characters=max_characters,
            new_after_n_chars=new_after_n_chars,
            combine_text_under_n_chars=combine_text_under_n_chars
        )
        
        logger.info(f"✅ Created {len(chunks)} chunks")
        return chunks
        
    except Exception as e:
        logger.error(f"❌ Failed to create chunks: {e}")
        return []