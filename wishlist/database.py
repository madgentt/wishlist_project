"""This module provides the Wishlist database functionality."""
# wishlist/database.py

import os
import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from wishlist import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "wishlist/"
)


class DBResponse(NamedTuple):
    wish_list: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_wishes(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_wishes(self, wish_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(wish_list, db, indent=4)
            return DBResponse(wish_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(wish_list, DB_WRITE_ERROR)


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the wishes database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the wishes database."""
    try:
        if not os.path.exists(path=Path(db_path).parent):
            os.mkdir(path=Path(db_path).parent)
        db_path.write_text("[]")  # Empty wishes list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
