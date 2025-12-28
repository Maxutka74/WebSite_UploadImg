from abc import ABC, abstractmethod
from typing import List, Optional

from src.db.dto import ImageDTO, ImageDetailsDTO


class ImageRepository(ABC):

    @abstractmethod
    def create(self, image: ImageDTO) -> ImageDetailsDTO:
        pass

    @abstractmethod
    def get_by_id(self, image_id: int) -> Optional[ImageDetailsDTO]:
        pass

    @abstractmethod
    def get_by_filename(self, filename: str) -> Optional[ImageDetailsDTO]:
        pass

    @abstractmethod
    def delete(self, image_id: int) -> bool:
        pass

    @abstractmethod
    def delete_by_filename(self, filename: str) -> bool:
        pass

    @abstractmethod
    def list_all(self, limit: int = 10, offset: int = 0, order: str = "desc") -> List[ImageDetailsDTO]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
