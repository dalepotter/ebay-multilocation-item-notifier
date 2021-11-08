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
