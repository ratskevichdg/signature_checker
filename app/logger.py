from loguru import logger


logger.add(
    "../logs/api_logs.log",
    format="{time} :: {level} :: {message}",
    level="WARNING",
    rotation="1 MB",
    compression="zip"
)
