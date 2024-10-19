import logging
import subprocess


def create_logger(
    logger_name: str = None,
    log_file: str = None,
    level: str = "INFO",
    level_logfile: str = None,
    format_: str = "info",
) -> logging.Logger:
    """Create and configure a logger with console and optional file handlers."""

    # Define logging levels and formats
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    format_map = {
        "debug": "%(name)s - %(levelname)s: %(message)s | %(funcName)s:%(lineno)d",
        "info": "%(name)s - %(levelname)s: %(message)s",
        "file": "%(asctime)s | %(name)s - %(levelname)s: %(message)s",
    }

    # Set console and file logging levels
    c_level = level_map.get(level, logging.INFO)
    f_level = level_map.get(level_logfile, c_level)

    # Set logging formats
    format_console = format_map.get(format_, format_map["info"])
    format_file = format_map["file"]

    # Determine the logger name
    if not logger_name:
        logger_name = __name__

    # Create and configure the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(c_level)  # Ensures the logger can handle the specified log level

    # Create console handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(c_level)
    c_handler.setFormatter(logging.Formatter(format_console))
    logger.addHandler(c_handler)

    # Create file handler if log_file is specified
    if log_file:
        f_handler = logging.FileHandler(log_file, mode="a")
        f_handler.setLevel(f_level)
        f_handler.setFormatter(logging.Formatter(format_file, "%Y-%b-%d %H:%M:%S"))
        logger.addHandler(f_handler)

    return logger


def check_installation(
    package_name: str,
    git_repo: str = None,
    auto_install: bool = False,
    extra_commands: list[str] = None,
) -> None:
    """Check if the required packages are installed"""
    try:
        __import__(package_name)
    except ImportError:
        if auto_install:
            _install_package(package_name, git_repo)
            if extra_commands:
                for command in extra_commands:
                    subprocess.run(command, check=True)
        else:
            raise ImportError(
                f"Required package `{package_name}` is not installed. Please install the package.",
            )


def _install_package(package_name: str, git_repo: str = None) -> None:
    """Install the required package

    Args:
    ----
        package_name (str): package name
        git_repo (str): git path for the package

    """
    from .general_utils import create_logger

    logger = create_logger()

    try:
        logger.info(f"Installing the required packages: `{package_name}` ...")
        if git_repo:
            command = f"pip install -U git+{git_repo}"
        else:
            command = f"pip install -U {package_name}"

        subprocess.run(command, check=True)

        logger.info("Installation successful!")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while installing the package: {e}")


def get_func_args(func):
    """Get the arguments of a function"""
    import inspect

    argspec = inspect.getfullargspec(func)
    no_default_args = ["no_default_value"] * (len(argspec.args) - len(argspec.defaults))
    all_values = no_default_args + list(argspec.defaults)
    argsdict = dict(zip(argspec.args, all_values))
    return argsdict
