from http import HTTPStatus
from fast_madr.schema import UserModel

user = UserModel


def test_retorno_get(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Hello": "Wold"}


def test_adicionar_usuario(client):
    response = client.post(
        "/user/",
        json={
            "username": "test",
            "email": "test@test.com",
            "password": "test",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "test",
        "email": "test@test.com",
    }


def test_adicionar_usuario_existente(client, user):
    response = client.post(
        "/user/",
        json={
            "username": user.username,
            "email": user.email,
            "password": user.password,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "User already exists."}


def test_atualizar_usuario(client, user):
    response = client.put(
        "/user/1",
        json={
            "username": "test_modificated",
            "email": "modificated@test.com",
            "password": "test",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "test_modificated",
        "email": "modificated@test.com",
    }


def test_atualizar_usuario_nao_encontrado(client):
    response = client.put(
        "/user/1",
        json={
            "username": "test_modificated",
            "email": "modificated@test.com",
            "password": "test",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found."}


def test_deletar_usuario(client, user):
    response = client.delete("/user/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"detail": "User deleted."}


def test_deletar_usuario_nao_encontrado(client, user):
    response = client.delete("/user/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found."}
