import datetime
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection


search_keywords = [
    # Search keyword string
    'brompton',
    '(bike, cycle) trailer',
    'sack truck',
    'tile cutter'
]

stations = [
    #  (Location name, UK location postcode, search radius in miles (optional))
    ('Office', os.environ['OFFICE_POSTCODE'], 20),
    ('Plymouth', 'PL4 6AB', 20),
    ('Ivybridge', 'PL21 0DQ'),
    ('Totnes', 'TQ9 5JR'),
    ('Newton Abbot', 'TQ12 2JE'),
    ('Teignmouth', 'TQ14 8PG'),
    ('Dawlish', 'EX7 9PJ'),
    ('Dawlish Warren', 'EX7 0NF'),
    ('Starcross', 'EX6 8PA'),
    ('Exeter St Thomas', 'EX4 1AJ'),
    ('Exeter St Davids', 'EX4 4NT', 20),
    ('Tiverton Parkway', 'EX16 7EH'),
    ('Taunton', 'TA1 1QP'),
    ('Bridgwater', 'TA6 5HB'),
    ('Highbridge & Burnham', 'TA9 3BT'),
    ('Weston-super-Mare', 'BS23 1XY'),
    ('Weston Milton', 'BS22 8PF'),
    ('Worle', 'BS22 6WA'),
    ('Yatton', 'BS49 4AJ'),
    ('Nailsea & Backwell', 'BS48 3LH'),
    ('Parson Street', 'BS3 5PU'),
    ('Bedminster', 'BS3 4LU'),
    ('Bristol Temple Meads', 'BS1 6QF', 20),
    ('Home', os.environ['HOME_POSTCODE'], 20)
]


def get_results_dict(search_keywords, stations, default_search_radius=5):
    """Return a nested dictionary containing results for the input search keyword and locations.

    Inputs:
        search_keywords (list of str) -- List of eBay search keyword strings
        stations (list of tuples) -- List of locations tuples in the format (Location name, UK location postcode, search radius in miles (optional))

    Returns:
        dict (of dicts) -- A two-dimensional dictionary containing search keywords (keys) and location search results (key, value pairs)
                           An example ebaysdk.response.ResponseDataObject (representing an item search result) can be found in tests/test_itemfinder.py
    """
    results = dict()

    api = Connection(
            appid='DP1dc611a-5511-41c1-b35e-99291acf532',
            siteid='EBAY-GB',
            config_file=None
    )

    for keyword in search_keywords:
        results[keyword] = dict()

        for station in stations:
            station_name = station[0]
            postcode = station[1]
            max_distance = default_search_radius
            try:
                max_distance = str(station[2])
            except IndexError:
                pass

            try:
                api_payload = {
                        'keywords': keyword,
                        'itemFilter': [
                            {'name': 'Condition',
                             'value': 'Used'},
                            {'name': 'ListingType',
                             'value': 'Auction'},
                            {'name': 'MaxDistance',
                             'value': max_distance},
                            {'name': 'LocalPickupOnly',
                             'value': True},
                            # Params for searching for sold items:
                            # {'name': 'SoldItemsOnly',
                            #  'value': True}
                        ],
                        'buyerPostalCode': postcode
                    }

                # Search for listings
                response = api.execute('findItemsAdvanced', api_payload)
                #  API verb for completed items: findCompletedItems

                assert(response.reply.ack == 'Success')
                assert(type(response.reply.timestamp) == datetime.datetime)
                assert(type(response.dict()) == dict)

            except ConnectionError as e:
                print(e)
                print(e.response.dict())

            print("Search keyword: {} - Station: {} - Results {}".format(
                keyword,
                station,
                response.reply.searchResult._count
            ))

            # Append search result to the output dictionary
            results[keyword][station_name] = response.reply.searchResult  # ebaysdk.response.ResponseDataObject

    return results

if __name__ == '__main__':
    results_dict = get_results_dict(search_keywords, stations)
    import pdb; pdb.set_trace()
