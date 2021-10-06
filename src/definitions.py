# gives definitions about static path variables and encompasses logger settings
import logging.config
import types
from pathlib import Path

# code from: https://gitlab.gistools.geog.uni-heidelberg.de/giscience/disaster-tools
# /health_access/isochrone_access/-/blob/master/src/definitions.py

ROOT_DIR = Path.cwd()

CONFIG_DIR = ROOT_DIR / "config"

DATA_PATH = ROOT_DIR / "data"

LOGGING_CONFIG_PATH = CONFIG_DIR / "logging.cfg"

LOG_PATH = ROOT_DIR / "logs"

INPUT_PATH_DOWNLOAD = DATA_PATH / "input_download.txt"
INPUT_PATH_PLOTLY = DATA_PATH / "input_plotly.txt"

if not DATA_PATH.exists():
    DATA_PATH.mkdir()

if not LOG_PATH.exists():
    LOG_PATH.mkdir()

LOGGING_FILE_PATH = LOG_PATH / "mapperlogger.log"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"},
        "error": {"format": "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"},
    },  # noqa E501
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": LOGGING_FILE_PATH,
            "mode": "a",
            "maxBytes": 1e7,
        },
    },
    "loggers": {
        "root": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "mapper": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

# logger = logging.getLogger(__name__)

logger = logging.getLogger("mapper")
# logging.getLogger("shapely").setLevel(logging.WARNING)
# logging.getLogger("oauth2client.crypt").setLevel(logging.WARNING)
# logging.getLogger("fiona.env").setLevel(logging.WARNING)
# logging.getLogger("fiona._env").setLevel(logging.WARNING)
# logging.getLogger("Fiona").setLevel(logging.WARNING)
# logging.getLogger("fiona.ogrext").setLevel(logging.WARNING)
# logging.getLogger("fiona.collection").setLevel(logging.WARNING)


def alter_logger_format(self, name: str, filter: str):
    """Take an logger object and change the format, for better details."""
    formatter = logging.Formatter(f"%(asctime)s - %(levelname)s - %(funcName)s - {name} - {filter} - %(message)s")  # noqa E501
    for item in self.handlers:
        item.setFormatter(formatter)


def reset_logger_format(self):
    """Reset logger format to standard scheme."""
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")  # noqa E501
    for item in self.handlers:
        item.setFormatter(formatter)


logger.alter_format = types.MethodType(alter_logger_format, logger)  # type: ignore[attr-defined]
logger.reset_format = types.MethodType(reset_logger_format, logger)  # type: ignore[attr-defined]
