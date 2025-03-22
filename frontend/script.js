// Función para registrar usuario en la base de datos
async function registrar() {
    let email = document.getElementById("registroEmail").value.trim();
    let password = document.getElementById("registroPassword").value.trim();

    if (!email || !password) {
        document.getElementById("mensajeRegistro").innerText = "Todos los campos son obligatorios.";
        return;
    }

    try {
        let respuesta = await fetch("http://localhost:5000/registrar_usuario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let resultado = await respuesta.json();
        document.getElementById("mensajeRegistro").innerText = resultado.mensaje;

        if (respuesta.ok) {
            setTimeout(() => window.location.href = "index.html", 2000);
        }
    } catch (error) {
        console.error("Error en el registro:", error);
    }
}

// Función para iniciar sesión
async function login() {
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    if (!email || !password) {
        document.getElementById("mensaje").innerText = "Todos los campos son obligatorios.";
        return;
    }

    try {
        let respuesta = await fetch("http://localhost:5000/iniciar_sesion", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let resultado = await respuesta.json();
        document.getElementById("mensaje").innerText = resultado.mensaje;

        if (respuesta.ok) {
            setTimeout(() => window.location.href = "home.html", 2000);
        }
    } catch (error) {
        console.error("Error en el inicio de sesión:", error);
    }
}

// Función para cerrar sesión
function cerrarSesion() {
    window.location.href = "index.html";
}

// Función para registrar un nuevo evento
document.getElementById("eventoForm")?.addEventListener("submit", async function (event) {
    event.preventDefault();

    let nombre = document.getElementById("nombreEvento").value.trim();
    let fecha = document.getElementById("fechaEvento").value;
    let tiquetes = parseInt(document.getElementById("cantidadTiquetes").value);
    let precio = parseFloat(document.getElementById("precioTiquete").value);

    if (!nombre || !fecha || isNaN(tiquetes) || isNaN(precio) || tiquetes <= 0 || precio <= 0) {
        alert("Por favor, ingrese valores válidos.");
        return;
    }

    try {
        let respuesta = await fetch("http://localhost:5000/agregar_evento", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, fecha, tiquetes, precio })
        });

        let resultado = await respuesta.json();
        alert(resultado.mensaje);

        if (respuesta.ok) {
            document.getElementById("eventoForm").reset();
            let modal = document.getElementById("crearEventoModal");
            if (modal) {
                let modalInstance = bootstrap.Modal.getInstance(modal);
                modalInstance?.hide();
            }
            cargarEventos();
        }
    } catch (error) {
        console.error("Error al agregar evento:", error);
    }
});

// Función para cargar eventos desde la base de datos y mostrarlos en la página
async function cargarEventos() {
    try {
        let respuesta = await fetch("http://localhost:5000/eventos");

        if (!respuesta.ok) throw new Error("Error al obtener eventos");

        let eventos = await respuesta.json();
        let container = document.getElementById("eventosContainer");

        if (!container) return;

        container.innerHTML = "";  // Limpiar contenido antes de recargar

        if (eventos.length === 0) {
            container.innerHTML = "<p>No hay eventos disponibles.</p>";
            return;
        }

        eventos.forEach(evento => {
            let eventoDiv = document.createElement("div");
            eventoDiv.classList.add("evento");

            eventoDiv.innerHTML = `
                <h3>${evento.nombre}</h3>
                <p><strong>Fecha:</strong> ${evento.fecha}</p>
                <p><strong>Boletos disponibles:</strong> <span id="boletos-${evento.id}">${evento.tiquetes}</span></p>
                <p><strong>Precio:</strong> $${Number(evento.precio).toFixed(2)}</p>
                <button onclick="comprarBoleto(${evento.id})" ${evento.tiquetes <= 0 ? "disabled" : ""}>
                    ${evento.tiquetes > 0 ? "Comprar" : "Agotado"}
                </button>
            `;

            container.appendChild(eventoDiv);
        });
    } catch (error) {
        console.error("Error al cargar eventos:", error);
    }
}

// Función para comprar un boleto
async function comprarBoleto(idEvento) {
    try {
        let respuesta = await fetch("http://localhost:5000/comprar_boleto", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: idEvento })
        });

        let resultado = await respuesta.json();
        alert(resultado.mensaje);

        if (respuesta.ok) {
            cargarEventos();  // Recargar eventos para actualizar la cantidad de boletos
        }
    } catch (error) {
        console.error("Error al comprar boleto:", error);
    }
}

// Cargar eventos si estamos en la página de eventos
if (window.location.pathname.includes("eventos.html")) {
    document.addEventListener("DOMContentLoaded", cargarEventos);
}
