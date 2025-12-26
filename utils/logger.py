import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Logger configuration
LOG_FILE = "logs/app.log"
logger = logging.getLogger("rag_pipeline")
logger.setLevel(logging.DEBUG)  # Capture all levels

# Rotating file handler (5 MB per file, keep 3 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)
