from src.views import (get_income_categories,
                       get_expences_income,
                       get_currency_stocks,
                       get_expences_categories,
                       get_operations_by_date_range,
                       post_events_response)


def test_post_events_response(post_events_response_result):
    assert post_events_response('01.10.2018', "W") == post_events_response_result


def test_get_income_categories():
    incomes = {
        'Зарплата': 1000,
        "Подарок": 2000
    }

    assert get_income_categories(incomes) == {
        'total_amount': 3000,
        'main': [{'category': 'Подарок', 'amount': 2000},
                 {'category': 'Зарплата', 'amount': 1000}]
    }


def test_get_expences_income(operations_m, expenses_income_results):
    assert get_expences_income(operations_m) == expenses_income_results
    assert get_expences_income([{
        "Сумма платежа": 100,
        "Категория": "Пополнение"
    }]) == ({
        "total_amount": 0,
        "main": [],
        "transfers_and_cash": []
    }, {
        'total_amount': 100,
        "main": [{'category': "Пополнение", 'amount': 100}]
    })


def test_get_currency_stocks(cur_stocks_result):
    assert get_currency_stocks() == cur_stocks_result


def test_get_expences_categories():
    expences = {
        'Топливо': 1000,
        "Супермаркет": 2000,
        "Наличные": 3000,
        "Красота": 4000,
        "Развлечение": 5000,
        "Одежда": 6000,
        "Фастфуд": 7000,
        "Благотворительность": 8000,
        "Ремонт": 9000,
    }

    assert get_expences_categories(expences) == {
        'total_amount': 45000,
        'main': [
            {'category': 'Ремонт', 'amount': 9000},
            {'category': 'Благотворительность', 'amount': 8000},
            {'category': 'Фастфуд', 'amount': 7000},
            {'category': 'Одежда', 'amount': 6000},
            {'category': 'Развлечение', 'amount': 5000},
            {'category': 'Красота', 'amount': 4000},
            {'category': 'Супермаркет', 'amount': 2000},
            {'category': 'Остальное', 'amount': 1000}],
        'transfers_and_cash': [{'category': 'Наличные', 'amount': 3000}]
    }


def test_get_operations_by_date_range(operations_m, operations_w, operations_all):
    assert get_operations_by_date_range('01.10.2018') == operations_m
    assert get_operations_by_date_range('01.10.2018', 'W') == operations_w
    assert get_operations_by_date_range('01.02.2018', 'ALL') == operations_all
    assert get_operations_by_date_range('01.02.2018', 'Y') == operations_all

