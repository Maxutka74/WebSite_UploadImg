from typing import Any


class PaginationError(Exception):
    pass


class InvalidPageNumberError(PaginationError):
    def __init__(self, value: Any):
        self.value = value
        super().__init__(f"Invalid page number: {value}. Page number must be a positive integer.")


class InvalidPerPageError(PaginationError):
    def __init__(self, value: Any):
        self.value = value
        super().__init__(f"Invalid per_page value: {value}. Per page must be a positive integer.")
