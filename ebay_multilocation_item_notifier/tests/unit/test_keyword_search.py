import ebaysdk
import pytest
import ebay_multilocation_item_notifier.tests.conftest as conftest


def test_find_items_returns_dict(mock_kw_search):
    """The `KeywordSearch.find_items` method must return the expected number of items."""
    result = mock_kw_search.find_items()

    assert len(result) == 3


def test_find_items_payload_default_item_filters(mocker, mock_kw_search):
    """An item object with default item filters must generate the expected API payload."""
    expected_calls = [
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxDistance', 'value': '20'},  # Custom value for location 1
                    {'name': 'LocalPickupOnly', 'value': True}
                ],
                'buyerPostalCode': 'AB1 2CD',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxDistance', 'value': '5'},  # No value set for location 2, so use default value
                    {'name': 'LocalPickupOnly', 'value': True}
                ],
                'buyerPostalCode': 'EF3 5GH',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxDistance', 'value': '10'},  # Custom value for location 3
                    {'name': 'LocalPickupOnly', 'value': True}
                ],
                'buyerPostalCode': 'IJ6 7KL',
            }
        )
    ]

    mock_kw_search.find_items()

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)


def test_find_items_payload_with_custom_item_filters(mocker, mock_kw_search):
    """An item object with custom item filters must generate the expected API payload."""
    mock_kw_search.search_filters = {
        'MaxPrice': 25,
        'LocalPickupOnly': False
    }
    expected_calls = [
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxDistance', 'value': '20'},  # Custom value for location 1
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxPrice', 'value': 25}
                ],
                'buyerPostalCode': 'AB1 2CD',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxDistance', 'value': '5'},  # No value set for location 2, so use default value
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxPrice', 'value': 25}
                ],
                'buyerPostalCode': 'EF3 5GH',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'ListingType', 'value': 'Auction'},
                    {'name': 'MaxDistance', 'value': '10'},  # Custom value for location 3
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxPrice', 'value': 25}
                ],
                'buyerPostalCode': 'IJ6 7KL',
            }
        )
    ]

    mock_kw_search.find_items()

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)


def test_generate_item_filter_list_default(mock_kw_search):
    """The default item filters must be returned when no arguments are passed."""
    result = mock_kw_search.generate_item_filter_list()

    assert result == [
        {'name': 'Condition', 'value': 'Used'},
        {'name': 'ListingType', 'value': 'Auction'},
        {'name': 'MaxDistance', 'value': '5'},
        {'name': 'LocalPickupOnly', 'value': True},
    ]


def test_generate_item_filter_list_explicit_default(mock_kw_search):
    """Defaults passed as an argument must override the package defaults."""
    mock_default_item_filter = {'MaxPrice': 10}

    result = mock_kw_search.generate_item_filter_list(
        default_item_filters=mock_default_item_filter
    )

    assert result == [
        {'name': 'MaxPrice', 'value': 10}
    ]


def test_generate_item_filter_list_no_conflicts(mock_kw_search):
    """A custom item filter list (with no conflicting item filter names) must be merged into the default list as expected."""
    mock_default_item_filter = {'MaxPrice': 10}
    custom_item_filters_non_conflicting = {'Condition': 'Used'}

    result = mock_kw_search.generate_item_filter_list(
        custom_item_filters_non_conflicting,
        mock_default_item_filter
    )

    assert result == [
        {'name': 'MaxPrice', 'value': 10},
        {'name': 'Condition', 'value': 'Used'}
    ]


def test_generate_item_filter_list_with_conflicts(mock_kw_search):
    """A custom item filter list (with a conflicting item filter name) must be merged into the default list as expected."""
    mock_default_item_filter = {'MaxPrice': 5}
    custom_item_filters_conflicting_name = {'MaxPrice': 10}

    result = mock_kw_search.generate_item_filter_list(
        custom_item_filters_conflicting_name,
        mock_default_item_filter
    )

    assert result == [
        {'name': 'MaxPrice', 'value': 10}
    ]


def test_generate_item_filter_list_independence(mock_kw_search):
    """Repeated calls to generate an item filter list must be independent from previous calls."""
    mock_default_item_filter = {
        'MaxPrice': 5
    }
    custom_item_filters_itererable = [
        {'Condition': 'Used'},
        {'ListingType': 'Auction'}
    ]

    for custom_item_filter in custom_item_filters_itererable:
        result = mock_kw_search.generate_item_filter_list(
            custom_item_filter,
            mock_default_item_filter
        )

    assert result == [
        {'name': 'MaxPrice', 'value': 5},
        {'name': 'ListingType', 'value': 'Auction'}
    ]


@pytest.mark.parametrize('mock_cached_results', [
    {},
    {
        'location 1': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult,
        'location 2': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult,
        'location 3': conftest.generate_mock_response(conftest.MOCK_SEARCH_RESULT_THREE_ITEMS).reply.searchResult
    }
])
def test_results_no_cache_calls_find_items(mocker, mock_kw_search, mock_cached_results):
    """An item object with no cached results calls find_items."""
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
