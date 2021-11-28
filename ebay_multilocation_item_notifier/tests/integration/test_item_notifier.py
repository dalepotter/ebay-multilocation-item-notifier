import re
import emails
import pytest
from collections import namedtuple
from ebay_multilocation_item_notifier.itemfinder import main
from ebay_multilocation_item_notifier.keyword_search import KeywordSearch
from ebay_multilocation_item_notifier.keyword_search_container import KeywordSearchContainer


class Bike(KeywordSearch):
    """Set up a search that can be expected to return a large number of items."""
    search_keyword = "(bike, bicycle)"
    search_filters = [
        {'name': 'MaxPrice', 'value': 1000}
    ]
    search_locations = [
        #  (Location name, UK location postcode, search radius in miles (optional))
        ("London Charing Cross Station", "WC2N 5HF"),
        ("Birmingham New Street Station", "B2 4QA"),
        ("Edinburgh Waverley Station", "EH8 8DL")
    ]

kw_container = KeywordSearchContainer(
    Bike()
)


class FakeMessage():
    def send(self, *args, **kwargs):
        mock_response = namedtuple('FakeSMTPResponse', ['status_code'])
        return mock_response(status_code=250)


@pytest.mark.uses_ebay_api
def test_main(capsys, mocker, caplog):
    mocker.patch.object(emails, 'html', return_value=FakeMessage())
    result = main(kw_container)

    stdout, stderr = capsys.readouterr()
    stdout_lines = [x for x in filter(len, stdout.split("\n"))]  # Split by new line, but exclude empty lines

    results_per_location = [int(re.search(r'Results (\d+)', line).group(1)) > 0 for line in stdout_lines]
    email_html_call = emails.html.call_args_list[0].kwargs

    assert len(stdout_lines) == 3  # There much be an output for each search item/location permutation
    assert all(["(bike, bicycle)" in x for x in stdout_lines])  # The keyword must be outputeed in each line
    assert all(
        [int(re.search(r'Results (\d+)', line).group(1)) > 0 for line in stdout_lines]
    )  # There must be at least 1 result for each search location
    print(type(email_html_call))
    print(email_html_call)
    assert False
    assert email_html_call['subject'] == '[ebay-multilocation-item-notifier] Item summary'
    assert email_html_call['html']  # The message string must not be empty
