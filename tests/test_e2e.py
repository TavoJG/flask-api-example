def test_health_status(client):
    response = client.get('/health')
    assert response.json == {'status': 'OK'}


def test_create_user(client, new_user):
    response = client.post('/sign_up', json=new_user)
    assert 'apiKey' in response.json


def test_get_stocks_data(client, requests_mock, stocks_api_response, get_stock_data_response):
    requests_mock.get('http://test.com', json=stocks_api_response)
    response = client.get(
        '/stocks', headers={'Authorization': 'Token fakeapikey'}, query_string={'symbol': 'META'})
    assert response.status == '200 OK'
    assert response.json == get_stock_data_response


def test_get_stocks_data_no_token(client):
    response = client.get(
        '/stocks',  query_string={'symbol': 'META'})
    assert response.status == '401 UNAUTHORIZED'


def test_get_stocks_data_bad_token_format(client):
    response = client.get(
        '/stocks', headers={'Authorization': 'Bearer fakeapikey'}, query_string={'symbol': 'META'})
    assert response.status == '401 UNAUTHORIZED'


def test_get_stocks_data_invalid_api_key(client):
    response = client.get(
        '/stocks', headers={'Authorization': 'Token invalidapikey'}, query_string={'symbol': 'META'})
    assert response.status == '401 UNAUTHORIZED'


def test_get_stocks_data_without_symbol(client):
    response = client.get(
        '/stocks', headers={'Authorization': 'Token fakeapikey'})
    assert response.status == '400 BAD REQUEST'
