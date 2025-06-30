const API_URL = "http://127.0.0.1:8000";

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


// Cargar grupos al cargar la página
cargarGrupos();
