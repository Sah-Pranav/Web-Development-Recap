# Placeholder
# app/embeddings/vectorstore.py

from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from app.embeddings.embedding_factory import get_embeddings
from utils.config_loader import config
from utils.logger import logger
import os

class VectorStoreManager:
    """Manage vector store operations"""
    
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize ChromaDB vector store"""
        provider = config.get('vectorstore', 'provider')
        
        if provider == "chroma":
            persist_dir = config.get('vectorstore', 'chroma', 'persist_directory')
            collection_name = config.get('vectorstore', 'chroma', 'collection_name')
            
            # Create directory if it doesn't exist
            os.makedirs(persist_dir, exist_ok=True)
            
            logger.info(f"🗄️  Initializing ChromaDB at: {persist_dir}")
            logger.info(f"📚 Collection name: {collection_name}")
            
            self.vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_dir
            )
            
            logger.info("✅ Vector store initialized successfully")
        else:
            raise ValueError(f"❌ Unsupported vector store provider: {provider}")
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to vector store
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("⚠️ No documents to add")
            return []
        
        logger.info(f"📥 Adding {len(documents)} documents to vector store...")
        
        try:
            ids = self.vectorstore.add_documents(documents)
            logger.info(f"✅ Successfully added {len(ids)} documents")
            return ids
        except Exception as e:
            logger.error(f"❌ Failed to add documents: {e}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: int = None
    ) -> List[Document]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if k is None:
            k = config.get('retrieval', 'top_k', default=5)
        
        logger.info(f"🔍 Searching for: '{query}' (top {k} results)")
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"✅ Found {len(results)} relevant documents")
            return results
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            raise
    
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = None
    ) -> List[tuple]:
        """
        Search with similarity scores
        
        Returns:
            List of (Document, score) tuples
        """
        if k is None:
            k = config.get('retrieval', 'top_k', default=5)
        
        logger.info(f"🔍 Searching with scores: '{query}'")
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            logger.info(f"✅ Found {len(results)} results with scores")
            return results
        except Exception as e:
            logger.error(f"❌ Search with scores failed: {e}")
            raise
    
    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        try:
            count = self.vectorstore._collection.count()
            logger.info(f"📊 Collection contains {count} documents")
            return count
        except Exception as e:
            logger.error(f"❌ Failed to get collection count: {e}")
            return 0

# Global instance
_vectorstore_instance = None

def get_vectorstore() -> VectorStoreManager:
    """Get or create vector store instance (singleton pattern)"""
    global _vectorstore_instance
    if _vectorstore_instance is None:
        _vectorstore_instance = VectorStoreManager()
    return _vectorstore_instance