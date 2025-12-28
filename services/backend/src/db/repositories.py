from typing import List, Optional
from psycopg_pool import ConnectionPool
from psycopg.errors import Error as PsycopgError

from src.interfaces.repositories import ImageRepository, ImageDTO, ImageDetailsDTO
from src.exceptions.repository_errors import EntityCreationError, EntityDeletionError, QueryExecutionError


class PostgresImageRepository(ImageRepository):
    def __init__(self, pool: ConnectionPool):
        self._pool = pool

    def create(self, image: ImageDTO) -> ImageDetailsDTO:
        query = """
            INSERT INTO images (filename, original_name, size, file_type)
            VALUES (%s, %s, %s, %s)
            RETURNING id, upload_time
        """
        try:
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        query,
                        (image.filename, image.original_filename, image.size, image.file_type),
                    )
                    db_id, upload_time = cur.fetchone()
                    conn.commit()

                    return ImageDetailsDTO(
                        id=db_id,
                        filename=image.filename,
                        original_filename=image.original_filename,
                        size=image.size,
                        file_type=image.file_type,
                        upload_time=upload_time.isoformat() if upload_time else None,
                    )
        except PsycopgError as e:
            raise EntityCreationError("Image", str(e))

    def get_by_id(self, image_id: int) -> Optional[ImageDetailsDTO]:
        query = """
            SELECT id, filename, original_name, size, upload_time, file_type::text
            FROM images
            WHERE id = %s
        """
        try:
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (image_id,))
                    result = cur.fetchone()
                    if not result:
                        return None
                    db_id, filename, original_name, size, upload_time, file_type = result
                    return ImageDetailsDTO(
                        id=db_id,
                        filename=filename,
                        original_filename=original_name,
                        size=size,
                        upload_time=upload_time.isoformat() if upload_time else None,
                        file_type=file_type,
                    )
        except PsycopgError as e:
            raise QueryExecutionError("get_by_id", str(e))

    def get_by_filename(self, filename: str) -> Optional[ImageDetailsDTO]:
        query = """
            SELECT id, filename, original_name, size, upload_time, file_type::text
            FROM images
            WHERE filename = %s
        """
        try:
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (filename,))
                    result = cur.fetchone()
                    if not result:
                        return None
                    db_id, filename, original_name, size, upload_time, file_type = result
                    return ImageDetailsDTO(
                        id=db_id,
                        filename=filename,
                        original_filename=original_name,
                        size=size,
                        upload_time=upload_time.isoformat() if upload_time else None,
                        file_type=file_type,
                    )
        except PsycopgError as e:
            raise QueryExecutionError("get_by_filename", str(e))

    def delete(self, image_id: int) -> bool:
        query = "DELETE FROM images WHERE id = %s RETURNING id"
        try:
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (image_id,))
                    result = cur.fetchone()
                    conn.commit()
                    return result is not None
        except PsycopgError as e:
            raise EntityDeletionError("Image", image_id, str(e))

    def delete_by_filename(self, filename: str) -> bool:
        query = "DELETE FROM images WHERE filename = %s RETURNING id"
        try:
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (filename,))
                    result = cur.fetchone()
                    conn.commit()
                    return result is not None
        except PsycopgError as e:
            raise EntityDeletionError("Image", filename, str(e))

    def list_all(self, limit: int = 10, offset: int = 0, order: str = "desc") -> List[ImageDetailsDTO]:
        if order.lower() not in ("desc", "asc"):
            raise ValueError("Order parameter must be 'desc' or 'asc'")
        query = f"""
            SELECT id, filename, original_name, size, upload_time, file_type::text
            FROM images
            ORDER BY upload_time {order.upper()}
            LIMIT %s OFFSET %s
        """
        try:
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (limit, offset))
                    results = cur.fetchall()
                    return [
                        ImageDetailsDTO(
                            id=row[0],
                            filename=row[1],
                            original_filename=row[2],
                            size=row[3],
                            upload_time=row[4].isoformat() if row[4] else None,
                            file_type=row[5],
                        )
                        for row in results
                    ]
        except PsycopgError as e:
            raise QueryExecutionError("list_all", str(e))

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM images"
        try:
            with self._pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    result = cur.fetchone()
                    return result[0]
        except PsycopgError as e:
            raise QueryExecutionError("count", str(e))
