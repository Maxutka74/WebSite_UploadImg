import os
import uuid
import shutil
from typing import cast

from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile

from src.settings.config import config
from src.exceptions.api_errors import NotSupportedFormatError, MaxSizeExceedError
from src.interfaces.protocols import SupportsWrite


def handle_uploaded_file(file: UploadFile) -> dict[str, str]:
    filename = file.filename if hasattr(file, "filename") else "uploaded_file"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in config.SUPPORTED_FORMATS:
        raise NotSupportedFormatError(config.SUPPORTED_FORMATS)

    # Перевірка розміру файлу
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > config.MAX_FILE_SIZE:
        raise MaxSizeExceedError(config.MAX_FILE_SIZE)

    # Перевірка валідності зображення
    try:
        image = Image.open(file.file)
        image.verify()
        file.file.seek(0)
    except (UnidentifiedImageError, OSError):
        raise NotSupportedFormatError(config.SUPPORTED_FORMATS)

    original_name = os.path.splitext(filename)[0].lower()
    original_name = ''.join(c for c in original_name if c.isalnum() or c in "_-")[:50]
    unique_name = f"{original_name}_{uuid.uuid4()}{ext}"

    os.makedirs(config.IMAGE_DIR, exist_ok=True)
    file_path = os.path.join(config.IMAGE_DIR, unique_name)

    # Збереження файлу
    with open(file_path, "wb") as f:
        file.file.seek(0)
        shutil.copyfileobj(file.file, cast(SupportsWrite, f))

    return {
        "filename": unique_name,
        "url": f"/images/{unique_name}"
    }
