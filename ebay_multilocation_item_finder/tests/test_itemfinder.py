import ebaysdk
from ..itemfinder import get_results_dict


def test_get_results_empty_input_returns_empty_dict(mocker, mock_response_three_items):
    """`get_results_dict` with no data must return an empty dictionary."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items
    result = get_results_dict([], [])

    assert isinstance(result, dict)
    assert result == {}


def test_get_results_with_input_returns_nested_dict(mocker, mock_response_three_items):
    """`get_results_dict` with mocked data must return a nested dictionary with the input search keyword as a parent of the input location."""
    mocker.patch.object(ebaysdk.finding.Connection, 'execute')
    ebaysdk.finding.Connection.execute.return_value = mock_response_three_items

    result = get_results_dict(
                ['search keyword 1'],
                [('location 1', 'PL4 6AB', 20)]
    )

    assert 'search keyword 1' in result.keys()
    assert 'location 1' in result['search keyword 1'].keys()
    assert isinstance(result['search keyword 1']['location 1'], ebaysdk.response.ResponseDataObject)
    assert result['search keyword 1']['location 1']._count == '3'
    assert len(result['search keyword 1']['location 1'].item) == 3
