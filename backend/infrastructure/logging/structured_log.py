import json
import time
import uuid

class StructuredLogger:
    _correlation_id = None

    @classmethod
    def set_correlation_id(cls, cid: str = None):
        cls._correlation_id = cid or str(uuid.uuid4())

    @classmethod
    def get_correlation_id(cls) -> str:
        if cls._correlation_id is None:
            cls.set_correlation_id()
        return cls._correlation_id

    @classmethod
    def clear_correlation_id(cls):
        cls._correlation_id = None

    @classmethod
    def _log(cls, level: str, message: str, context: dict = None):
        log_entry = {
            "timestamp": int(time.time()),
            "level": level,
            "correlation_id": cls.get_correlation_id(),
            "message": message,
            "context": context or {}
        }
        print(json.dumps(log_entry), flush=True)

    @classmethod
    def info(cls, message: str, context: dict = None):
        cls._log("INFO", message, context)

    @classmethod
    def warn(cls, message: str, context: dict = None):
        cls._log("WARN", message, context)

    @classmethod
    def error(cls, message: str, context: dict = None):
        cls._log("ERROR", message, context)
