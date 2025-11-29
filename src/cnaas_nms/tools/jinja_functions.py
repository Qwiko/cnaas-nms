"""Jinja filter functions for use in configuration templates"""

import base64
import hashlib
import ipaddress
import logging
import re
from typing import Any, Callable, Optional

from jinja2.exceptions import TemplateError
from netutils.config.parser import (
    BaseSpaceConfigParser,
    EOSConfigParser,
    IOSConfigParser,
    IOSXRConfigParser,
    JunosConfigParser,
    NXOSConfigParser,
)

from cnaas_nms.tools.log import get_logger

# This global dict can be used to update the Jinja environment global functions dict to include all
# registered template_function
FUNCTIONS = {}


def template_function(name: Optional[str] = None) -> Callable:
    """Registers a template function in the FUNCTIONS dict.

    Args:
        name: Optional alternative name to register the function as
    """

    def decorator(func):
        name_ = name if name else func.__name__
        FUNCTIONS[name_] = func
        return func

    return decorator


@template_function("raise")
def raise_helper(msg: str) -> None:
    """
    Raises TemplateError in templates.

    Usage: {{ raise("some exception") }}
    """
    raise TemplateError(msg)


@template_function()
def log(msg: str, level: str = "INFO", module_override: str = "render_template") -> str:
    """
    Log a message in templates.

    Usage:
        {{ log("some info log") }}
        {{ log("some specific warning log", "WARNING", "dist_render") }}

    Args:
        msg: Log message.
        level: Log level, CRITICAL, ERROR, WARNING, INFO, DEBUG.
        module_override: Override module in log-message. Defaults to render_template.

    Returns:
        Empty string ""
    """
    logger = get_logger()
    lvl: int = getattr(logging, str(level).upper(), None)
    if not lvl or not isinstance(lvl, int):
        logger.error(f"{level} is not a valid log level, defaulting to INFO.")
        lvl = logging.INFO

    logger.log(lvl, msg, extra={"module_override": module_override})
    return ""
