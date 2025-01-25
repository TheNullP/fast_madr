const token = localStorage.getItem("access_token");

if (!token) {
	//redireciona para o login caso nao tenha token
	window.location.href = "/";
} else {
	fetch("/user/info_user", {
		headers: {
			accept: "application/json",
			Authorization: `Bearer ${token}`, // add o token ao cabecalho de auth
		},
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error("Invalid or expired token");
			}
			return response.json(); // converte a responsta para JSON
		})
		.then((data) => {
			//info do usuario
			document.getElementById(
				"user-info",
			).innerText = `Bem-vindo, Usuário ${data.username}`;
		})
		.catch((error) => {
			console.error(error);
			alert("Session expired. Log in again.");
			window.location.href = "/";
		});
}
