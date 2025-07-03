const API_URL = "http://127.0.0.1:8000";

// Detectar grupo desde la URL
window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const grupoId = params.get("grupo");

  if (grupoId) {
    document.getElementById("grupoId").value = grupoId;
    document.getElementById("grupoIdGasto").value = grupoId;
    document.getElementById("grupoIdResumen").value = grupoId;
    document.getElementById("grupoIdPersonas").value = grupoId;
  }
});


async function crearGrupo() {
  const nombre = document.getElementById("nombreGrupo").value;
  if (!nombre) return alert("El nombre es obligatorio");

  const res = await fetch(`${API_URL}/grupos/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre })
  });

  if (res.ok) {
    alert("Grupo creado 🎉");
    document.getElementById("nombreGrupo").value = "";
    cargarGrupos();
  } else {
    alert("Error al crear el grupo");
  }
}

async function cargarGrupos() {
  const res = await fetch(`${API_URL}/grupos/`);
  const grupos = await res.json();

  const lista = document.getElementById("listaGrupos");
  lista.innerHTML = "";

  grupos.forEach(grupo => {
    const li = document.createElement("li");
    li.textContent = `${grupo.id} – ${grupo.nombre}`;
    lista.appendChild(li);
  });
}

async function agregarPersona() {
  const grupoId = document.getElementById("grupoIdPersona").value;
  const nombre = document.getElementById("nombrePersona").value;

  if (!grupoId || !nombre) return alert("Faltan datos");

  const res = await fetch(`${API_URL}/personas/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grupo_id: parseInt(grupoId), nombre })
  });

  if (res.ok) {
    alert("Persona agregada ✅");
    document.getElementById("nombrePersona").value = "";
    verPersonas();
  } else {
    alert("Error al agregar persona");
  }
}

async function verPersonas() {
  const grupoId = document.getElementById("grupoIdListado").value;
  if (!grupoId) return alert("Ingresá el ID del grupo");

  const res = await fetch(`${API_URL}/grupos/${grupoId}`);
  const grupo = await res.json();

  const lista = document.getElementById("listaPersonas");
  lista.innerHTML = "";

  if (grupo.personas) {
    grupo.personas.forEach(persona => {
      const li = document.createElement("li");
      li.textContent = persona.nombre;
      lista.appendChild(li);
    });
  } else {
    lista.innerHTML = "<li>No hay personas o grupo no encontrado</li>";
  }
}

async function registrarGasto() {
  const grupo_id = parseInt(document.getElementById("grupoGasto").value);
  const pagador_id = parseInt(document.getElementById("pagadorGasto").value);
  const descripcion = document.getElementById("descripcionGasto").value;
  const monto = parseFloat(document.getElementById("montoGasto").value);

  if (!grupo_id || !pagador_id || !descripcion || isNaN(monto)) {
    alert("Faltan datos");
    return;
  }

  const res = await fetch(`${API_URL}/gastos/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grupo_id, pagador_id, descripcion, monto })
  });

  if (res.ok) {
    alert("Gasto registrado 🎉");
    // Limpiar inputs
    document.getElementById("descripcionGasto").value = "";
    document.getElementById("montoGasto").value = "";
  } else {
    alert("Error al registrar gasto");
  }
}

async function verLiquidacion() {
  const grupoId = document.getElementById("grupoIdResumen").value;
  if (!grupoId) return alert("Ingresá el ID del grupo");

  const res = await fetch(`${API_URL}/grupos/${grupoId}/liquidacion`);
  const datos = await res.json();

  const lista = document.getElementById("listaLiquidacion");
  lista.innerHTML = "";

  if (datos.length === 0) {
    lista.innerHTML = "<li>Todo saldado 🎉</li>";
    return;
  }

  datos.forEach(item => {
    const li = document.createElement("li");
    li.textContent = `${item.deudor} debe ${item.monto} € a ${item.acreedor}`;
    lista.appendChild(li);
  });
}

async function registrarPago() {
  const grupo_id = parseInt(document.getElementById("grupoPago").value);
  const deudor_id = parseInt(document.getElementById("deudorPago").value);
  const acreedor_id = parseInt(document.getElementById("acreedorPago").value);
  const monto = parseFloat(document.getElementById("montoPago").value);

  if (!grupo_id || !deudor_id || !acreedor_id || isNaN(monto)) {
    alert("Faltan datos o hay error en el monto");
    return;
  }

  const res = await fetch(`${API_URL}/pagos/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ grupo_id, deudor_id, acreedor_id, monto })
  });

  if (res.ok) {
    alert("Pago registrado 💸");
    document.getElementById("montoPago").value = "";
    verLiquidacion(); // actualiza resumen
  } else {
    alert("Error al registrar pago");
  }
}

