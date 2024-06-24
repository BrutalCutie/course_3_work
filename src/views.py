import json
import os
from collections import defaultdict
from typing import Literal
import datetime
from config import OP_DATA_DIR, LOGS_DIR
from src.utils import read_file_data

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_handler = logging.FileHandler(str(os.path.join(LOGS_DIR, "views.log")), mode='w', encoding='utf8')
logger_formatter = logging.Formatter("%(name)s - %(funcName)s: %(message)s")
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)


def get_operations_by_date_range(date: str, optional_flag: Literal["M", "W", "Y", "ALL"] = "M") -> list[dict]:

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
        op_date = datetime.datetime.strptime(op["Дата операции"], "%d.%m.%Y %H:%M:%S")

        if start_date < op_date < last_date.replace(day=last_date.day+1):
            tmp.append(op)

    return tmp


def get_expences_and_income(transactions_data):
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

    for op in transactions_data:
        op_sum = op['Сумма операции']
        op_category = op['Категория']
        op_state = op['Статус']

        if op_state == 'FAILED':
            continue

        if op_sum < 0:
            expences_categories[op_category] += abs(op_sum)
        else:
            income_categories[op_category] += abs(op_sum)

    for op in dict(expences_categories).items():
        logger.debug(op)
        op_category, op_amount = op
        expences['total_amount'] += op_amount

        expences['main'].append({'category': op_category, 'amount': round(op_amount, 2)})

    for op in dict(income_categories).items():
        logger.debug(op)
        op_category, op_amount = op
        income['total_amount'] += op_amount

        income['main'].append({'category': op_category, 'amount': round(op_amount, 2)})

    return {
        'expences': expences,
        "income": income
    }


def post_json_response():
    pass


if __name__ == '__main__':
    result = get_operations_by_date_range("10.01.2018")
    with open('op.json', 'w', encoding='utf8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    result2 = get_expences_and_income(result)
    with open('result.json', 'w', encoding='utf8') as file:
        json.dump(result2, file, ensure_ascii=False, indent=4)
