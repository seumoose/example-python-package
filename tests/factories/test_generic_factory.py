import pytest

from example_python_package.factories import GenericFactory
from tests.factories.data import invalid_generic_factory, valid_generic_factory


def test_generic_factory_accepts_valid_maps_according_to_generic_typing():
    mapping = {
        "one": 1,
        "two": 2,
    }

    actual = GenericFactory[str, int](mapping)

    assert isinstance(actual, GenericFactory)


@pytest.mark.parametrize(
    "item",
    valid_generic_factory,
    ids=[item["description"] for item in valid_generic_factory],
)
def test_generic_factory_returns_expected_type_with_valid_key(item):
    types = item["generic_types"]

    # unable to unpack types into a generic definition
    class_instance = GenericFactory[types[0], types[1]](item["mapping"])

    actual = class_instance.create(
        item["key"], *item["arguments"], **item["keyword_arguments"]
    )

    assert isinstance(actual, item["expected_type"])


@pytest.mark.parametrize(
    "item",
    invalid_generic_factory,
    ids=[item["description"] for item in invalid_generic_factory],
)
def test_generic_factory_throws_expected_error_when_initialising(item):
    types = item["generic_types"]

    with pytest.raises(
        TypeError,
        match=item["exception"],
    ):
        # unable to unpack types into a generic definition
        GenericFactory[types[0], types[1]](item["mapping"])

        pytest.fail("Test should have failed.")


def test_generic_throws_expected_error_when_using_incorrect_input_key_type():
    mapping = {
        "one": 1,
        "two": 2,
    }

    with pytest.raises(
        TypeError,
        match='Type of argument "input_key" must be str; got int instead.',
    ):
        class_instance = GenericFactory[str, int](mapping)

        class_instance.create(1)
        pytest.fail("Test should have failed.")


def test_generic_throws_expected_error_with_no_available_mapping():
    with pytest.raises(
        ValueError,
        match="Could not find an applicable mapping for key one.",
    ):
        class_instance = GenericFactory[str, int]({})

        class_instance.create("one")
        pytest.fail("Test should have failed.")


def test_generic_factory_throws_expected_error_when_returning_invalid_value_according_to_generic_typing():
    mapping = {
        "one": 1,
        "two": 2,
    }

    with pytest.raises(
        TypeError,
        match="Type of the return value must be int; got str instead.",
    ):
        class_instance = GenericFactory[str, int](mapping)

        # get around name mangling
        class_instance._GenericFactory__mapping["two"] = "two"

        class_instance.create("two")
        pytest.fail("Test should have failed.")
