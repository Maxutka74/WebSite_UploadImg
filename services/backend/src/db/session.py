from typing import Optional
from psycopg_pool import ConnectionPool
from src.settings.config import config

_pool: Optional[ConnectionPool] = None

def get_connection_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
        conninfo = config.db_url,
        min_size = 2,
        max_size = 10,
        open=True
        )
    return _pool