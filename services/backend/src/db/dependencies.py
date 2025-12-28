from typing import Optional

from src.db.session import get_connection_pool
from src.db.repositories import PostgresImageRepository
from src.interfaces.repositories import ImageRepository


_image_repository: Optional[ImageRepository] = None

def get_image_repository() -> ImageRepository:
    global _image_repository
    if _image_repository is None:
        pool = get_connection_pool()
        _image_repository = PostgresImageRepository(pool)
    return _image_repository