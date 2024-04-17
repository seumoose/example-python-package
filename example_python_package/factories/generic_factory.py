import logging
from logging import Logger
from types import BuiltinFunctionType, FunctionType, MethodType
from typing import Any, Callable, Dict, Generic, List, TypeVar

from pytypes import get_orig_class
from typeguard import typechecked

logger: Logger = logging.getLogger(__name__)

K = TypeVar("K")
V = TypeVar("V")


@typechecked
class GenericFactory(Generic[K, V]):
    """Generic factory that produces instances of type <V> for a given key of type <K>."""

    @typechecked
    def __init__(
        self,
        mapping: Dict[K, V],
    ) -> None:
        """Initialiser method. Creates and stores an internal mapping of supplied key
            value pairs of types <K> and <V> respectively allowing the values to be
            created programmatically. Mapping values are checked to be an instance or
            subclass of type <V>.

            Class signature is as follows:
            <variable> = GenericFactory[<K>, <V>](<dictionary mapping>)

        Args:
            mapping (Dict[K, V]): a dictionary mapping keys of type<K> to values of type<V>.
        """

        # get types from internal Python API (they're not directly exposed...)
        self.k_type, self.v_type = get_orig_class(self).__args__  # type: ignore[no-untyped-call]

        self.__check_keys(list(mapping.keys()))
        self.__check_values(mapping)

        self.__mapping: Dict[K, V] = mapping

    def __check_keys(self, keys: List[K]) -> None:
        """Checks all mapping dictionary keys for correct typing.

        Args:
            keys (List[K]): the list of keys to be checked.

        Raises:
            TypeError: if the key type is incorrect to the specified generic type.
        """

        for key in keys:
            if not isinstance(key, self.k_type):
                expected_name: str = getattr(self.k_type, "__name__", repr(self.k_type))
                actual_name: str = getattr(type(key), "__name__", repr(type(key)))
                error_message: str = f"Type of keys of argument mapping must be {expected_name}; got {actual_name} instead."

                raise TypeError(error_message)

    def __check_values(self, mapping: Dict[K, V]) -> None:
        """Checks the all the mapping values for correct typing.

        Args:
            mapping (Dict[K, V]): the dictionary mapping of types <K> and <V>.

        Raises:
            TypeError: if the value type is incorrect to the specified generic type.
        """

        for key in mapping.keys():
            # check if the value is of the same type or is a subclass of the return type
            if not isinstance(mapping[key], self.v_type) and not (
                isinstance(mapping[key], Callable)  # type: ignore[arg-type]
                and issubclass(mapping[key], self.v_type)  # type: ignore[arg-type]
            ):
                expected_name: str = getattr(self.v_type, "__name__", repr(self.v_type))
                actual_name: str = getattr(
                    type(mapping[key]), "__name__", repr(type(mapping[key]))
                )
                error_message: str = f"Type of argument \"mapping\"['{key}'] must be {expected_name}; got {actual_name} instead."

                raise TypeError(error_message)

    @typechecked
    def create(self, input_key: K, *args: Any, **kwargs: Any) -> V:
        """Obtains an instance of type<V> based on the key mapping passed in.

        Args:
            input_key (K): the key to map to a type<V> reference.

        Raises:
            TypeError: if the key type is incorrect to the specified generic type.
            ValueError: if there is no applicable mapping within the factory.
            TypeError: if the return type of the factory is incorrect to the specified
                generic type.

        Returns:
            V: an instance of type<V>.
        """

        expected_name: str = ""
        actual_name: str = ""
        error_message: str = ""

        # validate generic input type - typechecked doesn't validate generics
        if not isinstance(input_key, self.k_type):
            expected_name = getattr(self.k_type, "__name__", repr(self.k_type))
            actual_name = getattr(type(input_key), "__name__", repr(type(input_key)))
            error_message = f'Type of argument "input_key" must be {expected_name}; got {actual_name} instead.'

            raise TypeError(error_message)

        if input_key not in self.__mapping:
            error_message = f"Could not find an applicable mapping for key {input_key}."
            logger.error(error_message)
            raise ValueError(error_message)

        logger.info(f"Found mapping for {input_key}.")

        return_value: V = self.__get_return_value(input_key, *args, **kwargs)

        # validate generic return type
        if not isinstance(return_value, self.v_type):
            expected_name = getattr(self.v_type, "__name__", repr(self.v_type))
            actual_name = getattr(
                type(return_value), "__name__", repr(type(return_value))
            )
            error_message = f"Type of the return value must be {expected_name}; got {actual_name} instead."

            raise TypeError(error_message)

        return return_value  # type: ignore[no-any-return]

    def __get_return_value(self, input_key: K, *args: Any, **kwargs: Any) -> V:
        """Helper method to return appropriate types depending on the

        Args:
            input_key (K): the key to map to a type<V> reference.

        Returns:
            V: a instance of type<V> with optional params applied to it (for class
            instances).
        """

        # 'primitive' types (which are all instances of class type) don't have the
        # __dict__ attribute - also need to check the item is not a function / method
        if hasattr(self.__mapping[input_key], "__dict__") and not isinstance(
            self.__mapping[input_key], (BuiltinFunctionType, FunctionType, MethodType)
        ):
            # return initialised class with options passed in
            return self.__mapping[input_key](*args, **kwargs)  # type: ignore[no-any-return,operator]

        # return reference to V<type>
        return self.__mapping[input_key]
