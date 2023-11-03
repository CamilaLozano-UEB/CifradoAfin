// login.js

// Función para cifrar una cadena con SHA-256
function sha256(str) {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    return crypto.subtle.digest("SHA-256", data).then(buffer => {
        const array = Array.from(new Uint8Array(buffer));
        return array.map(byte => byte.toString(16).padStart(2, "0")).join("");
    });

}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-button").addEventListener("click", function (e) {
        e.preventDefault();

        var username = document.getElementById("login-username").value;
        var password = document.getElementById("login-password").value;
         ip =

        // Cifra la contraseña con SHA-256 antes de enviarla
        sha256(password).then(function (cipheredPassword) {
            // Crea un objeto con los datos a enviar en formato JSON
            var data = {
                username: username,
                password: cipheredPassword

            };
            console.log(cipheredPassword)

            // Realiza una solicitud AJAX para enviar los datos de inicio de sesión al servidor en formato JSON
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/login", true);

            // Configura el encabezado para indicar que se está enviando JSON
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.onreadystatechange = function () {

                if (xhr.readyState === 4 && xhr.status === 200) {
                    console.log(xhr.responseText)
                    var response = JSON.parse(xhr.responseText);
                    if (response.blocked) {
                        alert(response.blocked)

                    } else if (response.success) {
                        // Si la autenticación es exitosa, redirige al usuario a la página deseada
                        window.location.href = "/index";

                    } else {
                        // Si la autenticación falla, muestra un mensaje de error
                        alert("Nombre de usuario o contraseña incorrectos.");
                    }
                }
            };

            var jsonData = JSON.stringify(data);
            xhr.send(jsonData);
        });
    });

});
