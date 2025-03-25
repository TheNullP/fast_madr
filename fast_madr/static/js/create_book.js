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


document.getElementById("book-form").addEventListener("submit",  async (e) => {
  e.preventDefault();

  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;
  const year = parseInt(document.getElementById("year").value, 10);
  const access_token = localStorage.getItem("access_token");

  try {

    const response = await fetch("/create_book",{
      method: "POST",
      headers: {
        "Authorization": `Bearer ${access_token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "titulo": title,
        "ano": year,
        "author": author
      }),
    })

    if (!response.ok){
      throw new Error(`Erro na requisição: ${response.status}`)
    }
    alert("success.")
    modal.style.display = "none";

  } catch (error){
    alert(error)   
  }
});
