from ebay_multilocation_item_finder.utils import generate_item_filter_list


def test_generate_item_filter_list_default():
    """The default item filters must be returned when no arguments are passed."""
    result = generate_item_filter_list()

    assert result == [
        {'name': 'Condition',
         'value': 'Used'},
        {'name': 'ListingType',
         'value': 'Auction'},
        {'name': 'MaxDistance',
         'value': '5'},
        {'name': 'LocalPickupOnly',
         'value': True},
    ]


def test_generate_item_filter_list_explicit_default():
    """Defaults passed as an argument must override the package defaults."""
    mock_default_item_filter = [
        {'name': 'MaxPrice',
         'value': 10}
    ]

    result = generate_item_filter_list(
        default_item_filters=mock_default_item_filter
    )

    assert result == [
        {'name': 'MaxPrice',
         'value': 10}
    ]


def test_generate_item_filter_list_no_conflicts():
    """A custom item filter list (with no conflicting item filter names) must be merged into the default list as expected."""
    mock_default_item_filter = [
        {'name': 'MaxPrice',
         'value': 10}
    ]
    custom_item_filters_non_conflicting = [
        {'name': 'Condition',
         'value': 'Used'}
    ]

    result = generate_item_filter_list(
        custom_item_filters_non_conflicting,
        mock_default_item_filter
    )

    assert result == [
        {'name': 'Condition',
         'value': 'Used'},
        {'name': 'MaxPrice',
         'value': 10}
    ]


def test_generate_item_filter_list_with_conflicts():
    """A custom item filter list (with a conflicting item filter name) must be merged into the default list as expected."""
    mock_default_item_filter = [
        {'name': 'MaxPrice',
         'value': 5}
    ]
    custom_item_filters_conflicting_name = [
        {'name': 'MaxPrice',
         'value': 10}
    ]

    result = generate_item_filter_list(
        custom_item_filters_conflicting_name,
        mock_default_item_filter
    )

    assert result == [
        {'name': 'MaxPrice',
         'value': 10}
    ]


def test_generate_item_filter_list_independence():
    """Repeated calls to generate an item filter list must be independent from previous calls."""
    mock_default_item_filter = [
        {'name': 'MaxPrice',
         'value': 5}
    ]
    custom_item_filters_itererable = [
        [
            {'name': 'Condition',
             'value': 'Used'}
        ],
        [
            {'name': 'ListingType',
             'value': 'Auction'}
        ]
    ]

    for custom_item_filter in custom_item_filters_itererable:
        result = generate_item_filter_list(
            custom_item_filter,
            mock_default_item_filter
        )

    assert result == [
        {'name': 'ListingType',
         'value': 'Auction'},
        {'name': 'MaxPrice',
         'value': 5}
    ]
