from jwt import decode

from fast_madr.core.config import ALGORITHM, SECRET_KEY


def test_jwt(user, access_token):
    response = decode(
        access_token['access_token'], SECRET_KEY, algorithms=[ALGORITHM]
    )

    assert response['usr'] == user.username
    assert access_token['token_type']
