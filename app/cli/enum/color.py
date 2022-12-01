from enum import Enum


class Color(Enum):
    SELECTION_INDEX = "#00FFFF"

    MANUFACTURER = "#FF7B00"
    GROUP = "#80FF00"
    HOST = "#0078FF"

    COMMAND = "#BB00FF"
    COLLECTION = "#FFF788"
    VARIABLE = "#00FF99"

    EXECUTE = "#8DBDFF"

    PROCEED = "#FFFFFF"

    FAIL = "#FF0000"
    SUCCESS = "#00FF00"
