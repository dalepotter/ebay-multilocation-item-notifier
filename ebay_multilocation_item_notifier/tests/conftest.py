import datetime
import pytest
import ebaysdk
from ebay_multilocation_item_notifier.keyword_search import KeywordSearch


MOCK_SEARCH_RESULT_ZERO_ITEMS = {
  '_count': '0'
}

MOCK_SEARCH_RESULT_THREE_ITEMS = {
  'item': [
      {
        'itemId': '143183113840',
        'title': 'BROMPTON M-TYPE M6L RAW LACQUER 6 SPEED FOLDING BIKE BICYCLE',
        'globalId': 'EBAY-GB',
        'primaryCategory': {
          'categoryId': '177831',
          'categoryName': 'Bikes'
        },
        'galleryURL': 'http://thumbs1.ebaystatic.com/m/mF0LAYbX8rRCTWzZQFAvofw/140.jpg',
        'viewItemURL': 'http://www.ebay.co.uk/itm/BROMPTON-M-TYPE-M6L-RAW-LACQUER-6-SPEED-FOLDING-BIKE-BICYCLE-/143183113840',
        'paymentMethod': 'PayPal',
        'autoPay': 'false',
        'postalCode': 'BS82QY',
        'location': 'Bristol,United Kingdom',
        'country': 'GB',
        'shippingInfo': {
          'shippingServiceCost': {
            '_currencyId': 'GBP',
            'value': '0.0'
          },
          'shippingType': 'FreePickup',
          'shipToLocations': 'Worldwide'
        },
        'sellingStatus': {
          'currentPrice': {
            '_currencyId': 'GBP',
            'value': '600.0'
          },
          'convertedCurrentPrice': {
            '_currencyId': 'GBP',
            'value': '600.0'
          },
          'bidCount': '0',
          'sellingState': 'Active',
          'timeLeft': 'P3DT10H45M7S'
        },
        'listingInfo': {
          'bestOfferEnabled': 'true',
          'buyItNowAvailable': 'false',
          'startTime': datetime.datetime(2019, 3, 22, 19, 8, 29),
          'endTime': datetime.datetime(2019, 3, 29, 19, 8, 29),
          'listingType': 'Auction',
          'gift': 'false',
          'watchCount': '23'
        },
        'distance': {
          '_unit': 'mi',
          'value': '5.0'
        },
        'condition': {
          'conditionId': '3000',
          'conditionDisplayName': 'Used'
        },
        'isMultiVariationListing': 'false',
        'topRatedListing': 'false'
      },
      {
        'itemId': '123704012295',
        'title': 'Brompton Rear Mudguard For Bikes Without Rack',
        'globalId': 'EBAY-GB',
        'primaryCategory': {
          'categoryId': '72569',
          'categoryName': 'Mudguards'
        },
        'galleryURL': 'http://thumbs4.ebaystatic.com/m/mUbwtE-FOV5Ww2eBcY-xrsQ/140.jpg',
        'viewItemURL': 'http://www.ebay.co.uk/itm/Brompton-Rear-Mudguard-Bikes-Without-Rack-/123704012295',
        'paymentMethod': 'PayPal',
        'autoPay': 'false',
        'postalCode': 'BS20HS',
        'location': 'Bristol,United Kingdom',
        'country': 'GB',
        'shippingInfo': {
          'shippingServiceCost': {
            '_currencyId': 'GBP',
            'value': '0.0'
          },
          'shippingType': 'FreePickup',
          'shipToLocations': 'Worldwide'
        },
        'sellingStatus': {
          'currentPrice': {
            '_currencyId': 'GBP',
            'value': '5.0'
          },
          'convertedCurrentPrice': {
            '_currencyId': 'GBP',
            'value': '5.0'
          },
          'bidCount': '1',
          'sellingState': 'Active',
          'timeLeft': 'P4DT5H34M9S'
        },
        'listingInfo': {
          'bestOfferEnabled': 'false',
          'buyItNowAvailable': 'false',
          'startTime': datetime.datetime(2019, 3, 23, 13, 57, 31),
          'endTime': datetime.datetime(2019, 3, 30, 13, 57, 31),
          'listingType': 'Auction',
          'gift': 'false',
          'watchCount': '6'
        },
        'distance': {
          '_unit': 'mi',
          'value': '5.0'
        },
        'condition': {
          'conditionId': '3000',
          'conditionDisplayName': 'Used'
        },
        'isMultiVariationListing': 'false',
        'topRatedListing': 'false'
      },
      {
        'itemId': '153421843699',
        'title': 'Limestone large Mantel Brompton \xa0(only 3 parts available please see description)',
        'globalId': 'EBAY-GB',
        'primaryCategory': {
          'categoryId': '79650',
          'categoryName': 'Mantelpieces & Surrounds'
        },
        'galleryURL': 'http://thumbs4.ebaystatic.com/m/mVL2VrdojNrb7ilkiah9FRw/140.jpg',
        'viewItemURL': 'http://www.ebay.co.uk/itm/Limestone-large-Mantel-Brompton-only-3-parts-available-please-see-description-/153421843699',
        'paymentMethod': 'PayPal',
        'autoPay': 'false',
        'postalCode': 'BS42JP',
        'location': 'Bristol,United Kingdom',
        'country': 'GB',
        'shippingInfo': {
          'shippingServiceCost': {
            '_currencyId': 'GBP',
            'value': '0.0'
          },
          'shippingType': 'FreePickup',
          'shipToLocations': 'Worldwide'
        },
        'sellingStatus': {
          'currentPrice': {
            '_currencyId': 'GBP',
            'value': '40.0'
          },
          'convertedCurrentPrice': {
            '_currencyId': 'GBP',
            'value': '40.0'
          },
          'bidCount': '0',
          'sellingState': 'Active',
          'timeLeft': 'P0DT11H18M43S'
        },
        'listingInfo': {
          'bestOfferEnabled': 'false',
          'buyItNowAvailable': 'false',
          'startTime': datetime.datetime(2019, 3, 19, 19, 42, 5),
          'endTime': datetime.datetime(2019, 3, 26, 19, 42, 5),
          'listingType': 'Auction',
          'gift': 'false',
          'watchCount': '1'
        },
        'distance': {
          '_unit': 'mi',
          'value': '5.0'
        },
        'condition': {
          'conditionId': '3000',
          'conditionDisplayName': 'Used'
        },
        'isMultiVariationListing': 'false',
        'topRatedListing': 'false'
      }
  ],
  '_count': '3'
}


class MockKeywordSearch(KeywordSearch):
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


def generate_mock_response(search_results):
    """Return a mock ebaysdk.response.Response object that can be used to patch the output of a `ebaysdk.finding.Connection.execute` object.

    Input:
        search_results (dict) -- Representing search results to be added to the mock response.

    Returns:
        ebaysdk.response.Response -- With input search results parsed within the object.
    """

    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    mock_response = ebaysdk.response.Response(None, parse_response=False)
    mock_response.reply = AttrDict()

    mock_reply = {
        'ack': 'Success',
        'version': '1.13.0',
        'timestamp': datetime.datetime.now(),
        'searchResult': ebaysdk.response.ResponseDataObject(search_results)
    }
    mock_response.reply.update(mock_reply)
    mock_response._dict = mock_reply

    return mock_response


@pytest.fixture
def mock_response_three_items():
    """Return dictionary representaion of a `ebaysdk.response.Response` search result containing 3 items."""
    return generate_mock_response(MOCK_SEARCH_RESULT_THREE_ITEMS)


@pytest.fixture
def mock_kw_search(mocker, mock_response_three_items):
    """Return a mock `KeywordSearch` object that returns three items for each location."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items

    return MockKeywordSearch()
