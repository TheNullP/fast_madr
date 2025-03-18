const modal = document.getElementById("book-modal");
const openModal = document.getElementById("open-modal");
const closeModal = document.querySelector(".close");

openModal.addEventListener("click", () =>{
  modal.style.display = "block";
});

closeModal.addEventListener("click", () =>{
  modal.style.display = "none";
});

// Fecha modal ao clicar fora
window.addEventListener("click", (e) =>{
  if (e.target === modal){
    modal.style.display = "none";
  }
});

document.getElementById("book-form").addEventListener("submit", (e) =>{
  e.preventDefault();

  alert("Livro Adicionado!")
  modal.style.display = "none";
})
