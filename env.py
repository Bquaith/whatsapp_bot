from typing import Any

import os

def getenv(env: str, default: Any, type: Any = str):
    return type(os.getenv(env) if os.getenv(env) else default)

TRY_AUTH = getenv("TRY_AUTH", 10, int)
TRY_AUTH_SLEEP = getenv("TRY_AUTH_SLEEP", 5, int)

LOAD_HOME_PAGE = getenv("LOAD_HOME_PAGE", 20, int)

PATH_TO_PROF = getenv("PATH_TO_PROF", "./.chrome_prof")

MAGIC_SLEEP = getenv("MAGIC_SLEEP", 1, int)