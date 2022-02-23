import ebaysdk
import pytest
import ebay_multilocation_item_notifier.tests.conftest as conftest
from ebay_multilocation_item_notifier.keyword_search import KeywordSearch


def test_find_items_returns_dict(mock_kw_search):
    """The `KeywordSearch.find_items` method must return the expected number of items."""
    result = mock_kw_search.find_items()

    assert len(result) == 3


def test_find_items_payload_default_item_filters(mocker, mock_kw_search):
    """A `KeywordSearch` object with default item filters must generate the expected API payload."""
    mock_kw_search.search_locations = [
        ['location 1', 'AB1 2CD', 30],
        ['location 2', 'EF3 5GH'],
        ['location 3', 'IJ6 7KL', 20]
    ]
    expected_calls = [
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'LocalPickupOnly', 'value': True},
                    {'name': 'MaxDistance', 'value': '30'},  # Custom value for location 1
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'}
                ],
                'buyerPostalCode': 'AB1 2CD',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'LocalPickupOnly', 'value': True},
                    {'name': 'MaxDistance', 'value': '5'},  # No value set for location 2, so use default value
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'}
                ],
                'buyerPostalCode': 'EF3 5GH',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'LocalPickupOnly', 'value': True},
                    {'name': 'MaxDistance', 'value': '20'},  # Custom value for location 3
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'}
                ],
                'buyerPostalCode': 'IJ6 7KL',
            }
        )
    ]

    mock_kw_search.find_items()

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)


def test_find_items_payload_with_custom_item_filters(mocker, MockKwSearch):
    """A `KeywordSearch` object with custom item filters must generate the expected API payload."""
    class MockKeywordSearchCustomFilters(MockKwSearch):
        search_filters = {
            'LocalPickupOnly': False,  # Overwrites key/value set in MockKeywordSearch
            'MaxPrice': 25  # Adds new key/value not set in MockKeywordSearch
        }

    expected_calls = [
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxDistance', 'value': '20'},  # `MockKwSearch` sets custom value for location 1
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxPrice', 'value': 25}
                ],
                'buyerPostalCode': 'AB1 2CD',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxDistance', 'value': '5'},  # No custom value set for location 2, so use default value
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxPrice', 'value': 25}
                ],
                'buyerPostalCode': 'EF3 5GH',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxDistance', 'value': '10'},  # MockKwSearch` sets custom value for location 3
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxPrice', 'value': 25}
                ],
                'buyerPostalCode': 'IJ6 7KL',
            }
        )
    ]

    _ = MockKeywordSearchCustomFilters().find_items()

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)


def test_find_items_largest_max_distance(mocker, mock_kw_search):
    """A `KeywordSearch` object with location search radiuses disabled must generate the expected API payload."""
    mock_kw_search.location_radius_overrides_default_search_radius = False
    mock_kw_search.search_filters = {'MaxDistance': '10'}
    mock_kw_search.search_locations = [
        ['location 1', 'AB1 2CD', 30],
        ['location 2', 'EF3 5GH'],
        ['location 3', 'IJ6 7KL', 20]
    ]
    expected_calls = [
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'MaxDistance', 'value': '10'},  # `mock_kw_search` overrides custom value for location 1
                ],
                'buyerPostalCode': 'AB1 2CD',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'MaxDistance', 'value': '10'},  # mock_kw_search` uses default search radius anyway
                ],
                'buyerPostalCode': 'EF3 5GH',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'MaxDistance', 'value': '10'},  # mock_kw_search` overrides custom value for location 3
                ],
                'buyerPostalCode': 'IJ6 7KL',
            }
        )
    ]

    _ = mock_kw_search.find_items()

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)


def test_generate_item_filter_list_structure(mock_kw_search):
    """An item filter list must be returned with the expected structure."""
    mock_kw_search.search_filters = {
        'Condition': 'Used',
        'ListingType': 'Auction',
        'MaxDistance': 10,
        'LocalPickupOnly': True
    }

    result = mock_kw_search.generate_item_filter_list()

    assert result == [
        {'name': 'Condition', 'value': 'Used'},
        {'name': 'ListingType', 'value': 'Auction'},
        {'name': 'MaxDistance', 'value': 10},
        {'name': 'LocalPickupOnly', 'value': True},
    ]


@pytest.mark.parametrize('child_search_filters', [
    {'Condition': 'Used'},  # Key not in parent dict
    {'LocalPickupOnly': False},  # Overwriting key/value in parent dict
])
def test_search_filters_merged_keys(child_search_filters):
    """An item filter list must be returned containing key/value pairs from parent classes."""
    class ChildKeywordSearch(KeywordSearch):
        search_filters = child_search_filters
    parent_kw_search = KeywordSearch()  # KeywordSearch defines `search_filters = {'LocalPickupOnly': True}`
    child_kw_search = ChildKeywordSearch()

    result = child_kw_search.search_filters

    assert child_search_filters.items() <= result.items()  # All child search filters must be present in the result
    assert 'LocalPickupOnly' in result.keys()  # Parent `search_filters` key must be inherited (regardless of child `search_filters` defintion)
    assert parent_kw_search.search_filters == {'LocalPickupOnly': True, 'MaxDistance': '5'}  # Original keys/values must remain in parent


@pytest.mark.parametrize('mock_cached_results', [
    {},
    {
        'location 1': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult,
        'location 2': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult,
        'location 3': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult
    }
])
def test_results_no_cache_calls_find_items(mocker, mock_kw_search, mock_cached_results):
    """A `KeywordSearch` object with no cached results calls find_items."""
    mock_kw_search.cached_results = mock_cached_results
    spy = mocker.spy(conftest.MockKeywordSearch, 'find_items')

    result = mock_kw_search.results

    assert spy.called is not bool(mock_cached_results)  # Method must be called when there is no cached data, and vice versa
    assert result
    assert result['location 1']
    assert result['location 2']
    assert result['location 3']
    assert all(
        [isinstance(location_result, ebaysdk.response.ResponseDataObject) for location_result in result.values()]
    )

def test_results_removes_duplicates_items_found(mock_kw_search):
    """Duplicate item results must be removed when present in results at muliple locations."""
    mock_kw_search.remove_duplicates = True
    mock_kw_search.cached_results = {
        'location 1': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_ZERO_ITEMS).reply.searchResult,
        'location 2': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult,
        'location 3': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult
    }

    result = mock_kw_search.results

    assert len(getattr(result['location 1'], 'item', list())) == 0  # location 3 was mocked to contain zero items
    assert len(getattr(result['location 2'], 'item', list())) == 3
    assert len(getattr(result['location 3'], 'item', list())) == 0  # location 3 was mocked to contain same items as location 2, so remove all
