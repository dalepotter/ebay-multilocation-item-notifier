import pytest
from ebay_multilocation_item_notifier.keyword_search_container import KeywordSearchContainer


@pytest.mark.parametrize("number_of_mock_searches", [0, 1, 10, 5])  # Unordered to test a new object overwrites existing searches
def test_search_added_to_list(mock_kw_search, number_of_mock_searches):
    list_of_mock_searches = [mock_kw_search] * number_of_mock_searches

    mock_container = KeywordSearchContainer(*list_of_mock_searches)

    assert len(mock_container.search_list) == number_of_mock_searches


def test_output_renders_from_template(mock_kw_search_with_three_locations_three_items):
    """Ensure that the template is rendering content from the expected template."""
    mock_container = KeywordSearchContainer(
        mock_kw_search_with_three_locations_three_items
    )

    result = mock_container.render_email_template()

    assert isinstance(result, str)
    assert 'following items were found' in result


def test_single_location_results_in_template(mock_kw_search_with_three_locations_three_items):
    """A container with results for 3 items & 3 locations must render into the expected template format."""
    mock_container = KeywordSearchContainer(
        mock_kw_search_with_three_locations_three_items
    )

    result = mock_container.render_email_template()

    assert 'search keyword 1' in result
    assert 'location 1' in result
    assert 'BROMPTON M-TYPE M6L RAW LACQUER 6 SPEED FOLDING BIKE BICYCLE' in result
    # Build up more expected strings to be found in the rendered template here.
