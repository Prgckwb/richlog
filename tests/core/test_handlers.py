import json
import logging
import tempfile
from pathlib import Path

from richlog.core.handlers import AsyncHandler, BufferedHandler, FileHandler, JSONHandler


class TestFileHandler:
    def test_creates_file_handler(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            handler = FileHandler(f.name)
            assert handler.baseFilename == f.name
            Path(f.name).unlink()

    def test_file_handler_with_rotation(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            handler = FileHandler(
                f.name,
                max_bytes=1024,  # 1KB
                backup_count=5,
            )
            assert handler.maxBytes == 1024
            assert handler.backupCount == 5
            Path(f.name).unlink()

    def test_writes_log_to_file(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            handler = FileHandler(f.name)
            handler.setFormatter(logging.Formatter("%(message)s"))

            logger = logging.getLogger("test_file_logger")
            logger.handlers.clear()  # 既存のハンドラーをクリア
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            logger.info("Test message")
            handler.close()
            logger.removeHandler(handler)  # ハンドラーを削除

            content = Path(f.name).read_text()
            assert "Test message" in content
            Path(f.name).unlink()


class TestJSONHandler:
    def test_creates_json_handler(self) -> None:
        handler = JSONHandler()
        assert handler is not None

    def test_formats_log_as_json(self) -> None:
        handler = JSONHandler()

        # JSON形式でログレコードを整形することを確認
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        formatted = handler.format(record)
        data = json.loads(formatted)

        assert data["name"] == "test"
        assert data["level"] == "INFO"
        assert data["message"] == "Test message"
        assert data["pathname"] == "test.py"
        assert data["lineno"] == 10
        assert "timestamp" in data

    def test_includes_extra_fields(self) -> None:
        handler = JSONHandler()

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # 追加フィールドを設定
        record.user_id = "123"
        record.request_id = "abc-456"

        formatted = handler.format(record)
        data = json.loads(formatted)

        assert data["extra"]["user_id"] == "123"
        assert data["extra"]["request_id"] == "abc-456"


class TestAsyncHandler:
    def test_creates_async_handler(self) -> None:
        base_handler = logging.StreamHandler()
        handler = AsyncHandler(base_handler)
        assert handler is not None
        # クリーンアップ
        handler.close()

    def test_queues_messages(self) -> None:
        # AsyncHandlerがメッセージをキューに入れることを確認
        base_handler = logging.StreamHandler()
        handler = AsyncHandler(base_handler)

        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        handler.emit(record)
        # キューにレコードが追加されたことを確認
        assert not handler.queue.empty()

        # クリーンアップ
        handler.close()

    def test_processes_messages_asynchronously(self) -> None:
        # 非同期処理のテスト(実装により詳細は変わる)
        pass


class TestBufferedHandler:
    def test_creates_buffered_handler(self) -> None:
        base_handler = logging.StreamHandler()
        handler = BufferedHandler(base_handler, buffer_size=10)
        assert handler.buffer_size == 10

    def test_buffers_messages(self) -> None:
        base_handler = logging.StreamHandler()
        handler = BufferedHandler(base_handler, buffer_size=3)

        # バッファサイズ未満のメッセージを送信
        for i in range(2):
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname="test.py",
                lineno=10,
                msg=f"Message {i}",
                args=(),
                exc_info=None,
            )
            handler.emit(record)

        # バッファ内にメッセージが保持されていることを確認
        assert len(handler.buffer) == 2

    def test_flushes_on_buffer_full(self) -> None:
        # バッファがいっぱいになったときにフラッシュされることを確認
        from io import StringIO

        stream = StringIO()
        base_handler = logging.StreamHandler(stream)
        base_handler.setFormatter(logging.Formatter("%(message)s"))
        base_handler.setLevel(logging.DEBUG)  # レベルを明示的に設定

        handler = BufferedHandler(base_handler, buffer_size=2)
        handler.setLevel(logging.DEBUG)  # レベルを明示的に設定

        # バッファサイズ分のメッセージを送信
        for i in range(2):
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname="test.py",
                lineno=10,
                msg=f"Message {i}",
                args=(),
                exc_info=None,
            )
            handler.emit(record)

        # フラッシュされてストリームに書き込まれたことを確認
        output = stream.getvalue()
        assert "Message 0" in output
        assert "Message 1" in output

        # クリーンアップ
        handler.close()
