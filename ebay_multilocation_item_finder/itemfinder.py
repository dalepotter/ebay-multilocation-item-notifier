import datetime
import os
import emails
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from ebay_multilocation_item_finder.utils import generate_item_filter_list, render_email_template

searches = [
    # (Search keyword string (str), [optional] custom item filters (list of dicts))
    ['brompton'],
    ['(bike, cycle) trailer', [
        {'name': 'MaxPrice', 'value': 25}
    ]],
    ['sack truck -(antique, vintage, wooden)', [
        {'name': 'MaxPrice', 'value': 20}
    ]],
    ['radio (roberts, vintage) -(magazines, times, car, valve, valves)', [
        {'name': 'MaxPrice', 'value': 10}
    ]],
    ['(headphones, earphones)'],
    ['(back pack, back packer, back packers, back packing, backpack, backpacker, backpackers, backpacking, hiking) tent'],
    ['(bike, bicycle)']
]

search_locations = [
    #  (Location name, UK location postcode, search radius in miles (optional))
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
        subject='[ebay-multilocation-item-finder] Item summary',
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
