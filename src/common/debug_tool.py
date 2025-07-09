import logging
import os
import sys
import traceback
from logging.handlers import TimedRotatingFileHandler


class _RouteFilter(logging.Filter):
    _msg_list = [
        '/probe',
    ]

    def _check_message(self, _str):
        for msg in self._msg_list:
            if msg in _str:
                return False
        return True

    def filter(self, record):
        _str = record.getMessage()
        return self._check_message(_str=_str)


class _FileLogger:
    """
    local file
    """

    _ABS_PATH = os.path.abspath('.')
    _SETTINGS = {
        'debug': ('/debug_log/', logging.DEBUG),
        'info': ('/info_log/', logging.INFO),
        'warning': ('/warning_log/', logging.WARNING),
        'error': ('/error_log/', logging.ERROR),
        'critical': ('/critical_log/', logging.CRITICAL),
    }

    @classmethod
    def _create_path(cls, root):
        for key, (path, level) in cls._SETTINGS.items():
            folder_path = f'{cls._ABS_PATH}{root}{path}'
            os.makedirs(folder_path, exist_ok=True)

    @staticmethod
    def _get_handler(file_path, level=logging.DEBUG):
        console = TimedRotatingFileHandler(
            file_path,
            when='H',
            interval=1,
            backupCount=10000,
            encoding=None,
            delay=False,
            utc=False,
        )
        console.setLevel(level)
        formatter = logging.Formatter('[%(asctime)-s] [%(levelname)-8s] [%(message)s]')
        console.setFormatter(formatter)
        console.addFilter(_RouteFilter())
        return console

    @classmethod
    def get_handlers(cls, tag, root='/logs'):
        cls._create_path(root)
        console_list = list()
        for key, (path, level) in cls._SETTINGS.items():
            folder_path = f'{cls._ABS_PATH}{root}{path}'
            file_name = f'{tag}.log'
            file_path = f'{folder_path}{file_name}'
            file_handler = cls._get_handler(file_path, level)
            console_list.append(file_handler)
        return console_list


class _PrintLogger:
    """
    print on terminal
    """

    @staticmethod
    def get_handler(level=logging.DEBUG):
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)-8s] [%(message)s]')
        console.setFormatter(formatter)
        console.addFilter(_RouteFilter())
        return console


class DebugTool:
    """
    How to start:

        1. Set Logger
            + to file
                DebugTool.add_file_logger(tag)

        2. Initial Logger
            DebugTool.start_logging()

    How to use:
        DebugTool.<method>(exception=<Exception object>, msg=<message string>)

    *** error and critical method can logged traceback ***

    Example:

        try:
            ...

        except IOError as e:

            DebugTool.debug(e)
            DebugTool.debug(msg='occur IOError exception')
            DebugTool.debug(e, msg='occur IOError exception')
    """

    _logger = None
    _consoles: list = list()
    _packages = [
        'requests',
        'urllib3',
    ]

    @classmethod
    def _set_loggers(cls):
        cls._logger = logging.getLogger()
        cls._logger.setLevel(logging.DEBUG)
        for console in cls._consoles:
            cls._logger.addHandler(console)

    @classmethod
    def _shield_info(cls):
        for package in cls._packages:
            logging.getLogger(package).setLevel(logging.WARNING)
        logging.captureWarnings(True)

    @staticmethod
    def _format(info, newline=False):
        result = '' if info is None else info
        return f'\n{result}' if result and newline else result

    @classmethod
    def _get_debug_info(cls, msg=None, exception=None, details=None):
        msg = cls._format(msg)
        exception = cls._format(exception)
        details = cls._format(details, newline=True)
        return f'<MESSAGE>: {msg} | <EXCEPTION>: {exception} | <TRACEBACK>: {details}'

    @classmethod
    def _logging(cls, method, exception=None, msg=None, verbose=False):
        details = traceback.format_exc().strip('\n') if verbose else None
        debug_info = cls._get_debug_info(msg, exception, details)
        method(str(debug_info))

    @classmethod
    def _validate(cls):
        if not cls._logger:
            raise Exception(f'[{cls.__name__}] need to been initialized.')

    @classmethod
    def _adapt(cls, exception, msg):
        """
        To prevent positions are mismatched
        Swap if detect the type of exception is odd
        """
        if isinstance(exception, str):
            return msg, exception
        return exception, msg

    @classmethod
    def _add_print_logger(cls):
        cls._consoles.append(_PrintLogger.get_handler())

    @classmethod
    def add_file_logger(cls, tag, root='/logs'):
        cls._consoles.extend(_FileLogger.get_handlers(tag, root))

    @classmethod
    def start_logging(cls):
        cls._add_print_logger()
        cls._set_loggers()
        cls._shield_info()

    @classmethod
    def debug(cls, exception=None, msg=None, verbose=False):
        cls._validate()
        exception, msg = cls._adapt(exception, msg)
        cls._logging(cls._logger.debug, exception, msg, verbose=verbose)

    @classmethod
    def info(cls, exception=None, msg=None, verbose=False):
        cls._validate()
        exception, msg = cls._adapt(exception, msg)
        cls._logging(cls._logger.info, exception, msg, verbose=verbose)

    @classmethod
    def warning(cls, exception=None, msg=None, verbose=False):
        cls._validate()
        exception, msg = cls._adapt(exception, msg)
        cls._logging(cls._logger.warning, exception, msg, verbose=verbose)

    @classmethod
    def error(cls, exception=None, msg=None, verbose=True):
        cls._validate()
        exception, msg = cls._adapt(exception, msg)
        cls._logging(cls._logger.error, exception, msg, verbose=verbose)

    @classmethod
    def critical(cls, exception=None, msg=None, verbose=True):
        cls._validate()
        exception, msg = cls._adapt(exception, msg)
        cls._logging(cls._logger.critical, exception, msg, verbose=verbose)
