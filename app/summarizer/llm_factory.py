# app/summarizer/llm_factory.py

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from utils.config_loader import config
from utils.logger import logger

class LLMFactory:
    """Factory to create LLM instances based on configuration"""
    
    @staticmethod
    def create_llm():
        """Create LLM instance based on config"""
        provider = config.get('llm', 'provider')
        
        logger.info(f"🤖 Initializing LLM with provider: {provider}")
        
        if provider == "ollama":
            model = config.get('llm', 'ollama', 'model')
            base_url = config.get('llm', 'ollama', 'base_url')
            temperature = config.get('llm', 'ollama', 'temperature', default=0.1)
            
            logger.info(f"📦 Using Ollama model: {model}")
            return ChatOllama(
                model=model,
                base_url=base_url,
                temperature=temperature
            )
        
        elif provider == "openai":
            model = config.get('llm', 'openai', 'model')
            api_key = config.get('llm', 'openai', 'api_key')
            temperature = config.get('llm', 'openai', 'temperature', default=0.1)
            
            if not api_key or api_key.startswith("${"):
                raise ValueError("⚠️ OpenAI API key not set in environment!")
            
            logger.info(f"📦 Using OpenAI model: {model}")
            return ChatOpenAI(
                model=model,
                openai_api_key=api_key,
                temperature=temperature
            )
        
        else:
            raise ValueError(f"❌ Unknown LLM provider: {provider}")

# Convenience function
def get_llm():
    """Get LLM instance"""
    return LLMFactory.create_llm()