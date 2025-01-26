document.getElementById("logout").addEventListener("click", () => {
	localStorage.removeItem("loggedUser");
	window.location.href = "/";
});
