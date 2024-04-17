from typing import Callable

from example_python_package import Multiplier
from tests.stubs.stub_class import StubClass

valid_generic_factory = [
    (
        {
            "description": "Primitive type",
            "generic_types": [str, int],
            "mapping": {
                "one": 1,
            },
            "key": "one",
            "arguments": [],
            "keyword_arguments": {},
            "expected_type": int,
        }
    ),
    (
        {
            "description": "Function type",
            "generic_types": [str, Callable],
            "mapping": {
                "add": lambda a, b: a + b,
            },
            "key": "add",
            "arguments": [],
            "keyword_arguments": {},
            "expected_type": Callable,
        }
    ),
    (
        {
            "description": "Class type",
            "generic_types": [str, Multiplier],
            "mapping": {
                "multiply": Multiplier,
            },
            "key": "multiply",
            "arguments": [],
            "keyword_arguments": {},
            "expected_type": Multiplier,
            "method_name": "multiply",
        }
    ),
    (
        {
            "description": "Class type - with arguments",
            "generic_types": [str, StubClass],
            "mapping": {
                "stub": StubClass,
            },
            "key": "stub",
            "arguments": [1, 2],
            "keyword_arguments": {},
            "expected_type": StubClass,
        }
    ),
    (
        {
            "description": "Class type - with keyword arguments",
            "generic_types": [str, StubClass],
            "mapping": {
                "stub": StubClass,
            },
            "key": "stub",
            "arguments": [],
            "keyword_arguments": {"parameter_1": 1, "parameter_2": 2},
            "expected_type": StubClass,
        }
    ),
]

invalid_generic_factory = [
    (
        {
            "description": "does_not_accept_invalid_mapping_keys_according_to_generic_typing",
            "exception": " of argument mapping must be str; got int instead.",
            "generic_types": [str, int],
            "mapping": {
                "one": 1,
                2: 2,
            },
        }
    ),
    (
        {
            "description": "does_not_accept_invalid_mapping_values_according_to_generic_typing",
            # note: due to pytest regex matching certain characters need to be doubly escaped in exception messages
            "exception": " \"mapping\"\\['two'\\] must be int; got str instead.",
            "generic_types": [str, int],
            "mapping": {
                "one": 1,
                "two": "two",
            },
        }
    ),
]
