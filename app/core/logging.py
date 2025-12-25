# app/core/logging.py
import logging
import sys

# Configure root logger
logging.basicConfig(
    level=logging.INFO,  # Default logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Print logs to stdout (good for Docker/production)
    ],
)

# Optional: create a named logger for the app
logger = logging.getLogger("ai_rag_chatbot")
