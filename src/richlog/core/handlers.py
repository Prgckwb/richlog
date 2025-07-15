import json
import logging
import queue
import threading
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from typing import Any, Optional


class FileHandler(RotatingFileHandler):
    def __init__(
        self,
        filename: str,
        mode: str = "a",
        max_bytes: int = 0,
        backup_count: int = 0,
        encoding: Optional[str] = None,
        delay: bool = False,
    ) -> None:
        super().__init__(
            filename,
            mode=mode,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=encoding,
            delay=delay,
        )


class JSONHandler(logging.Handler):
    def format(self, record: logging.LogRecord) -> str:
        # Basic fields
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
            "thread": record.thread,
            "threadName": record.threadName,
            "process": record.process,
        }

        # Add error information if available
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)

        # Extract additional fields
        extra_fields = {}
        for key, value in record.__dict__.items():
            if key not in {
                "name",
                "msg",
                "args",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
                "taskName",
            }:
                extra_fields[key] = value

        if extra_fields:
            log_data["extra"] = extra_fields

        return json.dumps(log_data, ensure_ascii=False)


class AsyncHandler(logging.Handler):
    def __init__(self, base_handler: logging.Handler, queue_size: int = 1000) -> None:
        super().__init__()
        self.base_handler = base_handler
        self.queue: queue.Queue[Optional[logging.LogRecord]] = queue.Queue(maxsize=queue_size)
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.queue.put_nowait(record)
        except queue.Full:
            # Drop the log if queue is full
            pass

    def _worker(self) -> None:
        while not self._stop_event.is_set():
            try:
                record = self.queue.get(timeout=0.1)
                if record is not None:
                    self.base_handler.emit(record)
            except queue.Empty:
                continue
            except Exception:
                # Worker continues even if error occurs
                pass

    def close(self) -> None:
        self._stop_event.set()
        self._worker_thread.join(timeout=1.0)
        super().close()


class BufferedHandler(logging.Handler):
    def __init__(self, base_handler: logging.Handler, buffer_size: int = 100) -> None:
        super().__init__()
        self.base_handler = base_handler
        self.buffer_size = buffer_size
        self.buffer: list[logging.LogRecord] = []
        self._lock = threading.Lock()

    def emit(self, record: logging.LogRecord) -> None:
        should_flush = False
        with self._lock:
            self.buffer.append(record)
            if len(self.buffer) >= self.buffer_size:
                should_flush = True

        if should_flush:
            self.flush()

    def flush(self) -> None:
        with self._lock:
            records_to_flush = self.buffer.copy()
            self.buffer.clear()

        # Call emit outside the lock
        for record in records_to_flush:
            self.base_handler.emit(record)

        if hasattr(self.base_handler, "flush"):
            self.base_handler.flush()

    def close(self) -> None:
        self.flush()
        super().close()
