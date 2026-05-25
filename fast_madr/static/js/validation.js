document
	.getElementById("loginForm")
	.addEventListener("submit", async (event) => {
		event.preventDefault();

		const username = document
			.getElementById("username")
			.value.toLowerCase()
			.trim();
		const password = document.getElementById("password").value;
		const errorDisplay = document.getElementById("errorMessage");

		// Limpa mensagens de erro anteriores
		errorDisplay.innerText = "";

		try {
			const response = await fetch("/user/token", {
				method: "POST",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded",
				},
				body: new URLSearchParams({ username, password }),
			});

			if (!response.ok) {
				errorDisplay.innerText =
					"Usuário ou senha incorretos. Verifique os dados.";
				return;
			}

			const data = await response.json();
			const token = data.access_token;
			const user = { name: username };

			localStorage.setItem("loggedUser", JSON.stringify(user));
			localStorage.setItem("access_token", token);

			window.location.href = "/user/profile";
		} catch (error) {
			console.error("Erro ao fazer login:", error);
			errorDisplay.innerText = "Falha na conexão. Tente novamente mais tarde.";
		}
	});

document.getElementById("register").addEventListener("click", () => {
	window.location.href = "/user/register";
});
