import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

project_path = Path(__file__).parent.parent
logger = logging.getLogger('genai_app')
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(str(project_path) + '/app.log',
                                       maxBytes=5*1024*1024, backupCount=10, encoding='utf-8')
    file_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
