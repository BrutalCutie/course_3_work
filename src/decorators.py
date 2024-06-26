import os
from functools import wraps

import pandas as pd

from config import DATA_DIR


class ReportSaver:

    @staticmethod
    def to_excel(file_name: str = "result_{func}.xls"):
        """
        Декоратор для сохранения результатов в файл.
        :param file_name: Имя файла в которую будет сохранён результат. По умолчанию result_ИмяФункции.xls
        :return: Результат работы функции
        """

        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs) -> pd.DataFrame:

                result: pd.DataFrame = func(*args, **kwargs)

                result.to_excel(
                    f"{os.path.join(DATA_DIR, file_name.format(func=func.__name__))}", index=False, engine="openpyxl"
                )

                return result

            return inner

        return wrapper
