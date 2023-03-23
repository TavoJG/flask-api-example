import pytest
from stocks_api import create_app
from stocks_api.services.stocks import StocksService
from stocks_api.services.users import UsersService
from stocks_api.services.database import MockDatabase


@pytest.fixture
def stocks_api_response():
    return {
        "Meta Data": {
            "1. Information": "Daily Time Series with Splits and Dividend Events",
            "2. Symbol": "META",
            "3. Last Refreshed": "2023-03-21 16:00:01",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2023-03-21": {
                "1. open": "203.2",
                "2. high": "203.55",
                "3. low": "197.95",
                "4. close": "202.16",
                "5. adjusted close": "202.16",
                "6. volume": "31807463",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0"
            },
            "2023-03-20": {
                "1. open": "198.48",
                "2. high": "199.36",
                "3. low": "193.64",
                "4. close": "197.81",
                "5. adjusted close": "197.81",
                "6. volume": "25186315",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0"
            }
        }
    }


@pytest.fixture
def stocks_api_no_symbol_response():
    return {
        "Error Message": "Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY_ADJUSTED."
    }


@pytest.fixture
def stocks_service():
    _stocks_service = StocksService()
    _stocks_service.url = 'http://test.com'
    return _stocks_service


@pytest.fixture
def get_stock_data_response():
    return {
        "closingPriceVariation": "4.35",
        "date": "2023-03-21",
        "higherPrice": "203.55",
        "lowerPrice": "197.95",
        "openPrice": "203.2"
    }


@pytest.fixture
def new_user():
    return {
        'firstName': 'Test',
        'lastName': 'Guy',
        'email': 'testguy@putsbox.com'
    }


@pytest.fixture
def database_service():
    return MockDatabase()


@pytest.fixture
def users_service(database_service):
    return UsersService(database_service)


@pytest.fixture
def app():
    app = create_app(test_mode=True)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
