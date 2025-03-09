// Función para registrar usuario en la base de datos
async function registrar() {
    let email = document.getElementById("registroEmail").value;
    let password = document.getElementById("registroPassword").value;

    if (email === "" || password === "") {
        document.getElementById("mensajeRegistro").innerText = "Todos los campos son obligatorios";
        return;
    }

    try {
        let respuesta = await fetch("http://127.0.0.1:5000/registrar_usuario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let data = await respuesta.json();
        document.getElementById("mensajeRegistro").innerText = data.mensaje;

        if (respuesta.ok) {
            setTimeout(() => {
                window.location.href = "index.html"; // Redirige al login
            }, 1000);
        }
    } catch (error) {
        console.error("❌ Error en el registro:", error);
        alert("Hubo un problema con el servidor.");
    }
}

// Función para iniciar sesión verificando en la base de datos
async function login() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    try {
        let respuesta = await fetch("http://127.0.0.1:5000/iniciar_sesion", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let data = await respuesta.json();
        document.getElementById("mensaje").innerText = data.mensaje;

        if (respuesta.ok) {
            localStorage.setItem("sesion", email); // Guardar sesión
            setTimeout(() => {
                window.location.href = "home.html"; // Redirigir al home
            }, 1000);
        }
    } catch (error) {
        console.error("❌ Error al iniciar sesión:", error);
        alert("Hubo un problema con el servidor.");
    }
}

// Verificar si hay sesión activa antes de cargar home.html
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

// Si está en home.html, verificar sesión
if (window.location.pathname.includes("home.html")) {
    verificarSesion();
}

// Función para agregar eventos a la base de datos
document.getElementById("eventoForm").addEventListener("submit", async function(event) {
    event.preventDefault();  

    const nombre = document.getElementById("nombreEvento").value;
    const fecha = document.getElementById("fechaEvento").value;
    const tiquetes = document.getElementById("cantidadTiquetes").value;
    const precio = document.getElementById("precioTiquete").value;

    try {
        const respuesta = await fetch("http://127.0.0.1:5000/agregar_evento", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
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
