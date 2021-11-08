import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from ebay_multilocation_item_notifier.utils import generate_item_filter_list


class KeywordSearch():
    """Base class, where the subclass represents one item search."""
    cached_results = {}
    default_search_radius = 5
    search_filters = []
    search_keyword = ""
    search_locations = []

    def find_items(self):
        """Return a dictionary of items for the search keyword and search locations.

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

    @property
    def results(self):
        """Return search results (either from cached data, or through calling the ebay API).

        Returns:
            dict -- Two dimensional dict containing item keywords (key) and dict of item location results.
        """
        if not self.cached_results:
            self.cached_results = self.find_items()

        return self.cached_results
