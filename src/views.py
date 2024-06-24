import json
import os
from collections import defaultdict
from typing import Literal
import datetime
from config import OP_DATA_DIR, LOGS_DIR, USER_SETTINGS
from src.utils import read_file_data

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler(str(os.path.join(LOGS_DIR, "views.log")), mode='w', encoding='utf8')
logger_formatter = logging.Formatter("%(name)s - %(funcName)s: %(message)s")
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)


def get_operations_by_date_range(date: str, optional_flag: str = "M") -> list[dict]:

    last_date = datetime.datetime.strptime(date, "%d.%m.%Y")

    start_date = last_date.replace(day=1)

    if optional_flag == "W":
        days_between = last_date.day - last_date.weekday()
        start_date = last_date.replace(day=days_between)
    elif optional_flag == 'Y':
        start_date = last_date.replace(day=1, month=1)
    elif optional_flag == 'ALL':
        start_date = last_date.replace(day=1, month=1, year=1)

    op_data = read_file_data(OP_DATA_DIR)
    tmp = []

    for op in op_data:
        if op['Статус'] != "OK":
            continue

        op_date = datetime.datetime.strptime(op["Дата операции"], "%d.%m.%Y %H:%M:%S")

        if start_date < op_date < last_date.replace(day=last_date.day+1):
            tmp.append(op)

    return tmp


def post_events_response(date: str, optional_flag: Literal["M", "W", "Y", "ALL"] = "M") -> dict:

    f_by_date_operations = get_operations_by_date_range(date, optional_flag)
    expences, income = get_expences_income(f_by_date_operations)

    currency_rates, stocks_prices = get_currency_stocks(USER_SETTINGS)

    return {
        'expences': expences,
        "income": income,
        "currency_rates": currency_rates,
        "stock_prices": stocks_prices
    }


def get_expences_income(operations: list[dict]) -> tuple[dict, dict]:

    expences = {
        'total_amount': 0,
        "main": [],
        "transfers_and_cash": []
    }

    income = {
        'total_amount': 0,
        "main": []
    }
    expences_categories = defaultdict(int)
    income_categories = defaultdict(int)

    for op in operations:
        op_sum = op['Сумма платежа']
        op_category = op['Категория']

        if op_sum < 0:
            expences_categories[op_category] += abs(op_sum)
        else:
            income_categories[op_category] += abs(op_sum)

    for op in dict(expences_categories).items():
        logger.debug(op)
        op_category, op_amount = op
        expences['total_amount'] += op_amount

        if op_category in ['Переводы', "Наличные"]:
            expences['transfers_and_cash'].append({'category': op_category, 'amount': round(op_amount)})
        else:
            expences['main'].append({'category': op_category, 'amount': round(op_amount)})

    for op in dict(income_categories).items():
        logger.debug(op)
        op_category, op_amount = op
        income['total_amount'] += op_amount

        income['main'].append({'category': op_category, 'amount': round(op_amount)})
    # TODO максимум категорий = 7. Самые дорогие. Далее "остальное"
    return expences, income


def get_currency_stocks(file_path: str) -> tuple[list, list]:

    with open(file_path, 'r', encoding='utf8') as user_file:
        user_settings = json.load(user_file)

    user_currencies = user_settings['user_currencies']
    user_stocks = user_settings['user_stocks']
    mock = 99.42  # TODO заменить затычку на данные с API
    currency_list = []
    stocks_list = []
    for cur in user_currencies:
        currency_list.append({"currency": cur, "rate": mock})

    for stock in user_stocks:
        stocks_list.append({'stock': stock, 'price': mock})

    return currency_list, user_stocks


if __name__ == '__main__':

    date = "10.02.2018"
    result = get_operations_by_date_range(date, "ALL")
    with open('op.json', 'w', encoding='utf8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    result2 = post_events_response(date, "ALL")
    with open('result.json', 'w', encoding='utf8') as file:
        json.dump(result2, file, ensure_ascii=False, indent=4)
