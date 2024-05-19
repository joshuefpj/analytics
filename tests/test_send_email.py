from ..analytic.send_email import template_replace, get_months_details
from ..analytic.utils import read_file

from pathlib import Path

base_dir = Path(__file__).parents[0]


def test_template_replace():
    # Act.
    _data = {
        'TOTAL_BALANCE': -28389.129999999997,
        'DEBIT_AMOUNT': -524.4848506401138,
        'CREDIT_AMOUNT': 503.43745562130175,
        'MONTH_TRX': {
            'May': 263,
            'June': 279,
            'July': 326,
            'August': 268,
            'September': 243
        }
    }

    expected_file = base_dir / 'data' / 'test_template_replace.html'
    expected_data = read_file(expected_file, 1)

    # Arrange.
    result = template_replace(_data)
    print(result)

    # Assert.
    assert result == expected_data


def test_get_months_details():
    # Act.
    details = {
        'MONTH_TRX': {
            '5': 265,
            '6': 271,
            '7': 303,
            '8': 265,
            '9': 275
        }
    }
    expected_data = """
                <p>Number of transactions in May: <b>265</b></p>
                <p>Number of transactions in June: <b>271</b></p>
                <p>Number of transactions in July: <b>303</b></p>
                <p>Number of transactions in August: <b>265</b></p>
                <p>Number of transactions in September: <b>275</b></p>"""

    # Arrange.
    result = get_months_details(details['MONTH_TRX'])

    # Assert.
    assert result == expected_data
