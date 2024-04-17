import logging
from logging import Logger
from typing import List

from typeguard import typechecked

# from example_python_package.factories import GenericFactory

logger: Logger = logging.getLogger(__name__)


class Multiplier:
    """A class that performs multiplication on a list of numbers."""

    @typechecked
    def __init__(self) -> None:
        """Initialiser method."""

        pass  # pragma: no cover

    @typechecked
    def multiply(
        self,
        numbers: List[int],
    ) -> int:
        """Main method - multiples a list of numbers and returns the result.

        Args:
            numbers (List[int]): a list of integers to be multiplied.


        Returns:
            int: a number as a result of multiplying all input integers.
        """

        logger.info("Multiplying input integers.")

        if not numbers:
            logger.warning("No integers passed in - skipping multiplying.")
            return 0

        result: int = 1

        for number in numbers:
            result *= number

        logger.info("Successfully multiplied input integers.")

        return result
