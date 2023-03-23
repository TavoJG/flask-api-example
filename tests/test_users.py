import pytest
from werkzeug.exceptions import BadRequest


def test_signup_user(new_user, users_service):
    result = users_service.sign_up(new_user)
    assert 'apiKey' in result


def test_signup_user_duplicate_email(new_user, users_service):
    users_service.sign_up(new_user)
    with pytest.raises(BadRequest):
        users_service.sign_up(new_user)


def test_validate_api_key(users_service):
    result = users_service.is_api_key_valid('fakeapikey')
    assert result


def test_validate_invalid_api_key(users_service):
    result = users_service.is_api_key_valid('invalidapikey')
    assert not result
