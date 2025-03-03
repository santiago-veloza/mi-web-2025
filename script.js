//script.js
// Función para registrar un usuario
function registrar() {
    let email = document.getElementById("registroEmail").value;
    let password = document.getElementById("registroPassword").value;

    if (email === "" || password === "") {
        document.getElementById("mensajeRegistro").innerText = "Todos los campos son obligatorios";
        return;
    }

    // Guardar usuario en localStorage
    localStorage.setItem("usuario", JSON.stringify({ email, password }));
    document.getElementById("mensajeRegistro").innerText = "Registro exitoso. Redirigiendo...";
    
    setTimeout(() => {
        window.location.href = "index.html";
    }, 1000);
}

// Función para iniciar sesión
function login() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let usuario = JSON.parse(localStorage.getItem("usuario"));

    if (!usuario) {
        document.getElementById("mensaje").innerText = "No hay usuarios registrados.";
        return;
    }

    if (email === usuario.email && password === usuario.password) {
        document.getElementById("mensaje").innerText = "Inicio de sesión exitoso. Redirigiendo...";
        
        // Guardar sesión iniciada
        localStorage.setItem("sesion", "activa");

        setTimeout(() => {
            window.location.href = "home.html";
        }, 1000);
    } else {
        document.getElementById("mensaje").innerText = "Credenciales incorrectas.";
    }
}

// Función para verificar si hay sesión iniciada
function verificarSesion() {
    if (!localStorage.getItem("sesion")) {
        window.location.href = "index.html";
    }
}

// Función para cerrar sesión
function cerrarSesion() {
    localStorage.removeItem("sesion");
    window.location.href = "index.html";
}

// Verificar si el usuario está en home.html y no tiene sesión
if (window.location.pathname.includes("home.html")) {
    verificarSesion();
}
