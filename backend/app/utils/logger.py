import logging
import sys
from typing import Optional

def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: Name of the logger
        level: Logging level (defaults to INFO if None)
        
    Returns:
        Configured logger instance
    """
    if level is None:
        level = logging.INFO
        
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# Create a default logger for the application
app_logger = setup_logger("resume_generator")

if __name__ == "__main__":
    app_logger.info("This is a test log message")
    app_logger.error("This is an error log message")
    app_logger.warning("This is a warning log message")     