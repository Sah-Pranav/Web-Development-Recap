# tests/test_vectorstore.py

from langchain_core.documents import Document
from app.embeddings.vectorstore import get_vectorstore
from utils.logger import logger

def test_vectorstore():
    """Test vector store operations"""
    
    print("\n" + "="*60)
    print("🧪 TESTING VECTOR STORE")
    print("="*60 + "\n")
    
    try:
        # Initialize vector store
        vectorstore = get_vectorstore()
        logger.info("✅ Vector store initialized")
        
        # Create sample documents
        sample_docs = [
            Document(
                page_content="Die DSGVO ist eine EU-Verordnung zum Datenschutz.",
                metadata={"source": "test.pdf", "page": 1, "category": "legal"}
            ),
            Document(
                page_content="Künstliche Intelligenz verändert die Arbeitswelt.",
                metadata={"source": "test.pdf", "page": 2, "category": "technology"}
            ),
            Document(
                page_content="Das Arbeitsrecht regelt die Beziehung zwischen Arbeitgeber und Arbeitnehmer.",
                metadata={"source": "test.pdf", "page": 3, "category": "legal"}
            ),
        ]
        
        logger.info(f"📝 Adding {len(sample_docs)} test documents...")
        
        # Add documents
        doc_ids = vectorstore.add_documents(sample_docs)
        print(f"\n✅ Added {len(doc_ids)} documents")
        print(f"✅ Document IDs: {doc_ids[:2]}... (showing first 2)")
        
        # Check collection count
        count = vectorstore.get_collection_count()
        print(f"✅ Total documents in collection: {count}")
        
        # Test search
        query = "Was regelt die DSGVO?"
        logger.info(f"🔍 Testing search: '{query}'")
        
        results = vectorstore.similarity_search(query, k=2)
        
        print(f"\n✅ Search returned {len(results)} results")
        print("\n📄 Top result:")
        print(f"   Content: {results[0].page_content}")
        print(f"   Metadata: {results[0].metadata}")
        
        # Test search with scores
        logger.info("🔍 Testing search with similarity scores...")
        results_with_scores = vectorstore.similarity_search_with_score(query, k=2)
        
        print(f"\n✅ Search with scores returned {len(results_with_scores)} results")
        for i, (doc, score) in enumerate(results_with_scores, 1):
            print(f"\n   Result {i}:")
            print(f"   Score: {score:.4f}")
            print(f"   Content: {doc.page_content[:100]}...")
        
        print("\n" + "="*60)
        print("✅ ALL VECTOR STORE TESTS PASSED!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Vector store test failed: {e}")
        print(f"\n❌ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_vectorstore()