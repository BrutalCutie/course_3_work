import pandas as pd
import numpy as np


def read_file_data(file_path: str):
    """
    Функция для чтения excel файла и возвращения данных в виде списка словарей
    :param file_path: Путь до файла с данными
    :return: Данные в виде списка словарей
    """

    data = pd.read_excel(file_path).replace({np.nan: None})
    data_as_dict = data.to_dict('records')

    return data_as_dict
