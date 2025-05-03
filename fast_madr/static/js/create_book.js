const modal = document.getElementById("book-modal");
const openModal = document.getElementById("open-modal");
const closeModal = document.querySelector(".close");

openModal.addEventListener("click", () => {
  modal.style.display = "block";
})

closeModal.addEventListener("click", () => {
  modal.style.display = "none";
});

// Fecha modal ao clicar fora
window.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});


document.getElementById("book-form").addEventListener("submit", async (e) => {
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
    modal.style.display = "none";

  } catch (error) {
    alert(error)
  }
});
