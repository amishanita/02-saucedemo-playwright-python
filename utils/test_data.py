import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

# Overridable so the suite can point at a different environment.
BASE_URL: str = os.environ.get("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com/")

DATA_FILE: Path = Path(__file__).parent.parent / "test-data" / "users.json"


@lru_cache(maxsize=1)
def load() -> Dict[str, Any]:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_user(key: str) -> Dict[str, str]:
    return load()["users"][key]


def get_all_users() -> Dict[str, Dict[str, str]]:
    return load()["users"]


def get_checkout_info() -> Dict[str, str]:
    return load()["checkout"]


def get_product_name(key: str) -> str:
    return load()["products"][key]


def get_all_products() -> List[str]:
    return list(load()["products"].values())
