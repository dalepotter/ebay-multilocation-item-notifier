import ebaysdk.response
import pytest
import ebay_multilocation_item_notifier.tests.conftest as conftest
from ebay_multilocation_item_notifier.utils import render_email_template


@pytest.fixture
def mock_search_result_three_items():
    """Return a ebaysdk.response.ResponseDataObject containing three items."""
    return ebaysdk.response.ResponseDataObject(
        conftest.MOCK_SEARCH_RESULT_THREE_ITEMS
    )


def test_output_renders_from_template():
    """Ensure that the template is rendering content from the expected template."""
    mock_results = {}

    result = render_email_template(mock_results)

    assert isinstance(result, str)
    assert 'following items were found' in result


def test_single_location_results_in_template(mock_search_result_three_items):
    """A results dictionary must render into the expected template format."""
    mock_results = {
        'Search keyword 1': {
            'Location 1': mock_search_result_three_items
        }
    }
    result = render_email_template(mock_results)

    assert 'Search keyword 1' in result
    assert 'Location 1' in result
    assert 'BROMPTON M-TYPE M6L RAW LACQUER 6 SPEED FOLDING BIKE BICYCLE' in result
    # Build up more expected strings to be found in the rendered template here.
