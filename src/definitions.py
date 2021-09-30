import os
import logging.config
import types

# code from: https://gitlab.gistools.geog.uni-heidelberg.de/giscience/disaster-tools/health_access/isochrone_access/-/blob/master/src/definitions.py

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

CONFIG_DIR = os.path.join(ROOT_DIR, "../config/")

# CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DATA_PATH = os.path.join(ROOT_DIR, "../data/")

LOGGING_CONFIG_PATH = os.path.join(CONFIG_DIR, "logging.cfg")

LOG_PATH = os.path.join(ROOT_DIR, "../logs/")

# FILTERS_PATH = os.path.join(CONFIG_DIR, "subject_filters.json")

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING_FILE_PATH = os.path.join(LOG_PATH, "isochrone_access.log")
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"standard": {"format": "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"},},  # noqa E501
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "standard"},
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
        "root": {"handlers": ["console"], "level": "INFO"},
        "isochrone_access": {"handlers": ["console", "file"], "level": "INFO", "propagate": True},
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("isochrone_access")
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("shapely").setLevel(logging.WARNING)
logging.getLogger("oauth2client.crypt").setLevel(logging.WARNING)
logging.getLogger("fiona.env").setLevel(logging.WARNING)
logging.getLogger("fiona._env").setLevel(logging.WARNING)
logging.getLogger("Fiona").setLevel(logging.WARNING)
logging.getLogger("fiona.ogrext").setLevel(logging.WARNING)
logging.getLogger("fiona.collection").setLevel(logging.WARNING)

def alter_logger_format(self, identifier: str, subject: str):
    """Take an logger object and change the format, for better details."""
    formatter = logging.Formatter(
        f"%(asctime)s - %(levelname)s - %(funcName)s - {identifier} - {subject} - %(message)s"
    )  # noqa E501
    for item in self.handlers:
        item.setFormatter(formatter)


def reset_logger_format(self):
    """Reset logger format to standard scheme."""
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")  # noqa E501
    for item in self.handlers:
        item.setFormatter(formatter)


logger.alter_format = types.MethodType(alter_logger_format, logger)  # type: ignore[attr-defined]
logger.reset_format = types.MethodType(reset_logger_format, logger)  # type: ignore[attr-defined]

