# Gives definitions about static path variables and encompasses logger settings.
import logging
from logging import config
from pathlib import Path

ROOT_DIR = Path.cwd()

CONFIG_DIR = ROOT_DIR / "config"

LOGGING_CONFIG_PATH = CONFIG_DIR / "logging.cfg"

LOG_DIR = ROOT_DIR / "logs"

LOGGING_ALL = LOG_DIR / "all_messages.log"
LOGGING_WARNINGS = LOG_DIR / "warning_n_above.log"

DATA_PATH = ROOT_DIR / "data"

INPUT_PATH = ROOT_DIR / "input"

INPUT_PATH_DOWNLOAD = INPUT_PATH / "input_download.txt"
INPUT_PATH_GPD = INPUT_PATH / "input_gpd.txt"
INPUT_PATH_BOKEH = INPUT_PATH / "input_bokeh.txt"

if not DATA_PATH.exists():
    DATA_PATH.mkdir()

if not LOG_DIR.exists():
    LOG_DIR.mkdir()

log_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "main": {"handlers": ["console_main"], "level": "INFO", "propagate": False},
        "function": {"handlers": ["console_function", "file_all", "file_warnings"], "level": "DEBUG", "propagate": False},
    },
    "handlers": {
        "console": {"formatter": "std_out", "class": "logging.StreamHandler", "level": "DEBUG"},
        "console_main": {"formatter": "std_out_main", "class": "logging.StreamHandler", "level": "INFO"},
        "console_function": {"formatter": "std_out_function", "class": "logging.StreamHandler", "level": "DEBUG"},
        "file_all": {
            "formatter": "std_out_function",
            "class": "logging.handlers.RotatingFileHandler",  # when file size is reached, begin on top
            "level": "INFO",
            "mode": "a",  # append
            "maxBytes": 1e7,  # 10 MB
            "filename": LOGGING_ALL,
        },
        "file_warnings": {
            "formatter": "std_out_function",
            "class": "logging.handlers.RotatingFileHandler",  # when file size is reached, begin on top
            "level": "WARNING",
            "mode": "a",  # append
            "maxBytes": 1e7,  # 10 MB
            "filename": LOGGING_WARNINGS,
        },
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(name)s : %(funcName)s : %(lineno)d : %(message)s",
            "datefmt": "%Y-%m-%d %I:%M:%S",
        },
        "std_out_main": {
            "format": "%(asctime)s : %(levelname)s : %(name)s : %(funcName)s : %(message)s",
            "datefmt": "%Y-%m-%d %I:%M:%S",
        },
        "std_out_function": {
            "format": "%(levelname)s : File:%(module)s : Func:%(funcName)s : %(lineno)d : LOG : %(message)s",  # %(asctime)s :
            "datefmt": "%Y-%m-%d %I:%M:%S",
        },
    },
}

config.dictConfig(log_config)
################ Logger #################
logger_m = logging.getLogger("main")
logger_f = logging.getLogger("function")

logging.config.dictConfig(log_config)

logger = logging.getLogger("mapper")
logging.getLogger("shapely").setLevel(logging.WARNING)
logging.getLogger("oauth2client.crypt").setLevel(logging.WARNING)
logging.getLogger("fiona.env").setLevel(logging.WARNING)
logging.getLogger("fiona._env").setLevel(logging.WARNING)
logging.getLogger("Fiona").setLevel(logging.WARNING)
logging.getLogger("fiona.ogrext").setLevel(logging.WARNING)
logging.getLogger("fiona.collection").setLevel(logging.WARNING)
