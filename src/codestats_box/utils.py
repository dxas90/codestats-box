"""Utility functions for calculations and formatting."""

import math


def calculate_level(xp: int) -> int:
    """Calculate level from XP using Code::Stats formula.

    Formula: level = floor(0.025 * sqrt(xp))

    Args:
        xp: Total experience points

    Returns:
        Level calculated from XP
    """
    if xp < 0:
        return 0
    return math.floor(0.025 * math.sqrt(xp))


def format_xp_value(xp: int, level: int, new_xp: int | None = None) -> str:
    """Format XP value with level and optional recent XP.

    Args:
        xp: Total experience points
        level: User level
        new_xp: Recent XP gained (optional)

    Returns:
        Formatted string like "lvl  26 (1,104,152 XP)" or with recent XP
    """
    base = f"lvl {level:>3} ({xp:>9,} XP)"

    if new_xp is not None and new_xp > 0:
        return f"{base} (+{new_xp:>6,})"

    return base


def format_xp_only(xp: int) -> str:
    """Format XP value without level.

    Args:
        xp: Total experience points

    Returns:
        Formatted string like "1,104,152 XP"
    """
    return f"{xp:>9,} XP"
