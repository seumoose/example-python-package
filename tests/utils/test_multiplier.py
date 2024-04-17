from example_python_package.utils import Multiplier


def test_multiplier_returns_multiplied_numbers():
    expected = 12 * 6 * 8

    actual = Multiplier().multiply([6, 12, 8])

    assert expected == actual


def test_multiplier_skips_with_no_input(caplog):
    Multiplier().multiply([])

    assert "No integers passed in - skipping multiplying." in caplog.text
