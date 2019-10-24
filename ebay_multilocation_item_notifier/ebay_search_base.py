import datetime
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from ebay_multilocation_item_notifier.utils import generate_item_filter_list


class EbaySearchItemBase():
    """Base class, where the subclass represents one item search."""
    default_search_radius = 5
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
    search_keyword = ""
    search_locations = [
        #  (Location name, UK location postcode, search radius in miles (optional))
        ('Saltash', 'PL12 4EB'),
        ('St Germans', 'PL12 5LS'),
        ('Liskeard', 'PL14 4DX'),
        ('Bodmin Parkway', 'PL30 4BB'),

        ('St Keyne Wishing Well Halt', 'PL14 4SE'),
        ('Causeland', 'PL14 4ST'),
        ('Sandplace', 'PL13 1PJ'),
        ('Looe', 'PL13 1HN'),

        ('Gunnislake', 'PL18 9DZ'),
        ('Calstock', 'PL18 9QY'),
        ('Bere Alston', 'PL20 7EP'),
        ('Bere Ferrers', 'PL20 7JS'),

        ('Tavistock', 'PL19 8AY'),

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

    def find_items(self):
        """Return a dictionary of itmes for the search keyword and search locations.

        Returns:
            dict -- A two-dimensional dictionary containing search locations (keys) and results (value)
                    An example ebaysdk.response.ResponseDataObject (representing an item search result) can be found in tests/test_itemfinder.py
        """
        results = dict()

        api = Connection(
            appid='DP1dc611a-5511-41c1-b35e-99291acf532',
            siteid='EBAY-GB',
            config_file=None
        )

        for search_location in self.search_locations:
            search_location_name = search_location[0]
            postcode = search_location[1]
            max_distance = str(self.default_search_radius)
            try:
                max_distance = str(search_location[2])
            except IndexError:
                pass

            try:
                item_filters = self.search_filters.copy()
            except IndexError:
                item_filters = []
                pass
            item_filters += [
                {'name': 'MaxDistance',
                 'value': max_distance}
            ]

            try:
                api_payload = {
                    'keywords': self.search_keyword,
                    'itemFilter': generate_item_filter_list(item_filters),
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

            print("Search keyword: {} - search_location: {} - Results {}".format(
                self.search_keyword,
                search_location,
                response.reply.searchResult._count
            ))

            # Append search result to the output dictionary
            results[search_location_name] = response.reply.searchResult  # ebaysdk.response.ResponseDataObject

        return results

    def generate_item_filter_list(self):
        pass
