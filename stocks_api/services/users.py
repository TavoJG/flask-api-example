import secrets
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import BadRequest


class UsersService:

    def __init__(self, database_service) -> None:
        self.db_service = database_service
        self.users_collection = self.db_service.db['users']
        self.users_collection.create_index('email', unique=True)

    def sign_up(self, user_data: dict[str, str]) -> dict[str, str]:
        api_key = secrets.token_urlsafe(24)
        user_data['apiKey'] = api_key
        try:
            self.users_collection.insert_one(user_data)
            return {'apiKey': api_key}
        except DuplicateKeyError:
            raise BadRequest(
                f'email {user_data["email"]} is already registered')

    def is_api_key_valid(self, api_key: str) -> bool:
        user = self.users_collection.find_one({'apiKey': api_key})
        return bool(user)
