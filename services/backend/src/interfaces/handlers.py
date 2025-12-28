from abc import ABC, abstractmethod
from typing import List, Callable, Any

from src.dto.file import UploadedFileDTO


class FileHandlerInterface(ABC):

    @abstractmethod
    def handle_upload(self, file) -> UploadedFileDTO:
        pass

    @abstractmethod
    def get_file_collector(self, files_list: List) -> Callable[[Any], None]:
        pass

    @abstractmethod
    def delete_file(self, filename: str) -> None:
        pass