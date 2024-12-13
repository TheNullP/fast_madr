from http import HTTPStatus


def test_login_com_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password
        }
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' == token
    assert 'token_type' in token
