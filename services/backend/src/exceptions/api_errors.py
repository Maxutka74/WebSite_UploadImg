class APIError(Exception):
    status_code = 400
    message = "API Error"

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)


class NotSupportedFormatError(APIError):
    def __init__(self, supported_formats: set[str]):
        formats_list = ", ".join(sorted(supported_formats))
        message = f"Unsupported file format. Supported formats: {formats_list}."
        super().__init__(message)


class MaxSizeExceedError(APIError):
    def __init__(self, max_size_bytes: int):
        max_size_mb = max_size_bytes / (1024 * 1024)
        message = f"File size exceeds the maximum allowed size of {max_size_mb:.1f} MB."
        super().__init__(message)


class MultipleFilesUploadError(APIError):
    def __init__(self):
        message = "Only one file can be uploaded per request."
        super().__init__(message)



class FileNotFoundError(APIError):
    status_code = 404

    def __init__(self, filename: str = None):
        message = "File not found."
        if filename:
            message = f"File '{filename}' not found."
        super().__init__(message)


class PermissionDeniedError(APIError):
    status_code = 500

    def __init__(self, operation: str = None):
        message = "Permission denied."
        if operation:
            message = f"Permission denied to {operation}."
        super().__init__(message)


class UnsupportedFileFormatError(APIError):
    def __init__(self, extension: str = None, supported_formats: set[str] = None):
        if extension and supported_formats:
            formats_list = ", ".join(sorted(supported_formats))
            message = f"Unsupported file format '{extension}'. Supported formats: {formats_list}."
        elif supported_formats:
            formats_list = ", ".join(sorted(supported_formats))
            message = f"Unsupported file format. Supported formats: {formats_list}."
        else:
            message = "Unsupported file format."
        super().__init__(message)