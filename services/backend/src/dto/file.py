from dataclasses import dataclass, field
from typing import Optional
import datetime

@dataclass
class UploadedFileDTO:
    filename: str
    original_filename: str  # <- замінив original_name
    size: int
    extension: str
    url: str
    upload_time: datetime.datetime = field(default_factory=datetime.datetime.now)

    def as_dict(self) -> dict:
        return {
            "filename": self.filename,
            "original_filename": self.original_filename,  # <- теж змінив тут
            "size": self.size,
            "extension": self.extension,
            "url": self.url,
            "upload_time": self.upload_time.isoformat()
        }
