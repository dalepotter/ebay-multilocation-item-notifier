from emails.template import JinjaTemplate


DEFAULT_ITEM_FILTER_LIST = [
    {'name': 'Condition',
     'value': 'Used'},
    {'name': 'ListingType',
     'value': 'Auction'},
    {'name': 'MaxDistance',
     'value': '5'},
    {'name': 'LocalPickupOnly',
     'value': True},
    # Params for searching for sold items:
    # {'name': 'SoldItemsOnly',
    #  'value': True}
]


def generate_item_filter_list(custom_item_filters=[], default_item_filters=DEFAULT_ITEM_FILTER_LIST):
    """Return a list of ebay API item filters. Merges the custom_item_filter into the default_item_filter list.
    Item filters within custom_item_filter always take priority if there are conflicts.

    Available item filters: https://developer.ebay.com/devzone/finding/CallRef/types/ItemFilterType.html

    Inputs:
        custom_item_filters (list (of dicts)) -- List of item filter dicts to be joined to the default list.
        default_item_filters (list (of dicts)) -- Initial list of item filter dicts.

    Returns:
        list (of dicts) -- Merged list of item filter dicts.
    """
    custom_item_filter_names = [x['name'] for x in custom_item_filters]
    for item_filter in default_item_filters:
        if item_filter['name'] not in custom_item_filter_names:
            # Only merge filters that do not exist
            # `custom_item_filters.append(item_filter)` has side effects
            custom_item_filters = custom_item_filters + [item_filter]

    return custom_item_filters
