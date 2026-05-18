import logging
from app.config.settings import settings

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger with the configured level and format.
    """
    logger = logging.getLogger(name)
    if not logger.handlers: # Avoid adding handlers multiple times if called repeatedly
        logger.setLevel(settings.log_level)
        formatter = logging.Formatter(settings.log_format)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Optional: File handler for persistent logging
        # In a production environment, consider log rotation and more sophisticated logging systems.
        # file_handler = logging.FileHandler("app.log")
        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

    return logger

# Example of how to get a logger instance:
# logger = setup_logger(__name__)
# logger.info("This is an info message.")
# logger.error("This is an error message.")
