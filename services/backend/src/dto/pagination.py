from dataclasses import dataclass
from typing import Tuple

@dataclass
class PaginationDTO:
    page: int
    per_page: int

    @staticmethod
    def to_limit_offset(page: int, per_page: int) -> Tuple[int, int]:
        return per_page, (page - 1) * per_page

    def to_sql_params(self) -> Tuple[int, int]:
        return self.to_limit_offset(self.page, self.per_page)