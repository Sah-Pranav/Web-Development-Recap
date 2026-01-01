# app/retriever/query.py

from typing import List, Dict, Tuple
from langchain_core.documents import Document
from app.embeddings.vectorstore import get_vectorstore
from utils.config_loader import config
from utils.logger import logger

class Retriever:
    """Handle document retrieval"""
    
    def __init__(self):
        self.vectorstore = get_vectorstore()
        self.top_k = config.get('retrieval', 'top_k', default=5)
        self.score_threshold = config.get('retrieval', 'score_threshold', default=0.7)
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = None,
        with_scores: bool = True
    ) -> List[Document] | List[Tuple[Document, float]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            with_scores: Whether to return similarity scores
            
        Returns:
            List of documents or (document, score) tuples
        """
        if top_k is None:
            top_k = self.top_k
        
        logger.info(f"🔍 Retrieving top {top_k} documents for query: '{query}'")
        
        try:
            if with_scores:
                results = self.vectorstore.similarity_search_with_score(query, k=top_k)
                
                # Filter by score threshold
                filtered_results = [
                    (doc, score) for doc, score in results 
                    if score <= self.score_threshold  # Lower score = more similar
                ]
                
                logger.info(f"✅ Retrieved {len(filtered_results)} documents (after filtering)")
                return filtered_results
            else:
                results = self.vectorstore.similarity_search(query, k=top_k)
                logger.info(f"✅ Retrieved {len(results)} documents")
                return results
                
        except Exception as e:
            logger.error(f"❌ Retrieval failed: {e}")
            raise
    
    def format_context(
        self, 
        documents: List[Document] | List[Tuple[Document, float]]
    ) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            documents: List of documents or (document, score) tuples
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, item in enumerate(documents, 1):
            # Handle both Document and (Document, score) formats
            if isinstance(item, tuple):
                doc, score = item
                score_text = f" (Relevanz: {1-score:.2f})"
            else:
                doc = item
                score_text = ""
            
            source = doc.metadata.get('source', 'Unbekannt')
            page = doc.metadata.get('page', 'N/A')
            
            context_parts.append(
                f"[Dokument {i} - Quelle: {source}, Seite: {page}{score_text}]\n"
                f"{doc.page_content}\n"
            )
        
        return "\n".join(context_parts)

# Global instance
def get_retriever() -> Retriever:
    """Get retriever instance"""
    return Retriever()