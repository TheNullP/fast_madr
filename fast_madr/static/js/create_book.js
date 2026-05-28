window.prepareBookModalForEdit = async function (bookId) {
	const bookModal = document.getElementById("book-modal");
	const bookForm = document.getElementById("book-form");
	const submitButton = document.getElementById("submit-book-form");
	const bookIdInput = document.getElementById("book-id-to-edit");

	// Campos de formulário (apenas se existirem no HTML, para evitar erros se estiverem comentados)
	const titleInput = document.getElementById("title");
	const authorInput = document.getElementById("author");
	const yearInput = document.getElementById("year");
	// const sinopseInput = document.getElementById('sinopse');
	const fileCoverInput = document.getElementById("file_cover");
	const fileBookInput = document.getElementById("file_book");

	bookForm.reset();
	if (fileCoverInput) fileCoverInput.value = "";
	if (fileBookInput) fileBookInput.value = "";

	if (bookModal.querySelector("h2")) {
		bookModal.querySelector("h2").textContent = "Editar Livro";
	}

	try {
		const response = await fetch(`/page_book?id_book=${bookId}`);
		if (!response.ok) {
			throw new Error(`Erro ao buscar detalhes do Livro: ${response.status}`);
		}
		const bookData = await response.json();

		//  Preencher os campos do formulário com os dados do livro
		if (titleInput) titleInput.value = bookData.titulo || "";
		if (authorInput) authorInput.value = bookData.author || "";
		if (yearInput) yearInput.value = bookData.ano || "";

		if (bookIdInput) {
			bookIdInput.value = bookData.id;
		} else {
			console.error(
				"ERRO: bookIdInput (#book-id-to-edit) não encontrado em prepareBookModalForEdit.",
			);
		}
		submitButton.textContent = "Salvar Alterações.";

		if (bookModal) {
			bookModal.style.display = "flex";
			setTimeout(() => {
				bookModal.classList.add("show");
			}, 10);
		}
	} catch (error) {
		console.error("Erro ao preparar modal de Edição: ", error);
		alert(
			`Não foi possível carregar os dados do livro para Edição: ${error.message}`,
		);
	}
};

window.deleteBook = async function (bookId) {
	const access_token = localStorage.getItem("access_token");

	if (!access_token) {
		alert("Você precisa estar logado para deletar um livro.");
		return;
	}

	try {
		const response = await fetch(`/delete_book?book_id=${bookId}`, {
			method: "DELETE",
			headers: { Authorization: `Bearer ${access_token}` },
		});

		if (!response.ok) {
			const errorData = await response
				.json()
				.catch(() => ({ message: "Erro desconhecido." }));
			throw new Error(
				`Erro: ${response.status} - ${errorData.message || response.statusText}`,
			);
		}

		alert("Livro deletado com sucesso!");

		if (window.fetchUserBooks && window.renderUserBooks) {
			const updatedBooks = await window.fetchUserBooks();
			window.renderUserBooks(updatedBooks);
		} else {
			console.warn(
				"Funções de renderização de livros não acessíveis. Recarregue a página manualmente.",
			);
		}

		const infModal = document.getElementById("inf-modal");
		if (infModal && infModal.classList.contains("show")) {
			infModal.classList.remove("show");
			setTimeout(() => {
				infModal.style.display = "none";
			}, 300);
		}
	} catch (error) {
		console.error("Erro ao deletar livro:", error);
		alert(`Falha ao deletar livro: ${error.message}`);
	}
};

