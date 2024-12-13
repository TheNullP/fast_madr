from fast_madr.security import  (ALGORITHM, create_access_token, SECRET_KEY)
from jwt import decode

def test_jwt():
    data = {'test': 'test@test.com'}
    token = create_access_token(data)

    response = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert response['test'] == data['test']
    assert response['exp']
