# scripts/debug_pdf_extraction.py

from app.ingestion.pdf_loader import partition_document, create_chunks_by_title
from app.pipeline.document_normalizer import build_documents, clean_text

pdf_file = "./docs/sample.pdf"

print("\n" + "="*70)
print("🔍 PDF EXTRACTION DIAGNOSTICS")
print("="*70 + "\n")

# Extract elements
elements = partition_document(pdf_file)

print(f"Total elements extracted: {len(elements)}\n")

# Show first 10 elements with their types
print("📄 First 10 elements:\n")
for i, element in enumerate(elements[:10], 1):
    text = getattr(element, "text", "")
    category = getattr(element, "category", "Unknown")
    print(f"{i}. [{category}] {text[:150]}...")
    print()

# Show chunks
chunks = create_chunks_by_title(elements)
print(f"\n🔨 Total chunks created: {len(chunks)}\n")

# Show first chunk before cleaning
if chunks:
    print("📋 First chunk (raw text):")
    print(chunks[0].text[:500])
    print("\n")
    
    print("🧹 First chunk (after cleaning):")
    cleaned = clean_text(chunks[0].text)
    print(cleaned[:500])
    print("\n")

# Show final documents
documents = build_documents(chunks, "report.pdf")
print(f"📚 Total documents after filtering: {len(documents)}\n")

if documents:
    print("📄 First document content:")
    print(documents[0].page_content[:500])
    print(f"\nMetadata: {documents[0].metadata}")