document.addEventListener("DOMContentLoaded", function () {
	const bookModal = document.getElementById("book-modal");
	const openModalBtn = document.getElementById("open-modal");
	const closeModalBtn = bookModal ? bookModal.querySelector(".close") : null; // Verificação de existência
	const bookForm = document.getElementById("book-form");
	const submitButton = document.getElementById("submit-book-form");
	const bookIdInput = document.getElementById("book-id-to-edit");

	const titleInput = document.getElementById("title");
	const authorInput = document.getElementById("author");
	const yearInput = document.getElementById("year");
	const sinopseInput = document.getElementById("sinopse");
	const fileCoverInput = document.getElementById("file_cover");
	const fileBookInput = document.getElementById("file_book");

	if (openModalBtn) {
		openModalBtn.addEventListener("click", () => {
			if (bookModal) {
				bookModal.style.display = "flex";
				setTimeout(() => {
					bookModal.classList.add("show");
				}, 10);
			}
			if (bookForm) bookForm.reset();
			if (fileCoverInput) fileCoverInput.value = "";
			if (bookIdInput) bookIdInput.value = "";
			if (submitButton) submitButton.textContent = "Adicionar";
			if (bookModal && bookModal.querySelector("h2"))
				bookModal.querySelector("h2").textContent = "Adicionar Novo Livro.";
		});
	} else {
		console.warn('Elemento "open-modal" (botão Novo Livro) não encontrado.');
	}

	if (closeModalBtn) {
		closeModalBtn.addEventListener("click", () => {
			if (bookModal) {
				bookModal.classList.remove("show");
				setTimeout(() => {
					bookModal.style.display = "none";
				}, 300);
			}
		});
	} else {
		console.warn(
			'Elemento ".close" (botão de fechar do book-modal) não encontrado.',
		);
	}

	window.addEventListener("click", (e) => {
		if (bookModal && e.target === bookModal) {
			bookModal.classList.remove("show");
			setTimeout(() => {
				bookModal.style.display = "none";
			}, 300);
		}
	});

	if (bookForm) {
		bookForm.addEventListener("submit", async (e) => {
			e.preventDefault();

			const bookId = bookIdInput ? bookIdInput.value : "";
			const isEditing = !!bookId;

			const title = titleInput ? titleInput.value : "";
			const author = authorInput ? authorInput.value : "";
			const year = yearInput ? parseInt(yearInput.value, 10) : 0;
			const sinopse = sinopseInput ? sinopseInput.value : "";

			const access_token = localStorage.getItem("access_token");

			const formData = new FormData();

			if (bookIdInput) formData.append("book_id", bookId);
			if (titleInput) formData.append("book_title", title);
			if (authorInput) formData.append("book_author", author);
			if (yearInput) formData.append("book_year", year);

			if (fileBookInput && fileBookInput.files.length > 0) {
				formData.append("book_file", fileBookInput.files[0]);
			}

			if (fileCoverInput && fileCoverInput.files.length > 0) {
				formData.append("book_cover", fileCoverInput.files[0]);
			}

			const method = isEditing ? "PUT" : "POST";
			const url = isEditing ? `/book/update` : "/create_book";

			try {
				const response = await fetch(url, {
					method: method,
					headers: { Authorization: `Bearer ${access_token}` },
					body: formData,
				});

				if (!response.ok) {
					const errorData = await response
						.json()
						.catch(() => ({ message: "Erro desconhecido." }));
					throw new Error(
						`Erro na requisição: ${response.status} - ${errorData.message || response.statusText}`,
					);
				}

				alert(
					isEditing
						? "Livro atualizado com sucesso!"
						: "Livro adicionado com sucesso!",
				);

				if (bookModal) bookModal.classList.remove("show");
				if (bookModal)
					setTimeout(() => {
						bookModal.style.display = "none";
					}, 300);

				if (window.fetchUserBooks && window.renderUserBooks) {
					const updatedBooks = await window.fetchUserBooks();
					window.renderUserBooks(updatedBooks);
				} else {
					console.warn(
						"Funções de renderização de livros não acessíveis. Recarregue a página manualmente.",
					);
				}

				if (bookForm) bookForm.reset();
				if (bookIdInput) bookIdInput.value = "";
				if (submitButton) submitButton.textContent = "Adicionar";
				if (bookModal && bookModal.querySelector("h2"))
					bookModal.querySelector("h2").textContent = "Adicionar Novo Livro";
			} catch (error) {
				alert(`Falha na operação: ${error.message}`);
			}
		});
	} else {
		console.warn("Elemento (book-form) não encontrado.");
	}
});
