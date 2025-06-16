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
    // console.log("livros recebidos: ", data.created_books);
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


  // GUARDA O ID DO LIVRO NO BOTÃO ED/DEL DENTRO DO 'inf-modal'
  const editBtn = document.getElementById('editBtn');
  const deleteBtn = document.getElementById('deleteBtn');


  books.forEach((book) => {
    const bookElement = document.createElement("div");
    bookElement.classList.add("book");
    bookElement.setAttribute('data-id', book.id);


    // Adiciona o evento de clique a cada livro criado dinamicamente
    bookElement.addEventListener('click', () => {

      document.getElementById('modal-title').textContent = book.titulo;
      document.getElementById('modal-author').textContent = `Autor: ${book.author}`;
      document.getElementById('modal-year').textContent = `Ano: ${book.ano}`;
      document.getElementById('modal-sinopse').textContent = book.sinopse;
      document.getElementById('link').href = book.file_book;
      // document.getElementById('modal-cover').src = book.cover_url; 

      if (editBtn) {
        editBtn.dataset.bookId = book.id;
      }
      if (deleteBtn) {
        deleteBtn.dataset.bookId = book.id;
      }

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
}



document.addEventListener('DOMContentLoaded', async function() {
  const access_token = localStorage.getItem("access_token");
  const modalInf = document.getElementById("inf-modal");

  // Botoes para Editar e Deletar o livro atual
  const editBtnInInfModal = document.getElementById('editBtn');
  const deleteBtnInInfModal = document.getElementById('deleteBtn');


  const closeEditBookBtn = document.querySelector('.close-edit-book');
  if (closeEditBookBtn) {
    closeEditBookBtn.addEventListener('click', () => {
      if (modalInf) {
        modalInf.classList.remove('show');
        setTimeout(() => { modalInf.style.display = 'none'; }, 300);
      }
    });
  } else {
    console.warn("Botão '.close-edit-book' para fechar o modal não encontrado.");
  }


  // Lógica para fechar o modal clicando fora dele (no overlay)
  window.addEventListener('click', (event) => {
    if (modalInf && event.target === modalInf) { // Verifica se o clique foi no próprio overlay do modal
      modalInf.classList.remove('show');
      setTimeout(() => { modalInf.style.display = 'none'; }, 300);
    }
  });

  if (editBtnInInfModal) {
    editBtnInInfModal.addEventListener('click', async () => {
      const bookIdToEdit = editBtnInInfModal.dataset.bookId;

      if (!bookIdToEdit) {
        console.error('Erro: ID do livro para editar não encontrado no dataset do botão.');
        alert('Erro: ID do livro não disponível para edição. Tente novamente.');
        return;
      }

      // Fecha o inf-modal (o modal de visualização)
      if (modalInf) {
        modalInf.classList.remove("show");
        setTimeout(() => { modalInf.style.display = 'none'; }, 300);
      }

      // Chama a função global para preparar o book-modal para edição
      if (typeof window.prepareBookModalForEdit === 'function') {
        await window.prepareBookModalForEdit(bookIdToEdit);
      } else {
        console.error("Função 'window.prepareBookModalForEdit' não encontrada. Verifique o escopo em create_book.js.");
        alert("Erro: A função de edição não está disponível. Contate o suporte.");
      }
    });
  }


  if (deleteBtnInInfModal) {
    deleteBtnInInfModal.addEventListener('click', async () => {
      const bookIdToDelete = deleteBtnInInfModal.dataset.bookId;

      if (!bookIdToDelete) {
        console.error('Erro: ID do livro para deletar não encontrado no dataset do botão.');
        alert('Erro: ID do livro não disponível para deleção. Tente novamente.');
        return;
      }

      if (confirm(`Tem certeza que deseja deletar este livro? Esta ação é irreversível.`)) {
        if (typeof window.deleteBook === 'function') {
          await window.deleteBook(bookIdToDelete);
        } else {
          console.error("Função 'window.deleteBook' não encontrada.");
          alert("Erro: A função de deleção não está disponível. Contate o suporte.");
        }
      }
    });
  }

  // --- Chamada inicial para buscar e renderizar os livros ---
  const my_books = await fetchUserBooks();
  renderUserBooks(my_books);
});
