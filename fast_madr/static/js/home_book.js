const modal = document.getElementById("inf-modal");
const close = document.querySelector(".close");
const modal_container = document.querySelector(".modal-content");

document.getElementById("books-container").addEventListener("click", async (e) => {
  const book = e.target.closest(".book");
  if (book) {
    modal.style.display = "block";

    const id_book = book.dataset.id;

    try {
      const response = await fetch(`/page_book?id_book=${id_book}`);

      if (!response.ok) {
        console.error('Erro ao buscar livro: ', response.status);
        return;
      }

      const inf_modal = await response.json();


      const url = document.getElementById("link");
      const title = document.getElementById('title');
      const author = document.getElementById('author');
      const year = document.getElementById('year');
      const sinopse = document.getElementById('sinopse');



      url.href = inf_modal.url;
      title.innerText = inf_modal.titulo;
      author.innerText = inf_modal.author;
      year.innerText = inf_modal.ano;


    } catch (error) {
      console.error('Erro na requisição: ', error);
    }
  }
});

close.addEventListener("click", () => {
  modal.style.display = "none";
});

window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
})
