import sys
import platform
import importlib.resources as resources
from pathlib import Path

_TOOLS = {
    "windows": {
        "libnedclib": ["libnedclib.dll", "nedclib.dll"],
        "nedcenc": ["nedcenc.exe"],
        "nevpk": ["nevpk.exe"],
    },
    "macos": {
        "libnedclib": ["libnedclib.dylib"],
        "nedcenc": ["nedcenc"],
        "nevpk": ["nevpk"],
    },
    "linux": {
        "libnedclib": ["libnedclib.so"],
        "nedcenc": ["nedcenc"],
        "nevpk": ["nevpk"],
    },
}

def get_machine():
    os_name = sys.platform
    machine = platform.machine().lower()

    # Normalize OS name
    if os_name.startswith("linux"):
        os_name = "linux"
    elif os_name == "darwin":
        os_name = "macos"
    elif os_name in ("win32", "cygwin", "msys"):
        os_name = "windows"

    # Normalize architecture
    if machine in ("amd64", "x86_64"):
        arch = "amd64"
    elif machine in ("aarch64", "arm64"):
        arch = "arm64"
    else:
        arch = machine

    return f"{os_name}-{arch}"


# validate platform os support
machine = get_machine()
plat = machine[:machine.index("-")]
platform_tools = _TOOLS.get(plat)
if not platform_tools:
    raise OSError(f"Piket currently does not support: {machine}")

# resolve tool paths and expose them
_TOOL_PATHS: dict[str, Path] = {}
for tool, filenames in platform_tools.items():
    for filename in filenames:
        try:
            with resources.path(f"piket.bin", filename) as p:
                if Path(p).exists():
                    _TOOL_PATHS[tool] = p
        except Exception as e:
            raise ImportError(f"Error loading binary '{filename}': {e}")
    if tool not in _TOOL_PATHS:
        raise FileNotFoundError(f"Missing required tool: {tool}")

NEDCENC = _TOOL_PATHS["nedcenc"]
NEVPK = _TOOL_PATHS["nevpk"]

# expose functions
from .util import decode, encode, get_id
from .card import Card
from . import connecting_pikmin as ConnectingPikmin
from . import plucking_pikmin as PluckingPikmin
from . import marching_pikmin as MarchingPikmin

__all__ = [
    "NEDCENC", "NEVPK", # tools
    "decode", "encode", "get_id", # direct methods
    "ConnectingPikmin", "PluckingPikmin", "MarchingPikmin", # classes
]
