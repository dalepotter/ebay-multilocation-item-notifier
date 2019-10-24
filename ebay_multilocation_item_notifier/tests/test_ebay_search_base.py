import ebaysdk
from ebay_multilocation_item_notifier.ebay_search_base import EbaySearchItemBase


class MockSearchItemBase(EbaySearchItemBase):
    search_keyword = "search keyword 1"
    search_filters = [
        {'name': 'Condition',
         'value': 'Used'},
        {'name': 'ListingType',
         'value': 'Auction'},
        # {'name': 'MaxDistance',
        #  'value': '5'},
        {'name': 'LocalPickupOnly',
         'value': True},
        # Params for searching for sold items:
        # {'name': 'SoldItemsOnly',
        #  'value': True}
    ]
    search_locations = [
        ['location 1', 'AB1 2CD', 20],
        ['location 2', 'EF3 5GH'],
        ['location 3', 'IJ6 7KL', 10]
    ]


class MockSearchItemBaseWithItemFilters(MockSearchItemBase):
    search_filters = [
        {'name': 'MaxPrice', 'value': 25},
        {'name': 'LocalPickupOnly', 'value': False}
    ]


def test_find_items_returns_dict(mocker, mock_response_three_items):
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items
    search = MockSearchItemBase()

    result = search.find_items()

    assert len(result) == 3


def test_find_items_payload_default_item_filters(mocker, mock_response_three_items):
    """An item object with default item filters must generate the expected API payload."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items
    search = MockSearchItemBase()
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

    search.find_items()

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)


def test_find_items_payload_with_custom_item_filters(mocker, mock_response_three_items):
    """An item object with custom item filters must generate the expected API payload."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items
    search = MockSearchItemBaseWithItemFilters()
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

    search.find_items()

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)
