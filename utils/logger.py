import logging
import os
import sys
import colorama

colorama.init()


class ColorFormatter(logging.Formatter):
    """
    The ColorFormatter class provides methods for formatting log messages with color (ansi escape codes)
    """

    # Colors
    grey = colorama.Fore.WHITE
    blue = colorama.Fore.BLUE
    yellow = colorama.Fore.YELLOW
    red = colorama.Fore.RED
    bold_red = colorama.Fore.RED + colorama.Style.BRIGHT
    reset = colorama.Fore.RESET
    format = "[%(asctime)s - %(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"  # log message format
    datefmt = "%m-%d-%Y, %X"

    FORMATS = {  # set the log colors for each level
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):  # override the format method
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Formatter(logging.Formatter):
    """
    The Formatter class provides methods for formatting log messages without color
    """

    format = "[%(asctime)s - %(name)s - %(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"  # log message format
    datefmt = "%Y-%m-%d %H:%M:%S"

    FORMATS = {  # set the log format for each level
        logging.DEBUG: format,
        logging.INFO: format,
        logging.WARNING: format,
        logging.ERROR: format,
        logging.CRITICAL: format,
    }

    def format(self, record):  # override the format method
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger(logging.Logger):
    """
    A custom logger with handlers for logging to a file and standard (console) output.
    """

    def __init__(self):
        super().__init__("afkbot")

    afkbot_logger = logging.getLogger("afkbot")
    afkbot_logger.setLevel(
        logging.DEBUG
    )  # Set the afkbot_logger level to debug for testing

    if not afkbot_logger.handlers:  # prevent duplicate messages
        file_handler = logging.FileHandler(
            filename=os.path.join(os.path.dirname(__file__), "..", "afkbot.log"),
            encoding="utf-8",
            mode="w",
        )
        file_handler.setFormatter(Formatter())

        console_handler = logging.StreamHandler(
            sys.stdout
        )  # Use sys.stdout for standard output
        console_handler.setFormatter(ColorFormatter())

        afkbot_logger.addHandler(console_handler)
        afkbot_logger.addHandler(file_handler)
