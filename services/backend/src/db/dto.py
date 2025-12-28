from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class ImageDTO:
    filename: str
    original_filename: str
    size: int
    file_type: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass(kw_only=True)
class ImageDetailsDTO:
    id: int
    filename: str
    original_filename: str
    size: int
    file_type: str
    upload_time: Optional[str] = None  # upload_time може бути None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
