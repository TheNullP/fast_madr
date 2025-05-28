document.addEventListener('DOMContentLoaded', function() {

  const bookModal = document.getElementById("book-modal");
  const openModalBtn = document.getElementById('open-modal');
  const closeModalBtn = document.querySelector(".close");

  if (openModalBtn) {
    openModalBtn.addEventListener("click", () => {
      bookModal.style.display = "flex";

      setTimeout(() => {
        bookModal.classList.add('show');
      }, 10);
    });
  } else {
    console.warn('Elemento (Novo Livro) não encontrado.')
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", () => {
      bookModal.style.display = "none";

      setTimeout(() => {
        bookModal.style.display = 'none';
      }, 300);
    });
  } else {
    console.warn('Elemento (Fechar) não encontrado.')
  }

  // Fecha modal ao clicar fora
  window.addEventListener("click", (e) => {
    if (e.target === modal) {
      bookModal.classList.remove('show');
      setTimeout(() => {
        bookModal.style.display = "none";
      }, 300)
    }
  });


  const bookForm = document.getElementById('book-form');

  if (bookForm) {

    bookForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const title = document.getElementById("title").value;
      const author = document.getElementById("author").value;
      const year = parseInt(document.getElementById("year").value, 10);
      const access_token = localStorage.getItem("access_token");
      const fileInput = document.getElementById("file_book");

      const file = fileInput.files[0];

      if (!file) {
        alert("Selecione um Arquivo.");
        return;
      }

      console.log(file.name)

      const formData = new FormData();
      formData.append("file", file);
      formData.append("titulo", title);
      formData.append("ano", year);
      formData.append("author", author);

      try {

        const response = await fetch("/create_book", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${access_token}`,
            // "Content-Type": "application/json"
          },
          body: formData,
        })

        if (!response.ok) {
          throw new Error(`Erro na requisição: ${response.status}`)
        }
        alert("success.")
        bookModal.style.display = "none";

        bookModal.classList.remove('show');
        setTimeout(() => {
          bookModal.style.display = none;
        }, 300)

        this.location.reload()
        bookForm.reset();

      } catch (error) {
        alert(error)
      }
    });
  } else {
    console.warn('Elemento (book-form) não encontrado.');
  }
}); 
