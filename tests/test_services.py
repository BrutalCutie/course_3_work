from src.services import search_by_persons, simple_searching


def test_simple_searching(cat_search_results):
    assert simple_searching("Райффайзенбанк") == cat_search_results


def test_search_by_persons(persons_search_result):
    assert search_by_persons()[:5] == persons_search_result
