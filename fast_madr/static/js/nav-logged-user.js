function loggedUser() {
	const user = JSON.parse(localStorage.getItem("loggedUser"));
	return user;
}

function nav_logged() {
	const user = loggedUser();
	const token = localStorage.getItem("access_token");

	if (user && token) {
		document.getElementById("nav-login").innerHTML =
			`<a href="/user/profile"> ${user.name}</a>`;
	} else {
		document.getElementById("nav-login").innerHTML =
			'<a href="/user/login">Login</a>';
	}
}
const home = document.getElementById("home");
document.addEventListener("DOMContentLoaded", () => {
	nav_logged();

	lucide.createIcons();
});

home.addEventListener("click", async (e) => {
	e.preventDefault();

	window.location.href = "/";
});
