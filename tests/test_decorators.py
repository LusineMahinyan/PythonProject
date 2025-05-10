import pytest

from decorators import log  # Импортируем декоратор из вашего файла


@pytest.fixture
def log_file(tmp_path):
    return tmp_path / "test_log.txt"


def test_log_to_console_success(capsys):
    @log()
    def add(a, b):
        return a + b

    add(2, 3)

    captured = capsys.readouterr()
    assert "add ok. Result: 5" in captured.out


def test_log_to_file_success(log_file):
    @log(filename=str(log_file))
    def multiply(a, b):
        return a * b

    multiply(3, 4)

    with open(log_file, "r") as f:
        log_content = f.read()
    assert "multiply ok. Result: 12" in log_content


def test_log_to_file_error(log_file):
    @log(filename=str(log_file))
    def fail() -> None:
        raise ValueError("Oops")

    with pytest.raises(ValueError):
        fail()

    with open(log_file, "r") as f:
        log_content = f.read()
    assert "fail error: ValueError" in log_content
    assert "Inputs: (), {}" in log_content


def test_preserves_function_metadata() -> None:
    @log()
    def original_func() -> None:
        """Тестовая функция."""
        pass

    assert original_func.__name__ == "original_func"
    assert original_func.__doc__ == "Тестовая функция."
