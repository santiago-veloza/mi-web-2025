// script.js
function registrar() {
    let email = document.getElementById("registroEmail").value;
    let password = document.getElementById("registroPassword").value;

    if (email === "" || password === "") {
        document.getElementById("mensajeRegistro").innerText = "Todos los campos son obligatorios";
        return;
    }

    
    localStorage.setItem("usuario", JSON.stringify({ email, password }));
    document.getElementById("mensajeRegistro").innerText = "Registro exitoso. Redirigiendo...";

    setTimeout(() => {
        window.location.href = "index.html";
    }, 1000);
}


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


        localStorage.setItem("sesion", "activa");

        setTimeout(() => {
            window.location.href = "home.html";
        }, 1000);
    } else {
        document.getElementById("mensaje").innerText = "Credenciales incorrectas.";
    }
}


function verificarSesion() {
    if (!localStorage.getItem("sesion")) {
        window.location.href = "index.html";
    }
}


function cerrarSesion() {
    localStorage.removeItem("sesion");
    window.location.href = "index.html";
}


if (window.location.pathname.includes("home.html")) {
    verificarSesion();
}

document.getElementById("eventoForm").addEventListener("submit", async function(event) {
    event.preventDefault();  

    const nombre = document.getElementById("nombreEvento").value;
    const fecha = document.getElementById("fechaEvento").value;
    const tiquetes = document.getElementById("cantidadTiquetes").value;
    const precio = document.getElementById("precioTiquete").value;

    try {
        const respuesta = await fetch("http://127.0.0.1:5000/agregar_evento", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                nombre, 
                fecha, 
                tiquetes, 
                precio 
            })
        });

        const resultado = await respuesta.json();


        alert(resultado.mensaje || resultado.error);

        
        if (respuesta.ok) {
            document.getElementById("eventoForm").reset();
            var modal = bootstrap.Modal.getInstance(document.getElementById("crearEventoModal"));
            modal.hide();
        }

    } catch (error) {
        console.error("Error al enviar la solicitud:", error);
        alert("❌ Hubo un error al conectar con el servidor.");
    }
});
