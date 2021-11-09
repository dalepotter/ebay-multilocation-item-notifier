import ebaysdk
import pytest
import ebay_multilocation_item_notifier.tests.conftest as conftest


def test_find_items_returns_dict(mock_kw_search):
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
                    {'name': 'LocalPickupOnly', 'value': True},
                    {'name': 'MaxDistance', 'value': '20'}  # Custom value for location 1
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
                    {'name': 'LocalPickupOnly', 'value': True},
                    {'name': 'MaxDistance', 'value': '5'}  # No value set for location 2, so use default value
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
                    {'name': 'LocalPickupOnly', 'value': True},
                    {'name': 'MaxDistance', 'value': '10'}  # Custom value for location 3
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
    mock_kw_search.search_filters = [
        {'name': 'MaxPrice', 'value': 25},
        {'name': 'LocalPickupOnly', 'value': False}
    ]
    expected_calls = [
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'MaxPrice', 'value': 25},
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxDistance', 'value': '20'},  # Custom value for location 1
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
                    {'name': 'MaxPrice', 'value': 25},
                    {'name': 'LocalPickupOnly', 'value': False},
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
                    {'name': 'MaxPrice', 'value': 25},
                    {'name': 'LocalPickupOnly', 'value': False},
                    {'name': 'MaxDistance', 'value': '10'},  # Custom value for location 3
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
