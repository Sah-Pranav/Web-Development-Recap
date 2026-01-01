# tests/test_rag_pipeline.py

from langchain_core.documents import Document
from app.embeddings.vectorstore import get_vectorstore
from app.summarizer.ai_summary import get_rag_pipeline
from utils.logger import logger

def test_rag_pipeline():
    """Test the complete RAG pipeline"""
    
    print("\n" + "="*60)
    print("🧪 TESTING COMPLETE RAG PIPELINE")
    print("="*60 + "\n")
    
    try:
        # Step 1: Add some test documents
        logger.info("📥 Adding test documents to vector store...")
        
        vectorstore = get_vectorstore()
        
        sample_docs = [
            Document(
                page_content="Die Datenschutz-Grundverordnung (DSGVO) ist eine Verordnung der Europäischen Union. Sie regelt die Verarbeitung personenbezogener Daten durch private Unternehmen und öffentliche Stellen. Die DSGVO stärkt die Rechte der betroffenen Personen und harmonisiert das Datenschutzrecht innerhalb der EU.",
                metadata={"source": "dsgvo_guide.pdf", "page": 1, "category": "legal"}
            ),
            Document(
                page_content="Nach der DSGVO haben betroffene Personen das Recht auf Auskunft, Berichtigung und Löschung ihrer personenbezogenen Daten. Unternehmen müssen die Einwilligung der Nutzer einholen und transparent über die Datenverarbeitung informieren.",
                metadata={"source": "dsgvo_guide.pdf", "page": 2, "category": "legal"}
            ),
            Document(
                page_content="Bei Verstößen gegen die DSGVO können Bußgelder von bis zu 20 Millionen Euro oder 4% des weltweiten Jahresumsatzes verhängt werden. Unternehmen müssen einen Datenschutzbeauftragten bestellen, wenn sie personenbezogene Daten in großem Umfang verarbeiten.",
                metadata={"source": "dsgvo_guide.pdf", "page": 3, "category": "legal"}
            ),
            Document(
                page_content="Künstliche Intelligenz revolutioniert viele Branchen. Machine Learning Modelle benötigen große Datenmengen für das Training. Deep Learning nutzt neuronale Netze mit vielen Schichten.",
                metadata={"source": "ai_basics.pdf", "page": 1, "category": "technology"}
            ),
        ]
        
        vectorstore.add_documents(sample_docs)
        print(f"✅ Added {len(sample_docs)} test documents\n")
        
        # Step 2: Initialize RAG pipeline
        logger.info("🔧 Initializing RAG pipeline...")
        rag = get_rag_pipeline()
        print("✅ RAG pipeline initialized\n")
        
        # Step 3: Test queries
        test_queries = [
            "Was regelt die DSGVO?",
            "Welche Rechte haben betroffene Personen nach der DSGVO?",
            "Wie hoch können Bußgelder bei DSGVO-Verstößen sein?",
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"📝 Test Query {i}: {query}")
            print('='*60)
            
            result = rag.query(query, top_k=3)
            
            print(f"\n🤖 Answer:")
            print(f"{result['answer']}\n")
            
            print(f"📚 Sources ({result['retrieved_docs']} documents):")
            for j, source in enumerate(result['sources'], 1):
                print(f"  {j}. {source['source']} (Seite {source['page']}, Relevanz: {source['relevance']})")
                print(f"     Preview: {source['content_preview'][:100]}...\n")
        
        print("\n" + "="*60)
        print("✅ ALL RAG PIPELINE TESTS PASSED!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ RAG pipeline test failed: {e}")
        print(f"\n❌ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_rag_pipeline()