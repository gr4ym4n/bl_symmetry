
import typing
import sys

DEBUG = 'DEBUG_MODE' is sys.argv

SYMMETRY_AFIX_SEPARATORS = (".", " ", "-", "_")
SYMMETRY_AFIXES_LEFT: typing.Set[str] = {"l", "L", "left", "Left", "LEFT"}
SYMMETRY_AFIXES_RIGHT: typing.Set[str] = {"r", "R", "Right", "RIGHT"}
SYMMETRY_AFIXES: typing.Set[str] = SYMMETRY_AFIXES_LEFT | SYMMETRY_AFIXES_RIGHT

SYMMETRY_AFIX_PAIRS: typing.Tuple[typing.Tuple[str, str], ...] = (
    ("l", "r"),
    ("r", "l"),
    ("L", "R"),
    ("R", "L"),
    ("left", "right"),
    ("right", "left"),
    ("Left", "Right"),
    ("Right", "Left"),
    ("LEFT", "RIGHT"),
    ("RIGHT", "LEFT")
    )

SYMMETRY_SUFFIX_LUT: typing.Dict[str, str] = {
    f'{a}{sep}': f'{b}{sep}' for a, b in SYMMETRY_AFIX_PAIRS for sep in SYMMETRY_AFIX_SEPARATORS
    }

SYMMETRY_PREFIX_LUT: typing.Dict[str, str] = {
    f'{sep}{a}': f'{sep}{b}' for a, b in SYMMETRY_AFIX_PAIRS for sep in SYMMETRY_AFIX_SEPARATORS
    }

def is_symmetrical(name: str) -> bool:
    """
    Check whether a data block name is formatted as symmetrical.
    """
    if DEBUG:
        assert isinstance(name, str), (f'is_symmetrical(name): '
                                       f'Expected name to be str, not {name.__class__.__name__}')
    return any(map(name.endswith, SYMMETRY_PREFIX_LUT)) or any(map(name.startswith, SYMMETRY_SUFFIX_LUT))

def symmetrical_prefix(name: str) -> str:
    """
    Returns the prefix for a prefixed symmetrical data block name, 
    or an empty string if the data block name is not symmetrical.
    """
    if DEBUG:
        assert isinstance(name, str), (f'symmetrical_prefix(name): '
                                       f'Expected name to be str, not {name.__class__.__name__}')
    return next((afix for afix in SYMMETRY_SUFFIX_LUT if name.startswith(afix)), "")

def symmetrical_suffix(name: str) -> str:
    """
    Returns the suffix for a suffixed symmetrical data block name, 
    or an empty string if the data block name is not symmetrical.
    """
    if DEBUG:
        assert isinstance(name, str), (f'symmetrical_suffix(name): '
                                       f'Expected name to be str, not {name.__class__.__name__}')
    return next((afix for afix in SYMMETRY_PREFIX_LUT if name.endswith(afix)), "")

def symmatrical_afix(name: str) -> str:
    """
    Returns the afix for the symmetrical data block name,
    or an empty string if the data block is not symmetrical.
    """
    if DEBUG:
        assert isinstance(name, str), (f'symmetrical_afix(name): '
                                       f'Expected name to be str, not {name.__class__.__name__}')
    return symmetrical_suffix(name) or symmetrical_prefix(name)

def symmetrical_basename(name: str) -> str:
    """
    Returns the name of the data block removing the symmetrical afix
    """
    if DEBUG:
        assert isinstance(name, str), (f'symmetrical_basename(name): '
                                       f'Expected name to be str, not {name.__class__.__name__}')
    afix = symmetrical_suffix(name)
    if afix:
        return f'{name[:-len(afix)]}'
    afix = symmetrical_prefix(name)
    if afix:
        return f'{name[len(afix)]}'
    return ""

def symmetrical_split(name: str) -> typing.Tuple[str, str, str]:
    """
    Splits the data block name into its symmetrical prefix, base name and symmetrical suffix.
    """
    if DEBUG:
        assert isinstance(name, str), (f'symmetrical_split(name): '
                                       f'Expected name to be str, not {name.__class__.__name__}')
    afix = symmetrical_suffix(name)
    if afix:
        return "", name[:-len(afix)], afix
    afix = symmetrical_prefix(name)
    if afix:
        return afix, name[len(afix)], ""
    return "", name, ""

def symmetrical_target(name: str) -> str:
    """
    Returns the name of the symmetrical data block if the name is symmetrical,
    otherwise returns an emptpy string.
    """
    if DEBUG:
        assert isinstance(name, str), (f'symmetrical_target(name): '
                                       f'Expected name to be str, not {name.__class__.__name__}')
    afix = symmetrical_suffix(name)
    if afix:
        return f'{name[:-len(afix)]}{SYMMETRY_PREFIX_LUT[afix]}'
    afix = symmetrical_prefix(name)
    if afix:
        return f'{SYMMETRY_SUFFIX_LUT[afix]}{name[len(afix):]}'
    return ""
