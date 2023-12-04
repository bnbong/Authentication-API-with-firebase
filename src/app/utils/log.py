import logging

from app.core.settings import AppSettings

settings = AppSettings()

FORMAT: str = "%(levelname)s [%(asctime)s - %(name)s] :  %(message)s"
app_logger_level = logging.DEBUG if settings.LOGGING_LEVEL else logging.INFO

logging.basicConfig(format=FORMAT, level=app_logger_level)

logger = logging.getLogger()
