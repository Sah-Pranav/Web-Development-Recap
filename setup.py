from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="rag_pipeline",
    version="0.1.0",
    description="RAG-based PDF processing pipeline",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),  # automatically finds all packages in app/ etc.
    include_package_data=True, # includes non-Python files if specified in MANIFEST.in
    install_requires=requirements,
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "rag-pipeline=app.ingestion.pdf_loader:main",  # optional CLI entry
        ],
    },
)
