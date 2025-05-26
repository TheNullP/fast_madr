document.addEventListener("DOMContentLoaded", async function() {
  const access_token = localStorage.getItem("access_token");
  console.log(access_token);
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
    const modal_edit_book = document.getElementById('inf-modal');
    const container = document.getElementById("created_books");
    container.innerHTML = "";
    books.forEach((book) => {
      const bookElement = document.createElement("div");
      bookElement.classList.add("book");

      bookElement.setAttribute('data-id', book.id);
      bookElement.addEventListener('click', () => {

        modal_edit_book.style.display = 'block';
      });


      bookElement.innerHTML = `
      <h2>${book.titulo}</h2>
      <p>Autor: ${book.author}</p>
      <p>Ano: ${book.ano}</p>
      `;
      container.appendChild(bookElement);
    });
  }

  const my_books = await fetchUserBooks();
  renderUserBooks(my_books);


});



// // fechar modal do livro criado
const close_edit_book = document.querySelector('.close-edit-book');
const modal_edit_book = document.getElementById('inf-modal');

close_edit_book.addEventListener('click', () => {

  modal_edit_book.style.display = "none";
});
