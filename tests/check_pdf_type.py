# Save this as scripts/check_pdf_type.py

import fitz  # PyMuPDF

pdf_path = "./docs/sample.pdf"
doc = fitz.open(pdf_path)

print("\n" + "="*60)
print("📄 PDF ANALYSIS")
print("="*60 + "\n")

for page_num in range(min(3, len(doc))):  # Check first 3 pages
    page = doc[page_num]
    
    # Get text
    text = page.get_text()
    
    # Get images
    images = page.get_images()
    
    print(f"Page {page_num + 1}:")
    print(f"  Text length: {len(text)} characters")
    print(f"  Number of images: {len(images)}")
    print(f"  Text preview: {text[:200]}")
    print()

print("\n" + "="*60)
print("DIAGNOSIS:")

if len(text) < 100:
    print("❌ Very little text found - likely a SCANNED/IMAGE-based PDF")
    print("✅ SOLUTION: Need better OCR or different dataset")
elif "�" in text or len([c for c in text if not c.isprintable()]) > len(text) * 0.1:
    print("⚠️  Corrupted text extraction")
    print("✅ SOLUTION: Try PyMuPDF or different extraction method")
else:
    print("✅ Text-based PDF - extraction should work")
    print("⚠️  Pipeline might need tuning")

print("="*60 + "\n")