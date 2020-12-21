#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK


import pathlib
import logging
import logging.config
import argparse
import argcomplete
from argcomplete.completers import EnvironCompleter as EC
from itertools import filterfalse
# Own modules
from starter import logging_conf
from starter import errors
from starter import utils
from starter import config_loader
from starter import version


# Setup logging
def setup_logging_directory(directory: pathlib.Path) -> tuple[logging.Logger, pathlib.Path]:
    """
    Returns a logger and a path to directory where the logs are saved
    """
    try:
        path_to_dir = utils.provide_dir(directory)
        logger_config = logging_conf.create_dict_config(path_to_dir, "debug.log", "info.log", "errors.log")
    except FileExistsError:
        logger.error(f"Failed to create the directory `{str(path_to_dir)}` because it already exists as a file.")
        logger.error(f"Please create the directory `{str(path_to_dir)}`")
    finally:
        logging.config.dictConfig(logger_config)
        logger = logging.getLogger(__name__)
    return logger, path_to_dir


logger, path_to_dir = setup_logging_directory(pathlib.Path.home() / utils.dir_name)


def argument_parser() -> argparse.ArgumentParser:
    """
    Creates an argument parser for command line arguments
    """
    parser = argparse.ArgumentParser(description="starter")
    parser.add_argument("-v", "--version", action="store_true", help="print out starter version and exit").completer = EC
    parser.add_argument("--autoconfig", action="store_true", help="Configure starter automatically").completer = EC
    return parser


def run(config: config_loader.Config) -> None:
    pass


def cli_start(version) -> None:
    """
    Entry point for any component start from the commmand line
    """
    logger.debug(f"{utils.program_name} started")
    parser = argument_parser()
    argcomplete.autocomplete(parser)
    cli_args = parser.parse_args()
    logger.debug(f"Parsed arguments: {cli_args}")
    path_to_config = path_to_dir / utils.configuration_file_name
    try:
        if cli_args.version:
            logger.info(f"{version}")
        else:
            with config_loader.Config(path_to_config, cli_args.autoconfig) as config:
                config.cli_args = cli_args
                run(config)
    except errors.WrongConfiguration as err:
        logger.error(err.message)
    except Exception as err:
        logger.exception(f"Uncaught exception {repr(err)} occurred.")
    logger.debug(f"{utils.program_name} ended")


if __name__ == "__main__":
    pass
