# 💸 Gastos App

Una app web simple para repartir gastos entre amigos, sin líos. Inspirada en Tricount, pero mucho más fácil de usar.

---

## 👣 ¿Qué hicimos paso a paso?

### ✅ Paso 1 – Creamos la estructura base del proyecto
- Armamos una carpeta vacía en el ordenador.
- Instalamos Python y FastAPI (tecnología que nos permite crear una “app por dentro”, como si fuera el motor).
- Creamos un archivo principal que responde con un mensaje: “Bienvenido a la app de gastos”.

---

### ✅ Paso 2 – Probamos que la app funcione localmente
- Ejecutamos el servidor para ver si responde.
- Lo abrimos en el navegador para confirmar que todo funcione.

---

### ✅ Paso 3 – Creamos la base de datos
- Preparamos una base para guardar información: grupos, personas, gastos.
- Usamos SQLite, una base de datos muy liviana.

---

### ✅ Paso 4 – Modelamos los datos
- Creamos 3 estructuras: `Grupo`, `Persona`, `Gasto`.
- Así definimos cómo vamos a guardar los datos.

---

### ✅ Paso 5 – Hicimos que se creen las tablas automáticamente
- Al iniciar la app, si no existe la base de datos, se crea sola.

---

### ✅ Paso 6 – Creamos el primer grupo desde la web
- Hicimos un endpoint para crear un grupo de amigos o familia, con nombre.

---

### ✅ Paso 7 – Permitimos ver todos los grupos creados
- Agregamos un botón que lista todos los grupos cargados.

---

### ✅ Paso 8 – Permitimos agregar personas a un grupo
- Creamos un formulario donde escribís el nombre y el número de grupo.
- Queda registrada cada persona en la base.

---

### ✅ Paso 9 – Creamos la lógica para registrar gastos
- Se puede indicar quién pagó, cuánto y para qué grupo.

---

### ✅ Paso 10 – Creamos la lógica para ver los gastos de un grupo
- Podés ver todo lo que se pagó dentro de un grupo determinado.

---

### ✅ Paso 11 – Mostramos un resumen individual
- Calculamos cuánto gastó cada persona y cuánto debería haber gastado.
- Mostramos si le deben o si debe plata.

---

### ✅ Paso 12 – Creamos la liquidación
- La app te dice directamente: “Ana le debe 20 € a Juan”.
- Hace los cálculos para repartir la plata y saldar cuentas.

---

### ✅ Paso 13 – Mejoramos el resumen individual
- Mostramos nombre, cuánto puso, cuánto le tocaba poner y el saldo exacto.

---

### ✅ Paso 14 – Mostramos los pagos que equilibran el grupo
- Ya no es solo un resumen, ahora es una guía de quién debe pagarle a quién para quedar 0 a 0.

---

### ✅ Paso 15 – Creamos el registro de pagos reales
- Agregamos la posibilidad de anotar: “Ya le pagué 15 € a Juan”.

---

### ✅ Paso 16 – La liquidación tiene en cuenta los pagos hechos
- Si ya pagaste, la app lo descuenta y solo te muestra lo que falta por saldar.

---

### ✅ Paso 17 – Creamos la parte visual (frontend)
- Hicimos una página simple para que cualquier persona pueda usarla sin instalar nada.
- Todo está en `index.html`.

---

### ✅ Paso 18 – Permitimos agregar personas desde el navegador
- Con el ID del grupo y un nombre, agregás gente fácil y rápido.

---

### ✅ Paso 19 – Permitimos registrar gastos desde el navegador
- Desde la misma página podés indicar cuánto pagó alguien y qué pagó.

---

### ✅ Paso 20 – Mostramos el resumen final en la web
- Hacés clic en “Ver resumen” y te dice exactamente quién le debe a quién.

---

## 📦 ¿Qué hay en el proyecto?

- Un motor que calcula quién debe qué (backend)
- Una base de datos que guarda todo
- Una web muy simple para interactuar (frontend)

---

## 🧪 ¿Cómo se usa?

1. Abrís el archivo `frontend/index.html`  
2. Creás un grupo  
3. Agregás personas  
4. Cargás gastos  
5. Ves automáticamente el resumen y los pagos sugeridos  
6. Marcás pagos como saldados si alguien ya transfirió

---

## 🧠 ¿Qué aprendimos?

- Cómo funciona una app por dentro
- Cómo se organizan datos reales
- Cómo hacer que una app calcule y muestre cosas útiles
- Cómo trabajar paso a paso para no mezclar todo

---

## 👤 Autor

Proyecto realizado por [@joaquinserra94](https://github.com/joaquinserra94)  
Desarrollado en MacBook, usando Warp y Visual Studio Code.

---

💬 Este README está escrito para que cualquier persona —aunque no programe— pueda entender qué hicimos y por qué.

