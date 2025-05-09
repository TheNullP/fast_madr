from http import HTTPStatus

from fast_madr.schemas.user_schema import UserModel

user = UserModel


def test_adicionar_usuario(client):
    response = client.post(
        '/user/create',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'msg': 'success.'}


def test_adicionar_usuario_existente(client, user):
    response = client.post(
        '/user/create',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'User or Email already exists.'}


def test_atualizar_usuario(client, user, access_token):
    response = client.put(
        '/user/update/',
        headers={'Authorization': f'Bearer {access_token["access_token"]}'},
        json={
            'username': 'test_modificated',
            'email': 'modificated@test.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'msg': 'success.'}


def test_atualizar_usuario_nao_encontrado(client, access_token):
    response = client.put(
        '/user/update/2',
        headers={'Authorization': f'Bearer {access_token["access_token"]}'},
        json={
            'username': 'test_modificated',
            'email': 'modificated@test.com',
            'password': 'test',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_deletar_usuario(client, access_token):
    response = client.delete(
        '/user/delete',
        headers={'Authorization': f'Bearer {access_token["access_token"]}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'User deleted.'}


def test_deletar_usuario_nao_autenticado(client):
    response = client.delete('/user/delete')

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}
