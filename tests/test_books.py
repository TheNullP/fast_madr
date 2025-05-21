from http import HTTPStatus


def test_lista_de_livros(client):
    response = client.get('/read-book')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_livro_ja_criado(client, access_token, book, user):
    response = client.post(
        '/create_book',
        headers={
            'Authorization': f'Bearer {access_token["access_token"]}',
        },
        data={
            'titulo': 'test',
            'ano': 1999,
            'author': 'test',
            'id_user': book.id_user,
        },
        files={
            'file': open(
                '/home/marcos/Documentos/computer_science/repositorios/FastApi/fast_madr/fast_madr/static/image/default.png',
                'rb',
            )
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Book already exists.'}
