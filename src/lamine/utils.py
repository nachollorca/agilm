"""Contains utility clases and functions for the core modules."""

import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from typing import Any, Callable


def parallelize_function(function: Callable, params_list: list[dict[str, Any]], max_workers: int = 10) -> list[Any]:
    """
    Executes a batch of calls of a function with different parameters in parallel using threading.

    Args:
        function (Callable): The function to be executed for each set of parameters.
        params_list (List[Dict[str, Any]]): A list of dictionaries, where each dictionary contains
            the keyword arguments for one call to `func`.
        max_threads (int): The maximum number of threads to use in the thread pool.

    Returns:
        list[Any]: A list containing the results of each function call, in the same order as the input parameters.

    Examples:
        >>> def add(a, b):
        ...     return a + b

        >>> params_list = [
        ...     {"a": 1, "b": 2},
        ...     {"a": 10, "b": 20},
        ...     {"a": 100, "b": 200}
        ... ]

        >>> run_in_parallel(add, params_list)
        [3, 30, 300]
    """
    results = [None] * len(params_list)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures_to_indices = {executor.submit(function, **params): index for index, params in enumerate(params_list)}
        for future in as_completed(futures_to_indices):
            index = futures_to_indices[future]
            results[index] = future.result()
    return results


def parallelize_functions(
    function_and_params: list[tuple[Callable, dict[str, Any]]], max_workers: int = 10
) -> list[Any]:
    """
    Executes a batch of different functions in parallel.

    Args:
        function_and_params (list[tuple[Callable, dict[str, Any]]]): A list of tuples, where each tuple contains
            a Callable object (function), and a dictionary with the parameters for the function (keys are parameter names).
        max_workers (int): The maximum number of threads to use in the thread pool.

    Returns:
        list[Any]: A list containing the results of each function call, in the same order as the input functions and parameters.

    Examples:
        >>> def add(a, b):
        ...     return a + b

        >>> def multiply(x, y):
        ...     return x * y

        >>> function_and_params = [
        ...     (add, {"a": 1, "b": 2}),
        ...     (multiply, {"x": 10, "y": 20}),
        ...     (add, {"a": 100, "b": 200})
        ... ]

        >>> parallelize_functions(function_and_params)
        [3, 200, 300]
    """
    results = [None] * len(function_and_params)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures_to_indices = {
            executor.submit(func, **params): index for index, (func, params) in enumerate(function_and_params)
        }
        for future in as_completed(futures_to_indices):
            index = futures_to_indices[future]
            results[index] = future.result()
    return results


def parse_xml(tag: str, string: str, should_raise: bool) -> list[str]:
    """
    Parses and extracts content within specified XML tags from a given string.

    Args:
        tag (str): The name of the XML tag to match.
        string (str): The input string containing the XML content.

    Returns:
        list[str]: A list of strings containing the matched content. If no matches are found, an empty list is returned.
    """
    matches = re.findall(
        pattern=f"<{tag}>(.*?)</{tag}>",
        string=string,
        flags=re.DOTALL,
    )

    if len(matches) == 0:
        details = f"<{tag}> could not be matched"
        logging.warning(details)
        if should_raise:
            raise Exception(details)  # change with ParsingError
        return []

    return [match.strip() for match in matches]


def return_if_exception(func: Callable) -> Callable:
    """
    A decorator that runs a function with given arguments and returns
    any exception that occurs.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: A wrapped version of the input function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any | Exception:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return e

    return wrapper
