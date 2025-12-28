import os
import uuid
import shutil
from typing import cast, List, Callable, Any

from PIL import Image, UnidentifiedImageError

from src.dto.file import UploadedFileDTO
from src.settings.config import config
from src.exceptions.api_errors import (
    NotSupportedFormatError,
    MaxSizeExceedError,
    MultipleFilesUploadError,
    UnsupportedFileFormatError,
    PermissionDeniedError,
    FileNotFoundError,
    APIError
)
from src.interfaces.protocols import SupportsWrite
from src.interfaces.handlers import FileHandlerInterface


class FileHandler(FileHandlerInterface):
    def __init__(
            self,
            images_dir: str = config.IMAGE_DIR,
            max_file_size: int = config.MAX_FILE_SIZE,
            supported_formats: set[str] = config.SUPPORTED_FORMATS
    ):
        self._images_dir = images_dir
        self._max_file_size = max_file_size
        self._supported_formats = supported_formats

    def handle_upload(self, file) -> UploadedFileDTO:
        filename = file.filename if hasattr(file, "filename") else "uploaded_file"
        ext = os.path.splitext(filename)[1].lower()

        if ext not in self._supported_formats:
            raise NotSupportedFormatError(self._supported_formats)

        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)

        if size > self._max_file_size:
            raise MaxSizeExceedError(self._max_file_size)

        try:
            image = Image.open(file.file)
            image.verify()
            file.file.seek(0)
        except (UnidentifiedImageError, OSError):
            raise NotSupportedFormatError(self._supported_formats)

        original_name = os.path.splitext(filename)[0].lower()
        original_name = ''.join(c for c in original_name if c.isalnum() or c in '_-')[:50]
        unique_name = f"{original_name}_{uuid.uuid4()}{ext}"
        os.makedirs(self._images_dir, exist_ok=True)
        file_path = os.path.join(self._images_dir, unique_name)

        with open(file_path, "wb") as f:
            file.file.seek(0)
            shutil.copyfileobj(file.file, cast(SupportsWrite, f))

        return UploadedFileDTO(
            filename=unique_name,
            original_filename=filename,
            size=size,
            extension=ext,
            url=f"/images/{unique_name}"
        )

    def get_file_collector(self, files_list: List) -> Callable[[Any], None]:
        def on_file(file):
            if len(files_list) >= 1:
                raise MultipleFilesUploadError()
            files_list.append(file)

        return on_file

    def delete_file(self, filename: str) -> None:
        filepath = os.path.join(self._images_dir, filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext not in self._supported_formats:
            raise UnsupportedFileFormatError(ext, self._supported_formats)

        if not os.path.isfile(filepath):
            raise FileNotFoundError(filename)

        try:
            os.remove(filepath)
        except PermissionError:
            raise PermissionDeniedError("delete file")
        except Exception as e:
            raise APIError(f"Failed to delete file: {str(e)}")
