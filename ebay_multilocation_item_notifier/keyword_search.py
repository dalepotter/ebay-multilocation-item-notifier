import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection


class KeywordSearchMeta(type):
    """Meta class controlling behaviour of new class objects."""

    def __new__(cls, name, bases, attrs):
        """Merge `.search_filters` from parent classes (if permitted by the child class)."""
        new_cls = super(KeywordSearchMeta, cls).__new__(cls, name, bases, attrs)

        if new_cls.merge_parent_search_filters:
            base_search_filters = [
                bc.search_filters for bc in bases if hasattr(bc, "search_filters")
            ]
            search_filters = base_search_filters + [new_cls.search_filters]

            new_cls.search_filters = {}
            for filter in search_filters:
                new_cls.search_filters.update(filter)

        return new_cls


class KeywordSearch(metaclass=KeywordSearchMeta):
    """Base class, where the subclass represents one item search."""

    cached_results = {}
    location_radius_overrides_default_search_radius = True
    merge_parent_search_filters = True
    search_filters = {
        "LocalPickupOnly": True,
        "MaxDistance": "5",
    }  # Available item filters: https://developer.ebay.com/devzone/finding/CallRef/types/ItemFilterType.html
    search_keyword = ""
    search_locations = []
    remove_duplicates = False  # If True, only the first item seen will be returned. This will NOT necessarily be at the closest location.

    def find_items(self):
        """Return a dictionary of items for the search keyword and search locations.

        Returns:
            dict -- Containing [key] locaton (string) and [value] search results (ebaysdk.response.ResponseDataObject).
                    An example ebaysdk.response.ResponseDataObject (representing a search result for a single location)
                    can be found in tests/integration/test_item_notifier.py
        """
        results = dict()

        api = Connection(
            appid="DP1dc611a-5511-41c1-b35e-99291acf532",
            siteid="EBAY-GB",
            config_file=None,
        )

        for search_location in self.search_locations:
            search_location_name = search_location[0]
            postcode = search_location[1]
            item_filters = self.search_filters.copy()
            if self.location_radius_overrides_default_search_radius:
                try:
                    item_filters.update({"MaxDistance": str(search_location[2])})
                except IndexError:
                    pass

            try:
                api_payload = {
                    "keywords": self.search_keyword,
                    "itemFilter": self.generate_item_filter_list(item_filters),
                    "buyerPostalCode": postcode,
                }

                # Search for listings
                response = api.execute("findItemsAdvanced", api_payload)
                #  API verb for completed items: findCompletedItems

                assert response.reply.ack == "Success"
                assert type(response.reply.timestamp) == datetime.datetime
                assert type(response.dict()) == dict

            except ConnectionError as e:
                print(e)
                print(e.response.dict())

            print(
                "Search keyword: {} - search_location: {} - Results for this location: {}".format(
                    self.search_keyword,
                    search_location,
                    response.reply.searchResult._count,
                )
            )

            # Append search result to the output dictionary
            results[
                search_location_name
            ] = response.reply.searchResult  # ebaysdk.response.ResponseDataObject

        return results

    def generate_item_filter_list(self, custom_item_filters={}):
        """Return a list of ebay API item filters. Merges any custom_item_filters into the class search_filters.
        Item filters within custom_item_filter always take priority if there are conflicts.

        Available item filters: https://developer.ebay.com/devzone/finding/CallRef/types/ItemFilterType.html

        Inputs:
            custom_item_filters (dict) -- Containing item filters to be merged into the default list.

        Returns:
            list (of dicts) -- Item filters in a structure supported by the ebay API.
        """
        item_filters = self.search_filters.copy()
        item_filters.update(custom_item_filters)
        output = list()
        for key, value in item_filters.items():
            output.append({"name": key, "value": value})

        return output

    @property
    def results(self):
        """Return search results (either from cached data, or through calling the ebay API).

        Returns:
            dict -- Containing [key] locaton (string) and [value] search results (ebaysdk.response.ResponseDataObject).
        """
        if not self.cached_results:
            self.cached_results = self.find_items()

        # Set default output
        output = self.cached_results

        if self.remove_duplicates:
            seen_item_ids = []
            for location, loc_results in output.items():
                try:
                    output[location].item = [
                        itm
                        for itm in output[location].item
                        if itm.itemId not in seen_item_ids
                    ]
                    seen_item_ids += [item.itemId for item in loc_results.item]
                except AttributeError:
                    # output[location].item not present (indicating zero results for this location)
                    pass

        return output
