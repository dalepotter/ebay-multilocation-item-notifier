import re
import pytest
from bs4 import BeautifulSoup
from ebay_multilocation_item_notifier.keyword_search_container import KeywordSearchContainer


@pytest.mark.parametrize("number_of_mock_searches", [0, 1, 10, 5])  # Unordered to test a new object overwrites existing searches
def test_input_searches_added_to_list(mock_kw_search, number_of_mock_searches):
    """`KeywordSearch` objects must be bound to the container's `search_list` property."""
    list_of_mock_searches = [mock_kw_search] * number_of_mock_searches

    mock_container = KeywordSearchContainer(*list_of_mock_searches)

    assert len(mock_container.search_list) == number_of_mock_searches

@pytest.fixture
def email_content_bs4_soup(mock_kw_search):
    """Returns email body content as a `BeautifulSoup` object."""
    mock_container = KeywordSearchContainer(
        mock_kw_search
    )

    email_content = mock_container.render_email_template()
    return BeautifulSoup(email_content, 'html.parser')


def test_output_renders_from_template(email_content_bs4_soup):
    """Ensure that the template is rendering content from the expected template."""
    assert email_content_bs4_soup.find('p').text == "The following items were found for the specified locations listed:"


def test_single_location_results_in_template(email_content_bs4_soup):
    """A container with results for 3 items & 3 locations must render into the expected template format."""
    search_keywords = email_content_bs4_soup.select('p > strong')
    location_1_lines = [x for x in email_content_bs4_soup.find_all("li") if 'location 1' in x.text]
    location_2_lines = [x for x in email_content_bs4_soup.find_all("li") if 'location 2' in x.text]
    location_3_lines = [x for x in email_content_bs4_soup.find_all("li") if 'location 3' in x.text]

    assert len(search_keywords) == 1  # `mock_container` has only one kw search object
    assert search_keywords[0].text == 'search keyword 1'
    assert (
        len(location_1_lines)
        == len(location_2_lines)
        == len(location_3_lines)
        == 3
    )  # `mock_container` contains 3 items for each location
    assert location_1_lines[0].find('a').text == 'BROMPTON M-TYPE M6L RAW LACQUER 6 SPEED FOLDING BIKE BICYCLE'
    # Build up more expected strings to be found in the rendered template here.
