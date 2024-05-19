from ..analytic.utils import get_keys


def test_get_keys():
    # Arrange.
    expected_dict = {
        'check': 'ok',
        'user': 'testing',
        'email': 'testing@noexisto.com',
    }

    # Act.
    result_dict = get_keys('test_data')

    # Assert.
    assert expected_dict == result_dict
