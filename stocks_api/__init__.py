from os import environ
from dotenv import load_dotenv
from flask import Flask, request, json
from flask_expects_json import expects_json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.exceptions import HTTPException

from stocks_api.schemas import user_schema
from stocks_api.decorators import api_key_required
from stocks_api.services.stocks import StocksService
from stocks_api.services.users import UsersService
from stocks_api.services.database import DatabaseService, MockDatabase

# ENV variables from .env file
load_dotenv()


def create_app(test_mode=False):

    app = Flask(__name__)

    env = environ.get('FLASK_ENV', 'development').lower()

    app.debug = env != 'production'
    app.testing = test_mode

    if test_mode:
        environ['STOCK_API_URL'] = 'http://test.com'

    # Fix to relaibly get remote address of user behind a proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
    limiter = Limiter(get_remote_address, app=app,
                      default_limits=['200/day', '50/hour'],
                      storage_uri=environ.get('DB_CONN_STRING'))

    database_service = DatabaseService() if not test_mode else MockDatabase()
    stocks_service = StocksService()
    users_service = UsersService(database_service)

    # Error handler

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    @app.route("/stocks", methods=['GET'])
    @api_key_required(users_service.is_api_key_valid)
    @limiter.limit('10/hour', key_func=lambda: request.api_key)
    def get_stocks():
        symbol = request.args.get('symbol')
        return stocks_service.get_stock_data(symbol) if symbol else ('Stock symbol missing in query params', 400)

    @app.route("/sign_up",  methods=['POST'])
    @expects_json(user_schema)
    def sign_up():
        user_data = request.get_json()
        return users_service.sign_up(user_data)

    @app.route("/health", methods=['GET'])
    def get_health_status():
        return {'status': 'OK'}

    return app
