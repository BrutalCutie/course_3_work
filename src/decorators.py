import os
import pandas as pd

from config import DATA_DIR


class ReportSaver:

    @staticmethod
    def to_excel(file_name: str = 'result_{func}.xls'):

        def wrapper(func):

            def inner(*args, **kwargs) -> pd.DataFrame:

                result: pd.DataFrame = func(*args, **kwargs)

                result.to_excel(f"{os.path.join(DATA_DIR, file_name.format(func=func.__name__))}",
                                index=False,
                                engine="openpyxl")

                return result

            return inner

        return wrapper
