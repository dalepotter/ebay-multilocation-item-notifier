import datetime
import os
import emails
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from ebay_multilocation_item_notifier.utils import generate_item_filter_list, render_email_template

searches = [
    # (Search keyword string (str), [optional] custom item filters (list of dicts))
    ['wallpaper (stripper, steamer)', [
        {'name': 'MaxPrice', 'value': 10}
    ]],
    ['brompton', [
        {'name': 'MaxPrice', 'value': 150}
    ]],
    ['raleigh cameo'],
    ['folding (bike, bicycle) -(exercise, motor, quad, rack)', [
        {'name': 'MaxPrice', 'value': 80}
    ]],
    ['uppababy vista', [
        {'name': 'MaxDistance', 'value': '10'}
    ]],
    ['(bike, cycle) trailer', [
        {'name': 'MaxPrice', 'value': 25}
    ]],
    ['sack truck -(antique, vintage, wooden)', [
        {'name': 'MaxPrice', 'value': 20}
    ]],
    ['(back pack, back packer, back packers, back packing, backpack, backpacker, backpackers, backpacking, hiking) tent', [
        {'name': 'MaxPrice', 'value': 40}
    ]],
    ['(bike, bicycle) -(boys, childs, exercise, girls, journal, kids, magazine, motor, quad, rack)', [
        {'name': 'MaxPrice', 'value': 15}
    ]]
]

search_locations = [
    #  (Location name, UK location postcode, search radius in miles (optional))
    ('Home', os.environ['HOME_POSTCODE'], 10),

    ("M4 J20", "BS32 4JT"),
    ("M4 J19", "BS16 1SX"),
    ("M4 J18", "BS37 6EJ"),
    ("M4 J17", "SN14 6BF"),
    ("M4 J16", "SN4 8QP"),
    ("M4 J15", "SN4 0ET"),
    ("M4 J14", "RG17 0PU"),
    ("M4 J13", "RG20 8XY"),
    ("M4 J12", "RG7 4TX"),
    ("M4 J11", "RG2 8FT"),
    ("M4 J10", "RG40 5QS"),
    ("M4 J9B", "SL6 4LJ"),
    ("M4 J9A", "SL6 2PJ"),
    ("M4 J9", "SL6 2HY"),
    ("M4 J8", "SL6 2HY"),
    ("M4 J7", "SL1 5LX"),
    ("M4 J6", "SL1 2SZ"),
    ("M4 J5", "SL3 8UG"),

    ("M25 J14", "SL3 0FD"),
    ("M25 J15", "UB7 7HQ"),
    ("M25 J16", "SL0 0NY"),
    ("M25 J17", "WD3 5DJ"),
    ("M25 J18", "WD3 5TQ"),
    ("M25 J19", "WD3 4ND"),
    ("M25 J20", "WD4 8QP"),
    ("M25 J21", "WD5 0SB"),
    ("M25 J21A", "AL2 3ET"),
    ("M25 J22", "AL2 1BX"),
    ("M25 J23", "EN6 3NP"),
    ("M25 J24", "EN6 5ER"),
    ("M25 J25", "EN8 8EZ"),
    ("M25 J26", "EN9 3QY"),

    ("Chingford station", "E4 6AL", 10),
    ("Piccadilly Circus station", "W1J 9HS", 10)
]


def get_results_dict(search_keywords, search_locations, default_search_radius=5):
    """Return a nested dictionary containing results for the input search keyword and locations.

    Inputs:
        search_keywords (list of lists) -- List of eBay search keyword strings
        search_locations (list of tuples) -- List of locations tuples in the format (Location name, UK location postcode, search radius in miles (optional))

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

    for search_list in search_keywords:
        keyword = search_list[0]

        results[keyword] = dict()

        for search_location in search_locations:
            search_location_name = search_location[0]
            postcode = search_location[1]
            max_distance = str(default_search_radius)
            try:
                item_filters = search_list[1].copy()
            except IndexError:
                item_filters = []
                pass
            try:
                max_distance = str(search_location[2])
            except IndexError:
                pass

            item_filters += [
                {'name': 'MaxDistance',
                 'value': max_distance}
            ]

            try:
                api_payload = {
                        'keywords': keyword,
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
                keyword,
                search_location,
                response.reply.searchResult._count
            ))

            # Append search result to the output dictionary
            results[keyword][search_location_name] = response.reply.searchResult  # ebaysdk.response.ResponseDataObject

    return results

if __name__ == '__main__':
    results_dict = get_results_dict(searches, search_locations)

    html_summary = render_email_template(results_dict)

    message = emails.html(
        subject='[ebay-multilocation-item-notifier] Item summary',
        html=html_summary,
        mail_from=(os.environ['EMAIL_SENDER_NAME'], os.environ['EMAIL_SENDER_ADDRESS'])
    )
    req = message.send(to=(os.environ['EMAIL_RECIPIENT_NAME'], os.environ['EMAIL_RECIPIENT_ADDRESS']),
                       smtp={'host': os.environ['EMAIL_SMTP_HOST'],
                             'port': 465,
                             'ssl': True,
                             'user': os.environ['EMAIL_SMTP_USERNAME'],
                             'password': os.environ['EMAIL_SMTP_PASSWORD']}
                       )
    assert req.status_code == 250
