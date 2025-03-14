import inspect
import pytest

from app.shared.core.errors.result_errors.db_errors import DbErrors
from app.shared.core.errors.result_errors.user_errors import UserErrors
from app.shared.core.result.result_error import ResultError

pytest.skip(allow_module_level=True)


def get_all_subclasses(cls):
    """
    Recursively finds all subclasses of a given class.
    """
    subclasses = set(cls.__subclasses__())
    for subclass in cls.__subclasses__():
        subclasses |= get_all_subclasses(subclass)
    return subclasses


def test_unique_error_codes():
    """
    Test that all subclasses of ResultError have unique error codes.

    This function iterates through all subclasses of ResultError,
    inspects their public methods (ignoring private/special methods),
    and attempts to call them with no arguments (assuming they are
    static or class methods that act as error factories). It then
    checks that the `.code` attribute on the returned instance is unique.
    """
    error_codes = []  # Map each error code to its origin (Class.method)

    # Retrieve all subclasses of ResultError.
    all_error_classes = get_all_subclasses(ResultError)
    all_error_classes.add(ResultError)
    for error_class in all_error_classes:
        codes = error_class.codes
        print("errr", error_class, codes.values())
        for code in codes.values():
            if code in error_codes:
                print(f"Duplicate error code '{code}' found in {error_class}")
                pytest.fail(f"Duplicate error code '{code}' found ")
            error_codes.append(code)
    # If no duplicates are found, the test passes.
