# app/embeddings/embedding_factory.py

from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from utils.config_loader import config
from utils.logger import logger

class EmbeddingFactory:
    """Factory to create embeddings based on configuration"""
    
    @staticmethod
    def create_embeddings():
        """Create embeddings instance based on config"""
        provider = config.get('embeddings', 'provider')
        
        logger.info(f"🔧 Initializing embeddings with provider: {provider}")
        
        if provider == "ollama":
            model = config.get('embeddings', 'ollama', 'model')
            base_url = config.get('embeddings', 'ollama', 'base_url')
            
            logger.info(f"📦 Using Ollama embedding model: {model}")
            return OllamaEmbeddings(
                model=model,
                base_url=base_url
            )
        
        elif provider == "openai":
            model = config.get('embeddings', 'openai', 'model')
            api_key = config.get('embeddings', 'openai', 'api_key')
            
            if not api_key or api_key.startswith("${"):
                raise ValueError("⚠️ OpenAI API key not set in environment!")
            
            logger.info(f"📦 Using OpenAI embedding model: {model}")
            return OpenAIEmbeddings(
                model=model,
                openai_api_key=api_key
            )
        
        else:
            raise ValueError(f"❌ Unknown embedding provider: {provider}")

# Convenience function
def get_embeddings():
    """Get embeddings instance"""
    return EmbeddingFactory.create_embeddings()