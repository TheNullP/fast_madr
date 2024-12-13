from http import HTTPStatus


def test_lista_de_livros(client):
    response = client.get("/books/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_criando_livro(client, user):
    response = client.post(
        "/book/1/",
        json={
            "titulo": "test",
            "ano": 1999,
            "id_user": 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"titulo": "test", "ano": 1999, "id_user": 1}
