import logging
from os import environ

from werkzeug.exceptions import NotFound, InternalServerError
from requests_cache import CachedSession

logger = logging.getLogger(__name__)


class StocksService:

    def __init__(self) -> None:
        self.query_dict = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "outputsize": "compact",
            "apikey": environ.get('STOCK_API_KEY')
        }
        self.url = environ.get('STOCK_API_URL')
        self.session = CachedSession(backend='memory', expire_after=environ.get(
            'STOCK_API_CACHE_EXPIRE_TIME', 3600))

    def _get_stock_data_from_api(self, symbol: str) -> dict[str, dict[str]]:
        query_params = {"symbol": symbol}
        query_params.update(self.query_dict)
        try:
            response = self.session.get(
                self.url, params=query_params)
            response.raise_for_status()
            result = response.json()
            # Stocks api always returns a 200 status code, even if symbol doesn't exists. We need to check API response
        except Exception as e:
            logger.error(e)
            raise InternalServerError("Error when consulting Stock API")

        if "Meta Data" not in result:
            raise NotFound('Stock symbol not found')
        return result

    def get_stock_data(self, symbol: str) -> dict[str, str]:
        stock_data = self._get_stock_data_from_api(symbol)
        time_series = stock_data.get("Time Series (Daily)")
        last_date = max(time_series.keys())
        last_date_data: dict = time_series.pop(last_date)
        second_last_date = max(time_series.keys())
        second_last_date_data: dict = time_series.pop(second_last_date)
        closing_price_variation = float(last_date_data.get(
            "4. close")) - float(second_last_date_data.get("4. close"))

        result = {
            "date": last_date,
            "openPrice": last_date_data.get("1. open"),
            "higherPrice": last_date_data.get("2. high"),
            "lowerPrice": last_date_data.get("3. low"),
            "closingPriceVariation": f'{closing_price_variation:.2f}'
        }
        return result
