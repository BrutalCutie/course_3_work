from src.views import (get_income_categories,
                       get_expences_income,
                       get_currency_stocks,
                       get_expences_categories,
                       get_operations_by_date_range)


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


def test_get_expences_income():
    pass


def test_get_currency_stocks(cur_stocks_result):
    assert get_currency_stocks() == cur_stocks_result


def test_get_expences_categories():
    expences = {
        'Топливо': 1000,
        "Супермаркет": 2000,
        "Наличные": 3000
    }

    assert get_expences_categories(expences) == {
        'total_amount': 6000,
        'main': [{'category': 'Супермаркет', 'amount': 2000},
                 {'category': 'Топливо', 'amount': 1000}],
        'transfers_and_cash': [{'category': 'Наличные', 'amount': 3000}]
    }


def test_get_operations_by_date_range():
    pass
