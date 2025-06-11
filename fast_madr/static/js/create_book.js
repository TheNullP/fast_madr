window.prepareBookModalForEdit = async function(bookId) {
  const bookModal = document.getElementById('book-modal');
  const bookForm = document.getElementById('book-form');
  const submitButton = document.getElementById('submit-book-form');
  const bookIdInput = document.getElementById('book-id-to-edit');
  // const sinopseInput = document.getElementById('sinopse');
  // const fileCoverInput = document.getElementById('file_cover');
  const fileBookInput = document.getElementById('file_book');

  bookForm.reset();
  // file_cover.value = '';
  fileBookInput.value = '';
  document.getElementById('file_book').value = '';


  bookModal.querySelector('h2').textContent = 'Editar Livro.';

  try {
    const response = await fetch(`/page_book?id_book=${bookId}`)
    if (!response.ok) {
      throw new Error(`Erro ao buscar detalhes do Livro: ${response.status}`);
    }
    const bookData = await response.json(); // provavel ficar como respose.BookList
    console.log("Dados do livro para edição:", bookData);

    //Preencher os campos do Form
    document.getElementById('title').value = bookData.titulo;
    document.getElementById('author').value = bookData.author;
    document.getElementById('year').value = bookData.ano;
    // sinopseInput.value = bookData.sinopse || '';

    bookIdInput.value = bookData.id;
    // submitButton.textContent = 'Salvar Alterações.';

    bookModal.style.display = 'flex';
    setTimeout(() => {
      bookModal.classList.add('show');
    }, 10);

  } catch (error) {
    console.error('Erro ao preparar modal de Edição: ', error);
    alert(`Não foi possivel carregar os dados do livro para Edição: ${error.message}`)
  }
};


// --- FUNÇÃO GLOBAL PARA DELETAR LIVRO ---
// Garante que a função deleteBook também esteja global
window.deleteBook = async function(bookId) {
  const access_token = localStorage.getItem("access_token");

  if (!access_token) {
    alert("Você precisa estar logado para deletar um livro.");
    return;
  }

  if (!confirm(`Tem certeza que deseja deletar o livro (ID: ${bookId})? Esta ação é irreversível.`)) {
    return;
  }

  try {
    const response = await fetch(`/delete_book/${bookId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${access_token}` },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: "Erro desconhecido." }));
      throw new Error(`Erro: ${response.status} - ${errorData.message || response.statusText}`);
    }

    alert("Livro deletado com sucesso!");

    // Recarregar a lista de livros (funções globais)
    if (window.fetchUserBooks && window.renderUserBooks) {
      const updatedBooks = await window.fetchUserBooks();
      window.renderUserBooks(updatedBooks);
    } else {
      console.warn("Funções de renderização de livros não acessíveis. Recarregue a página manualmente.");
    }

    // Fechar o inf-modal se estiver aberto
    const infModal = document.getElementById('inf-modal');
    if (infModal && infModal.classList.contains('show')) {
      infModal.classList.remove("show");
      setTimeout(() => { infModal.style.display = 'none'; }, 300);
    }

  } catch (error) {
    console.error("Erro ao deletar livro:", error);
    alert(`Falha ao deletar livro: ${error.message}`);
  }
};


document.addEventListener('DOMContentLoaded', function() {

  const bookModal = document.getElementById("book-modal");
  const openModalBtn = document.getElementById('open-modal');
  const closeModalBtn = document.querySelector(".close");
  const bookForm = document.getElementById('book-form');
  const submitButton = document.getElementById("submit-book-form");
  const bookIdInput = document.getElementById("book-id-to-edit");

  if (openModalBtn) {
    openModalBtn.addEventListener("click", () => {
      bookModal.style.display = "flex";
      setTimeout(() => {
        bookModal.classList.add('show');
      }, 10);
      bookForm.reset();
      fileBookInput.value = '';
      // document.getElementById('file_cover').value = '';
      bookIdInput.value = "";
      submitButton.textContent = "Adicionar";
      bookModal.querySelector('h2').textContent = "Adicionar Novo Livro.";
    });
  } else {
    console.warn('Elemento (Novo Livro) não encontrado.')
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", () => {
      bookModal.classList.remove('show');
      setTimeout(() => {
        bookModal.style.display = 'none';
      }, 300);
    });
  } else {
    console.warn('Elemento (Fechar) não encontrado.')
  }

  // Fecha modal ao clicar fora
  window.addEventListener("click", (e) => {
    if (bookModal && e.target === bookModal) {
      bookModal.classList.remove('show');
      setTimeout(() => {
        bookModal.style.display = "none";
      }, 300);
    }
  });



  if (bookForm) {

    bookForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const bookId = bookIdInput.value;
      const isEditing = !!bookId;
      console.log('ESSE É O RESULTADO DO BOLEANO PARA EDITA: ', isEditing);

      const title = document.getElementById("title").value;
      const author = document.getElementById("author").value;
      const year = parseInt(document.getElementById("year").value, 10);
      const fileBookInput = document.getElementById("file_book");
      const access_token = localStorage.getItem("access_token");

      // const file = fileBookInput.files[0];


      const formData = new FormData();
      formData.append("book_id", bookId);
      formData.append("book_title", title);
      formData.append("book_author", author);
      formData.append("book_year", year);
      // formData.append("book_sinopse", sinopse);


      if (fileBookInput.files && fileBookInput.files.length > 0) {
        formData.append("book_file", fileBookInput.files[0]);
        console.log("DEBUG: Novo arquivo de livro selecionado e adicionado ao FormData.");
      }
      // if (fileCoverInput.files && fileCoverInput.files.length > 0) {
      //   formData.append('cover_file', fileCoverInput.files[0]);
      // }

      const method = isEditing ? "PUT" : "POST";
      const url = isEditing ? `/book/update` : "/create_book";

      try {

        const response = await fetch(url, {
          method: method,
          headers: { "Authorization": `Bearer ${access_token}` },
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ message: "Erro desconhecido." }));
          throw new Error(`Erro na requisição: ${response.status} - ${errorData.message || response.statusText}`);
        }

        alert(isEditing ? "Livro atualizado com sucesso!" : "Livro adicionado com sucesso!");

        bookModal.classList.remove('show');
        setTimeout(() => { bookModal.style.display = "none"; }, 300);


        // Recarrega a lista de livros (usando as funções globais)
        if (window.fetchUserBooks && window.renderUserBooks) {
          const updatedBooks = await window.fetchUserBooks();
          window.renderUserBooks(updatedBooks);
        } else {
          console.warn("Funções de renderização de livros não acessíveis. Recarregue a página manualmente.");
        }

        bookForm.reset(); // Limpa o formulário
        bookIdInput.value = ""; // Limpa o ID oculto
        submitButton.textContent = "Adicionar"; // Volta o texto do botão
        bookModal.querySelector('h2').textContent = "Adicionar Novo Livro"; // Volta o título do modal


      } catch (error) {
        console.error("Erro na operação do livro:", error);
        alert(`Falha na operação: ${error.message}`);
      }
    });
  } else {
    console.warn('Elemento (book-form) não encontrado.');
  }
}); 
