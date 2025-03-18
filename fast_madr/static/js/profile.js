document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("access_token");

    if (!token) {
        // Redireciona para o login caso não tenha token
        window.location.href = "/";
        return;
    }

    try {
        const response = await fetch("/user/info_user", {
            headers: {
                Accept: "application/json",
                Authorization: `Bearer ${token}`, // Adiciona o token ao cabeçalho
            },
        });

        if (!response.ok) {
            throw new Error("Invalid or expired token");
        }

        const data = await response.json(); // Converte a resposta para JSON

        // Atualiza as informações do usuário
        document.getElementById("user-info").innerText = `${data.username}`;
        document.getElementById("number_of_books").innerText = `${data.number_of_books}`;

        if (data.profile_picture) {
            document.getElementById("profile-picture").src = data.profile_picture;
        }

        // Evento de logout
        document.getElementById("logout").addEventListener("click", () => {
            localStorage.removeItem("access_token");
            window.location.href = "/";
        });

    } catch (error) {
        console.error(error);
        alert("Sessão expirada. Faça login novamente.");
        localStorage.removeItem("access_token");
        window.location.href = "/user/login";
    }

    // 💾 Upload de imagem de perfil
    const profilePicture = document.getElementById("profile-picture");
    const uploadPhoto = document.getElementById("upload-photo");

    profilePicture.addEventListener("click", function () {
        uploadPhoto.click();
    });

    uploadPhoto.addEventListener("change", async function (event) {
        if (!event.target.files || event.target.files.length === 0) {
            console.warn("Nenhum arquivo selecionado.");
            return;
        }

        const file = event.target.files[0];

        // Atualiza o preview da imagem antes do upload
        const reader = new FileReader();
        reader.onload = function (e) {
            profilePicture.src = e.target.result;
        };
        reader.readAsDataURL(file);
        uploadPhoto.value = "";  // reseta o input para permitir outra selecao

        // Cria o FormData para enviar a imagem
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/upload/profile-picture/", {
                method: "POST",
                body: formData,
                headers: { Authorization: `Bearer ${token}` }, // Adiciona o token ao envio da imagem
            });

            const data = await response.json();
            console.log("Upload realizado com sucesso:", data);

            if (data.url) {
                profilePicture.src = data.url;
            } else {
                console.warn("Erro ao obter a URL da imagem.");
            }

        } catch (error) {
            console.error("Erro no upload:", error);
            alert("Erro ao enviar a imagem. Tente novamente.");
        }
    });
});

