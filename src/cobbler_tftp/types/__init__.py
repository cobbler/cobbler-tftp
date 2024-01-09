"""Custom types and aliases required to make typing in cobbler-tftp easier."""

from pathlib import Path
from typing import Dict, Union

# Dictionary type for configuration parameters
# if this type changes: changes __valdiate_module function in migrations/__init__.py
SettingsDict = Dict[
    str, Union[float, bool, str, Path, Dict[str, Union[int, str, Path]]]
]