async function verHistorialPagos() {
  const grupoId = document.getElementById("grupoIdHistorial").value;
  if (!grupoId) return alert("Ingresá el ID del grupo");

  // 1. Pedimos las personas del grupo
  const grupoRes = await fetch(`${API_URL}/grupos/${grupoId}`);
  const grupo = await grupoRes.json();

  if (!grupo.personas) {
    alert("Grupo no encontrado o sin personas");
    return;
  }

  // Creamos el mapa de IDs a nombres
  const idToNombre = {};
  grupo.personas.forEach(p => {
    idToNombre[p.id] = p.nombre;
  });

  // 2. Pedimos los pagos registrados
  const res = await fetch(`${API_URL}/pagos/?grupo_id=${grupoId}`);
  const pagos = await res.json();

  const lista = document.getElementById("listaPagos");
  lista.innerHTML = "";

  if (pagos.length === 0) {
    lista.innerHTML = "<li>No hay pagos registrados aún</li>";
    return;
  }

  // 3. Mostrar pagos con nombres
  pagos.forEach(pago => {
    const fecha = new Date(pago.fecha).toLocaleString();
    const li = document.createElement("li");

    const deudor = idToNombre[pago.deudor_id] || `ID ${pago.deudor_id}`;
    const acreedor = idToNombre[pago.acreedor_id] || `ID ${pago.acreedor_id}`;

    li.textContent = `${deudor} pagó ${pago.monto} € a ${acreedor} el ${fecha}`;
    lista.appendChild(li);
  });
}

async function editarGrupo() {
  const id = parseInt(document.getElementById("grupoEditarId").value);
  const nombre = document.getElementById("grupoNuevoNombre").value;

  if (!id || !nombre) return alert("Faltan datos");

  const res = await fetch(`${API_URL}/grupos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre })
  });

  if (res.ok) {
    alert("Nombre de grupo actualizado ✅");
    cargarGrupos(); // opcional, actualiza la lista
  } else {
    alert("Error al actualizar grupo");
  }
}

async function editarPersona() {
  const id = parseInt(document.getElementById("personaEditarId").value);
  const nombre = document.getElementById("personaNuevoNombre").value;

  if (!id || !nombre) return alert("Faltan datos");

  const res = await fetch(`${API_URL}/personas/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre })
  });

  if (res.ok) {
    alert("Nombre de persona actualizado ✅");
    verPersonas(); // opcional, actualiza la lista del grupo
  } else {
    alert("Error al actualizar persona");
  }
}

async function eliminarPersona() {
  const id = parseInt(document.getElementById("personaEliminarId").value);
  if (!id) return alert("Ingresá un ID válido");

  const res = await fetch(`${API_URL}/personas/${id}`, { method: "DELETE" });

  if (res.ok) {
    alert("Persona eliminada ✅");
    verPersonas(); // refresca la lista
  } else {
    alert("Error al eliminar persona");
  }
}

async function eliminarGasto() {
  const id = parseInt(document.getElementById("gastoEliminarId").value);
  if (!id) return alert("Ingresá un ID válido");

  const res = await fetch(`${API_URL}/gastos/${id}`, { method: "DELETE" });

  if (res.ok) {
    alert("Gasto eliminado ✅");
  } else {
    alert("Error al eliminar gasto");
  }
}

function compartirGrupo() {
  const id = document.getElementById("grupoCompartirId").value;
  if (!id) return alert("Ingresá un ID válido");

  const url = `${window.location.origin}?grupo=${id}`;
  navigator.clipboard.writeText(url);
  alert(`Enlace copiado al portapapeles: ${url}`);
}



// Cargar grupos al cargar la página
cargarGrupos();
