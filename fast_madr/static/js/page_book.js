const modal = document.getElementById("inf-modal");
const close = document.querySelector(".close");
const modal_container = document.querySelector(".modal-content");

document.getElementById("books-container").addEventListener("click", (e) => {
  const book = e.target.closest(".book");
  if (book) {
    modal.style.display = "block";
    console.log(book);

    const title = document.getElementById("title");
    title.innerText = book.dataset.title;
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
