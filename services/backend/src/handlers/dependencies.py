from typing import Optional

from src.handlers.files import FileHandler
from src.interfaces.handlers import FileHandlerInterface
from src.settings.config import config

_file_handler: Optional[FileHandlerInterface] = None

def get_file_handler() -> FileHandlerInterface:
    global _file_handler
    if _file_handler is None:
        _file_handler = FileHandler(
            images_dir = config.IMAGE_DIR,
            max_file_size = config.MAX_FILE_SIZE,
            supported_formats = config.SUPPORTED_FORMATS
        )
    return _file_handler