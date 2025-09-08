import functools
from datetime import datetime


def log(filename=None):
    """Декоратор для логирования вызовов функций, их результатов и ошибок.

        Логирует начало и конец выполнения функции, а также возникшие ошибки.
        Результаты могут записываться в файл или выводиться в консоль.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Обёртка для логирования вызова функции."""
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                result = func(*args, **kwargs)

                log_message = f"{timestamp} - {func_name} ok. Result: {result}\n"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                return result

            except Exception as e:
                error_message = f"{timestamp} - {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(error_message)
                else:
                    print(error_message, end='')

                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)
