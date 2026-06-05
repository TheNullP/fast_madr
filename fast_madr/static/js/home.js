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
	container.innerHTML = "";

	books.forEach((book) => {
		const bookElement = document.createElement("div");
		bookElement.classList.add("book");

		bookElement.setAttribute("data-id", book.id);
		bookElement.setAttribute("data-cover", book.book_cover);

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

	for (let i = 1; i <= totalPages; i++) {
		const button = document.createElement("button");
		button.textContent = i;
		button.disabled = i === currentPage;
		button.addEventListener("click", () => loadBooks(i));
		paginationContainer.appendChild(button);
	}
}

async function loadBooks(page = 1) {
	const perPage = 12;
	const { books, total_books } = await fetchBooks(page, perPage);
	renderBooks(books);

	const totalPages = Math.ceil(total_books / perPage);
	renderPagination(page, totalPages);
}

document.addEventListener("DOMContentLoaded", () => {
	loadBooks();

	if (typeof lucide !== "undefined") {
		lucide.createIcons();
	}

	const btn_search = document.getElementById("search-icon");
	const inpt_search = document.getElementById("input-search");

	if (btn_search && inpt_search) {
		btn_search.addEventListener("click", async (e) => {
			const queryValue = inpt_search.value.trim();

			if (!queryValue) {
				alert("Por favor, digite um termo para buscar.");
				return;
			}

			try {
				const response = await fetch(
					`/search?q=${encodeURIComponent(queryValue)}`,
					{
						method: "GET",
					},
				);

				if (!response.ok) {
					const err = await response.json();
					alert(err.message || "Erro ao realizar busca.");
					return;
				}

				const data = await response.json();
				renderBooks(data.books);

				const totalPages = Math.ceil(data.total_books / 12);
				renderPagination(1, totalPages);
			} catch (error) {
				console.error("Erro na requisição de busca:", error);
			}
		});
	}
});
