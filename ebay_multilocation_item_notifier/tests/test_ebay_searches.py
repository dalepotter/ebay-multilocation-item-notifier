import pytest
from ebay_multilocation_item_notifier.ebay_searches import EbaySearches


@pytest.mark.parametrize("number_of_mock_searches", [0, 1, 10, 5])  # Unordered to test a new object overwrites existing searches
def test_search_added_to_list(mock_search, number_of_mock_searches):
    list_of_mock_searches = [mock_search] * number_of_mock_searches

    searches = EbaySearches(*list_of_mock_searches)

    assert len(searches.search_list) == number_of_mock_searches
