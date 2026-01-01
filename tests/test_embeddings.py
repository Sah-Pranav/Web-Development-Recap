# tests/test_embeddings.py

from app.embeddings.embedding_factory import get_embeddings
from utils.logger import logger

def test_embeddings():
    """Test that embeddings are working"""
    
    print("\n" + "="*60)
    print("🧪 TESTING EMBEDDINGS")
    print("="*60 + "\n")
    
    try:
        # Get embeddings
        embeddings = get_embeddings()
        logger.info("✅ Embeddings initialized successfully")
        
        # Test with sample texts
        test_texts = [
            "Die DSGVO regelt den Datenschutz in der Europäischen Union.",
            "Das deutsche Arbeitsrecht schützt die Rechte der Arbeitnehmer.",
            "Machine learning models require large amounts of training data."
        ]
        
        logger.info(f"📝 Testing with {len(test_texts)} sample texts...")
        
        # Generate embeddings for documents
        logger.info("⏳ Generating document embeddings...")
        vectors = embeddings.embed_documents(test_texts)
        
        print(f"\n✅ Generated {len(vectors)} embeddings")
        print(f"✅ Embedding dimension: {len(vectors[0])} dimensions")
        print(f"✅ First vector preview: {vectors[0][:5]}... (showing first 5 values)")
        
        # Test query embedding
        query = "Was ist Datenschutz?"
        logger.info(f"⏳ Generating query embedding for: '{query}'")
        query_vector = embeddings.embed_query(query)
        
        print(f"\n✅ Query embedding dimension: {len(query_vector)} dimensions")
        print(f"✅ Query vector preview: {query_vector[:5]}...")
        
        print("\n" + "="*60)
        print("✅ ALL EMBEDDING TESTS PASSED!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Embedding test failed: {e}")
        print(f"\n❌ TEST FAILED: {e}\n")
        return False

if __name__ == "__main__":
    test_embeddings()