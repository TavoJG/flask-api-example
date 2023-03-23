import pytest

from werkzeug.exceptions import NotFound, InternalServerError
from requests.exceptions import ConnectTimeout


def test_get_stock_data_from_api(requests_mock, stocks_api_response, stocks_service):
    requests_mock.get('http://test.com', json=stocks_api_response)
    result = stocks_service._get_stock_data_from_api('META')
    assert result == stocks_api_response


def test_get_stock_data_from_api_no_symbol(requests_mock, stocks_api_no_symbol_response, stocks_service):
    requests_mock.get('http://test.com', json=stocks_api_no_symbol_response)
    with pytest.raises(NotFound):
        stocks_service._get_stock_data_from_api('FAKE_SYMBOL')


def test_get_stock_data_from_api_request_error(requests_mock, stocks_service):
    requests_mock.get('http://test.com', exc=ConnectTimeout)
    with pytest.raises(InternalServerError):
        stocks_service._get_stock_data_from_api('FAKE_SYMBOL')


def test_get_stock_data(requests_mock, stocks_api_response, stocks_service, get_stock_data_response):
    requests_mock.get('http://test.com', json=stocks_api_response)
    result = stocks_service.get_stock_data('META')
    assert result == get_stock_data_response


def test_get_stock_data_no_symbol(requests_mock, stocks_api_no_symbol_response, stocks_service):
    requests_mock.get('http://test.com', json=stocks_api_no_symbol_response)
    with pytest.raises(NotFound):
        stocks_service.get_stock_data('META')
