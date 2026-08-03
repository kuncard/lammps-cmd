"""
Shared logging setup — single point of configuration for all project scripts.
Ensures consistent format and log level whether running standalone or via import.

Usage:
  from logging_setup import setup_logging
  log = setup_logging(__name__)
  log.info("message")
  log.warning("warning")
  log.error("error")
"""
import logging


def setup_logging(name=None):
    """Configure root logger and return a module-specific logger.

    Only calls basicConfig once (idempotent after first call).
    Name defaults to __name__ of caller.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger(name or __name__)
