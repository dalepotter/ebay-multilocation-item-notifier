import os
import emails
import ebay_multilocation_item_notifier.items.items as items
from ebay_multilocation_item_notifier.keyword_search_container import KeywordSearchContainer

items = KeywordSearchContainer(
    items.WallpaperSteamer(),
    items.Brompton(),
    items.RaleighCameo(),
    items.FoldingBike(),
    items.UppababyVista(),
    items.BikeTrailer(),
    items.SackTruck(),
    items.BackpackingTent(),
    items.Bike()
)


def get_results_dict(container):
    """Return a nested dictionary containing results for the input search keywords and locations.

    Inputs:
        container (KeywordSearchContainer) -- Object containing eBay keyword searches.

    Returns:
        dict (of dicts) -- A two-dimensional dictionary containing search keywords (keys) and location search results (key, value pairs)
                           An example ebaysdk.response.ResponseDataObject (representing an item search result) can be found in tests/test_itemfinder.py
    """
    results_dict = dict()
    for item in container.search_list:
        # Use item.results
        results_dict[item.search_keyword] = item.find_items()
    return results_dict


if __name__ == '__main__':
    html_summary = items.render_email_template()

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
