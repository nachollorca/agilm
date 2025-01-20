"""Contains utility clases and functions."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from enum import Enum, EnumMeta
from typing import Any, Callable


@dataclass
class BaseDataclass:
    """Base class providing utility methods for other dataclasses."""

    @property
    def dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):  # type: ignore
        return cls(**data)

    @property
    def str(self) -> str:
        return ""


class BaseEnumMeta(EnumMeta):
    @property
    def values(cls):
        """Return a list of all the values in the enumeration."""
        return [member.value for member in cls]


class BaseEnum(Enum, metaclass=BaseEnumMeta):
    """Enum that can be made from a list of strings and can easily print all values."""

    @classmethod
    def from_list(cls, name: str, lst: list[str]):
        """Turns a list of string ids into an Enum."""
        enum_members = {model_id.upper().replace("-", "_").replace(".", "_"): model_id for model_id in lst}
        return cls(name, enum_members)  # type: ignore


def _run_batch(function: Callable, params_list: list[dict[str, Any]], max_workers: int = 10) -> list[Any]:
    """
    Executes a batch of calls of a function with different parameters in parallel using threading.

    Args:
        function (Callable): The function to be executed for each set of parameters.
        params_list (List[Dict[str, Any]]): A list of dictionaries, where each dictionary contains
            the keyword arguments for one call to `func`.
        max_threads (int): The maximum number of threads to use in the thread pool.

    Returns:
        List[Any]: A list containing the results of each function call, in the same order as the input parameters.
    """
    results = [None] * len(params_list)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures_to_indices = {executor.submit(function, **params): index for index, params in enumerate(params_list)}
        for future in as_completed(futures_to_indices):
            index = futures_to_indices[future]
            results[index] = future.result()
    return results
