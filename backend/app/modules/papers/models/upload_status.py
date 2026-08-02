from enum import Enum


class UploadStatus(str, Enum):
    """
    Current processing state of a paper.
    """

    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"