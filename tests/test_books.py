from http import HTTPStatus


def test_lista_de_livros(client):
    response = client.get('/read-book')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_criando_livro(client, access_token, user):
    response = client.post(
        '/create_book',
        headers={
            'Authorization': f'Bearer {access_token["access_token"]}',
        },
        json={
            'titulo': 'test',
            'ano': 1999,
            'author': 'Stephen king',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'msg': 'success.'}
