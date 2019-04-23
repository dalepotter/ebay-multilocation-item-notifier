import datetime
import os
import emails
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection


search_keywords = [
    # Search keyword string
    'brompton',
    '(bike, cycle) trailer',
    'sack truck',
    'tile cutter'
]

search_locations = [
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


def get_results_dict(search_keywords, search_locations, default_search_radius=5):
    """Return a nested dictionary containing results for the input search keyword and locations.

    Inputs:
        search_keywords (list of str) -- List of eBay search keyword strings
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

    for keyword in search_keywords:
        results[keyword] = dict()

        for search_location in search_locations:
            search_location_name = search_location[0]
            postcode = search_location[1]
            max_distance = default_search_radius
            try:
                max_distance = str(search_location[2])
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

            except Exception as e:
                print(type(e))
                print(e)

            print("Search keyword: {} - search_location: {} - Results {}".format(
                keyword,
                search_location,
                response.reply.searchResult._count
            ))

            # Append search result to the output dictionary
            results[keyword][search_location_name] = response.reply.searchResult  # ebaysdk.response.ResponseDataObject

    return results

if __name__ == '__main__':
    from utils import render_email_template  # FIXME: Move to top of file
    results_dict = get_results_dict(search_keywords, search_locations)

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
