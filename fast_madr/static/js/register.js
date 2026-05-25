document.addEventListener("DOMContentLoaded", () => {
	document
		.getElementById("registerForm")
		.addEventListener("submit", async (event) => {
			event.preventDefault();

			const username = document
				.getElementById("username")
				.value.toLowerCase()
				.trim();
			const email = document.getElementById("email").value.trim();
			const password = document.getElementById("password").value;
			const errorDisplay = document.getElementById("errorMessage");

			errorDisplay.innerText = "";

			try {
				const response = await fetch("/user/create", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ username, email, password }),
				});

				const data = await response.json();

				if (response.ok) {
					alert(data.msg || "Cadastro realizado com sucesso!");
					window.location.href = "/user/login"; // Redireciona para o login
				} else {
					console.error("Erro no cadastro:", data);
					errorDisplay.innerText =
						data.detail || "Falha ao criar conta. Tente outro usuário.";
				}
			} catch (error) {
				console.error("Erro na requisição:", error);
				errorDisplay.innerText = "Erro ao conectar com o servidor.";
			}
		});
});
