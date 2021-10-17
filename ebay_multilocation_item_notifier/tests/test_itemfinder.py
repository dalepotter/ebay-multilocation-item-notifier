import ebaysdk
from ebay_multilocation_item_notifier.itemfinder import get_results_dict


def test_get_results_api_receives_expected_payload(mocker, mock_response_three_items):
    """The ebay API must receive expected input params (could paramaterise for two connections)."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items
    mock_search_keywords = [
        ['search keyword 1', [
            {'name': 'MaxPrice', 'value': 25}
        ]]
    ]
    mock_search_locations = [
        ['location 1', 'AB1 2CD', 20],
        ['location 2', 'EF3 5GH'],
        ['location 3', 'IJ6 7KL', 10]
    ]
    expected_calls = [
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'MaxPrice', 'value': 25},
                    {'name': 'MaxDistance', 'value': '20'},  # Value for location 1
                    {'name': 'LocalPickupOnly', 'value': True}
                ],
                'buyerPostalCode': 'AB1 2CD',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'MaxPrice', 'value': 25},
                    {'name': 'MaxDistance', 'value': '10'},  # No value set for location 2, so use default value
                    {'name': 'LocalPickupOnly', 'value': True}
                ],
                'buyerPostalCode': 'EF3 5GH',
            }
        ),
        mocker.call(
            'findItemsAdvanced', {
                'keywords': 'search keyword 1',
                'itemFilter': [
                    {'name': 'MaxPrice', 'value': 25},
                    {'name': 'MaxDistance', 'value': '10'},  # Value for location 3
                    {'name': 'LocalPickupOnly', 'value': True}
                ],
                'buyerPostalCode': 'IJ6 7KL',
            }
        )
    ]

    get_results_dict(mock_search_keywords, mock_search_locations)

    assert ebaysdk.finding.Connection.execute.call_count == 3
    ebaysdk.finding.Connection.execute.assert_has_calls(expected_calls)


def test_get_results_empty_input_returns_empty_dict(mocker, mock_response_three_items):
    """`get_results_dict` with no data must return an empty dictionary."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items

    result = get_results_dict([], [])

    assert isinstance(result, dict)
    assert result == {}


def test_get_results_with_input_returns_nested_dict(mocker, mock_response_three_items):
    """`get_results_dict` with mocked data must return a nested dictionary with the input search keyword as a parent of the input location."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items

    result = get_results_dict(
                [['search keyword 1']],
                [['location 1', 'PL4 6AB', 20]]
    )

    assert 'search keyword 1' in result.keys()
    assert 'location 1' in result['search keyword 1'].keys()
    assert isinstance(result['search keyword 1']['location 1'], ebaysdk.response.ResponseDataObject)
    assert result['search keyword 1']['location 1']._count == '3'
    assert len(result['search keyword 1']['location 1'].item) == 3
