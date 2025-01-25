async function fetchBooks(page = 1, perPage = 10) {
	try {
		const response = await fetch(`/books?page=${page}&per_page=${perPage}`);
		if (!response.ok) throw new Error("Erro ao buscar livros.");
		return await response.json();
	} catch (error) {
		console.error(error);
		return { books: [], total_books: 0 };
	}
}

function renderBooks(books) {
	const container = document.getElementById("books-container");
	container.innerHTML = ""; // limpa o container
	books.forEach((book) => {
		const bookElement = document.createElement("div");
		bookElement.classList.add("book");
		bookElement.innerHTML = `
      <h2>${book.titulo}</h2>
      <p>Autor: ${book.author}</p>
      <p>Ano: ${book.ano}</p>
    `;

		container.appendChild(bookElement);
	});
}

function renderPagination(currentPage, totalPages) {
	const paginationContainer = document.getElementById("pagination");
	paginationContainer.innerHTML = "";

	for (let i = 1; i < totalPages; i++) {
		const button = document.createElement("button");
		button.textContent = i;
		button.disabled = i === currentPage;
		button.addEventListener("click", () => loadBooks(i)); //recarregar os livros ao clicar
		paginationContainer.appendChild(button);
	}
}

async function loadBooks(page = 1) {
	const perPage = 2;
	const { books, total_books } = await fetchBooks(page, perPage);
	renderBooks(books);

	const totalPages = Math.ceil(total_books / perPage);
	renderPagination(page, total_books);
}

// Inicializa a pagina ao carregar o DOM
document.addEventListener("DOMContentLoaded", () => {
	loadBooks();
});
