document
	.getElementById("loginForm")
	.addEventListener("submit", async (event) => {
		event.preventDefault();

		const username = document.getElementById("username").value;
		const password = document.getElementById("password").value;

		try {
			const response = await fetch("/user/token", {
				method: "POST",
				headers: {
					// Define o tipo de dados enviado
					"Content-Type": "application/x-www-form-urlencoded",
				},
				// Enviar os dados no formato correto
				body: new URLSearchParams({ username, password }),
			});

			if (!response.ok) {
				alert("Login falhou. Verifique Username ou Senha.");
				return;
			}

			const data = await response.json(); //converte resposta da API em JSON
			const token = data.access_token; //pega o token retornado pela API

			localStorage.setItem("access_token", token); // Armazena token no localStorage

			window.location.href = "/user/profile";
		} catch (error) {
			console.error("Erro ao fazer login:", error);
			alert("Ocorreu um erro ao tentar fazer login.");
		}
	});
