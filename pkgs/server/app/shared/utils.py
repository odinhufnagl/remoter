import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import shutil
from typing import Any

import emails  # type: ignore
import jwt
from jinja2 import Template
from jwt.exceptions import InvalidTokenError

from app.core import security
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
