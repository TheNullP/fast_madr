document.addEventListener("DOMContentLoaded", () => {

	document
		.getElementById("registerForm")
		.addEventListener("submit", async (event) => {
			event.preventDefault();

			const username = document.getElementById("username").value.toLowerCase();
			const email = document.getElementById("email").value;
			const password = document.getElementById("password").value;

			try {
				const response = await fetch("/user/create", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						username: username,
						email: email,
						password: password
					})
				});
				if (response.ok) {
					const data = await response.json();
					console.log(data);
					alert(data["msg"]);
					window.location.href = "/";
				} else {
					const errorData = await response.json();
					console.error("Error: ", errorData);
					alert(errorData["detail"]);
				}
			} catch (error) {
				console.log("Ferrou cambada");
			}
		});
})
