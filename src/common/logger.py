import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger

from .config import settings


class FunctionNameFilter(logging.Filter):
    """Add function name to log records in [function_name] format.

    Filters log records to format the function name with square brackets
    for improved visibility in log output.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Process a log record to format the function name.

        Args:
            record (logging.LogRecord): The log record to process.

        Returns:
            bool: Always returns True to allow the record through.
        """
        record.funcName = f"[{record.funcName}]"
        return True


def cleanup_old_logs(log_file_path: str, days: int = 3) -> None:
    """
    Remove log files older than specified number of days.

    Args:
        log_file_path (str): Path to the log file directory.
        days (int): Number of days to keep logs. Defaults to 3.
                   Files older than this will be deleted.

    Returns:
        None

    Example:
        cleanup_old_logs("logs/activity.log", days=3)
        # Removes all log files in logs/ directory older than 3 days
    """
    try:
        log_path = Path(log_file_path)
        log_dir = log_path.parent

        if not log_dir.exists():
            return

        cutoff_time = datetime.now() - timedelta(days=days)

        for log_file in log_dir.glob(f"{log_path.stem}*"):
            if log_file.is_file():
                file_mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_mtime < cutoff_time:
                    try:
                        log_file.unlink()
                        logging.getLogger(__name__).debug(f"Removed old log file: {log_file}")
                    except OSError as e:
                        logging.getLogger(__name__).warning(f"Failed to remove log file {log_file}: {str(e)}")
    except Exception as e:
        logging.getLogger(__name__).error(f"Error cleaning up old logs: {str(e)}", exc_info=True)


def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger instance with file and console handlers.

    Sets up logging with JSON formatting, daily log rotation, 50MB file size limits,
    and automatic cleanup of logs older than 3 days. Includes optional console output
    when debug mode is enabled.

    Args:
        name (str): Name of the logger (typically __name__).

    Returns:
        logging.Logger: Configured logger instance ready for use.

    Features:
        - JSON-formatted log output
        - Daily rotation at midnight
        - 50MB max size per file
        - Automatic cleanup of logs older than 3 days
        - Optional console output in debug mode
        - Function names formatted with square brackets

    Example:
        logger = setup_logger(__name__)
        logger.info("Application started")
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    if logger.handlers:
        return logger

    # Clean up logs older than x days
    cleanup_old_logs(settings.log_file, settings.backlog_date)

    # Format: timestamp level logger [function_name] line - message
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(funcName)s %(lineno)d - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    log_path: Path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Rotate daily OR when file reaches 50MB (whichever comes first)
    file_handler = TimedRotatingFileHandler(
        filename=settings.log_file,
        when='midnight',
        interval=1,
        backupCount=30,         # Keep 30 days
        encoding='utf-8'
    )
    file_handler.suffix = "%Y-%m-%d"
    file_handler.maxBytes = 50 * 1024 * 1024  # 50MB max per file
    file_handler.setFormatter(formatter)
    file_handler.addFilter(FunctionNameFilter())
    logger.addHandler(file_handler)

    if settings.debug:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(FunctionNameFilter())
        logger.addHandler(console_handler)

    return logger


# Create default logger
logger = setup_logger(__name__)


