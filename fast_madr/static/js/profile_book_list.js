document.addEventListener("DOMContentLoaded", async function() {
  const access_token = localStorage.getItem("access_token");

  // --- Funções de Fetch e Renderização de Livros ---
  async function fetchUserBooks() {
    try {
      const response = await fetch("/user/info_user", {
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });
      if (!response.ok) {
        console.log("Erro na requisição:", response.status);
        return [];
      }
      const data = await response.json();
      console.log("livros recebidos: ", data.created_books);
      return data.created_books || [];
    } catch (error) {
      console.error("erro ao buscar os livros: ", error);
      return [];
    }
  }

  function renderUserBooks(books) {
    const modalInf = document.getElementById('inf-modal'); // Referência ao modal de informações
    const container = document.getElementById("created_books");
    container.innerHTML = ""; // Limpa antes de adicionar

    books.forEach((book) => {
      const bookElement = document.createElement("div");
      bookElement.classList.add("book");
      bookElement.setAttribute('data-id', book.id);

      // Adiciona o evento de clique a cada livro criado dinamicamente
      bookElement.addEventListener('click', () => {
        console.log(`Livro com ID ${bookElement.dataset.id} clicado!`);

        document.getElementById('modal-title').textContent = book.titulo;
        document.getElementById('modal-author').textContent = `Autor: ${book.author}`;
        document.getElementById('modal-year').textContent = `Ano: ${book.ano}`;
        document.getElementById('modal-sinopse').textContent = book.sinopse;
        // document.getElementById('modal-cover').src = book.cover_url; 
        // document.getElementById('link').href = book.download_url;

        modalInf.style.display = 'flex';
        setTimeout(() => {
          modalInf.classList.add('show');
        }, 10);
      });

      bookElement.innerHTML = `
                <h2>${book.titulo}</h2>
                <p>Autor: ${book.author}</p>
                <p>Ano: ${book.ano}</p>
            `;
      container.appendChild(bookElement);
    });

    const closeEditBookBtn = document.querySelector('.close-edit-book');

    if (closeEditBookBtn) {
      closeEditBookBtn.addEventListener('click', () => {
        modalInf.classList.remove('show');
        setTimeout(() => {
          modalInf.style.display = 'none'; // Fecha o modal
        }, 300)
      });
    } else {
      console.warn("Botão '.close-edit-book' para fechar o modal não encontrado.");
    }

    // Lógica para fechar o modal clicando fora dele (no overlay)
    window.addEventListener('click', (event) => {
      if (event.target === modalInf) { // Verifica se o clique foi no próprio overlay do modal
        modalInf.classList.remove('show');
        setTimeout(() => {
          modalInf.style.display = 'none';
        });
      }
    });
  }

  // --- Chamada inicial para buscar e renderizar os livros ---
  const my_books = await fetchUserBooks();
  renderUserBooks(my_books);
});
