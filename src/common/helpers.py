from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from typing import Callable
    from typing import Optional
    from typing import TypeVar

    T = TypeVar("T")

__all__ = (
    "from_list",
    "add_param",
)


def from_list(f: Callable[[Any], T], x: Any) -> list[T]:
    r"""Applies a function to all elements in a list.

    :param f: Function to apply on list elements
    :type f: Callable[[Any], T]
    :param x: List of objects
    :type x: Any
    :raises TypeError: If x is not a list
    :return: New list
    :rtype: list[T]
    """
    if not isinstance(x, list):
        raise TypeError("Wrong type received. Expected list.")
    return [f(y) for y in x]


def add_param(
    params: dict[str, Any],
    kwargs: dict[str, Any],
    key: str,
    param_name: Optional[str] = None,
    converter: Optional[Callable[[Any], T]] = None,
) -> bool:
    r"""Adds a parameter to a dictionary if it exists in kwargs.

    :param params: Dictionary to add parameter to
    :type params: dict[str, Any]
    :param kwargs: Dictionary to get parameter from
    :type kwargs: dict[str, Any]
    :param key: Key to get parameter from
    :type key: str
    :param param_name: Name of parameter to add to dictionary, defaults to None
    :type param_name: Optional[str]
    :param converter: Function to convert parameter, defaults to None
    :type converter: Optional[Callable[[Any], T]]
    :return: True if parameter was added, False otherwise
    :rtype: bool
    """
    if key in kwargs:
        value = kwargs[key]
        if converter:
            value = converter(value)
        params[param_name or key] = value
        return True
    return False
