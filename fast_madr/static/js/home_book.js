document.addEventListener("DOMContentLoaded", function() {

  const modal = document.getElementById("inf-modal");
  const closeBtn = document.querySelector(".close");
  const modal_container = document.querySelector(".modal-content");

  const modalDownloadLink = document.getElementById("link");
  const modalTitle = document.getElementById('modal-title');
  const modalAuthor = document.getElementById('modal-author');
  const modalYear = document.getElementById('modal-year');
  const modalSinopse = document.getElementById('modal-sinopse');

  document.getElementById("books-container").addEventListener("click", async (e) => {
    const bookElement = e.target.closest(".book");

    if (bookElement) {

      const id_book = bookElement.dataset.id;

      try {
        const response = await fetch(`/page_book?id_book=${id_book}`);

        if (!response.ok) {
          console.error('Erro ao buscar livro: ', response.status);
          return;
        }

        const inf_modal_data = await response.json();


        modalDownloadLink.href = inf_modal_data.url;
        modalTitle.innerText = inf_modal_data.titulo;
        modalAuthor.textContent = `Author: ${inf_modal_data.author}`;
        modalYear.innerText = `Ano: ${inf_modal_data.ano}`;

        modal.style.display = "flex";
        setTimeout(() => {
          modal.classList.add('show')
        }, 10);

      } catch (error) {
        console.error('Erro na requisição: ', error);
      }
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.classList.remove('show');
      setTimeout(() => {
        modal.style.display = "none";
      }, 300);
    });
  } else {
    console.warn('Botao close do modal não encotrado.');

  }

  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.remove('show');
      setTimeout(() => {
        modal.style.display = "none";
      }, 300);
    }
  });

});
