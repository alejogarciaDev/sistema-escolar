const usuarios = [
    { usuario: "admin", password: "1234", rol: "admin" },
    { usuario: "gestion", password: "abcd", rol: "pañol" },
    { usuario: "profesor1", password: "pass", rol: "profesor" }
];

document.getElementById("loginForm").addEventListener("submit", function(e){
    e.preventDefault();
    const user = document.getElementById("usuario").value;
    const pass = document.getElementById("password").value;

    const encontrado = usuarios.find(u => u.usuario === user && u.password === pass);

    if(encontrado){
        localStorage.setItem("usuarioLogueado", user);
        localStorage.setItem("rolUsuario", encontrado.rol);

        // Redirige según rol
        if(encontrado.rol === "admin") window.location.href = "dashboard_admin.html";
        else if(encontrado.rol === "pañol") window.location.href = "dashboard_panol2.html";
        else if(encontrado.rol === "profesor") window.location.href = "dashboard_profesor.html";
    } else {
        document.getElementById("error").textContent = "Usuario o contraseña incorrectos";
    }
});

// dashboard admins

// Función para mostrar usuarios en la lista gráfica
f// Función para mostrar usuarios en la lista gráfica
function renderUsers() {
    const userList = document.getElementById("userList");
    userList.innerHTML = "";
    usuarios.forEach(u => {
        const card = document.createElement("div");
        card.className = "user-card";
        card.innerHTML = `
            <h4>${u.usuario}</h4>
            <p>Rol: ${u.rol}</p>
            <p>Contraseña: ${u.password}</p>
        `;
        userList.appendChild(card);
    });
}

// Manejo del formulario para crear usuario
document.getElementById("createUserForm").addEventListener("submit", function(e){
    e.preventDefault();
    const user = document.getElementById("newUsername").value;
    const pass = document.getElementById("newPassword").value;
    const rol = document.getElementById("newRole").value;

    if(user && pass && rol){
        usuarios.push({usuario: user, password: pass, rol: rol});
        renderUsers();

        // Limpiar formulario
        this.reset();
    }
});

// Inicializar lista al cargar
renderUsers();

//dashboard pañol

let categories = ["Comida", "Bebida", "Postres"];
let tools = [
    {name: "Martillo", number: "001", category: "Herramientas"},
    {name: "Destornillador", number: "002", category: "Herramientas"}
];
let loans = [
    {toolNumber: "001", user: "Profesor1"}
];

// Renderizar categorías
function renderCategories() {
    const list = document.getElementById("categoryList");
    list.innerHTML = "";
    categories.forEach(cat => {
        const card = document.createElement("div");
        card.className = "user-card user-card-category";
        card.innerHTML = `<h4>${cat}</h4> 
        <button onclick="deleteCategory('${cat}')">Eliminar</button>`;
        list.appendChild(card);
    });

    const select = document.getElementById("toolCategory");
    select.innerHTML = `<option value="">Seleccionar categoría</option>`;
    categories.forEach(c => select.innerHTML += `<option value="${c}">${c}</option>`);
}

// Renderizar herramientas
function renderTools() {
    const list = document.getElementById("toolList");
    const available = document.getElementById("availableTools");
    list.innerHTML = "";
    available.innerHTML = "";

    tools.forEach(t => {
        const card = document.createElement("div");
        card.className = "user-card user-card-tool";
        card.innerHTML = `<h4>${t.name}</h4><p>Número: ${t.number}</p><p>Categoría: ${t.category}</p>
        <button onclick="deleteTool('${t.number}')">Eliminar</button>`;
        list.appendChild(card);

        // Mostrar solo las herramientas no prestadas
        const prestada = loans.find(l => l.toolNumber === t.number);
        if(!prestada){
            const availCard = document.createElement("div");
            availCard.className = "user-card user-card-available";
            availCard.innerHTML = `<h4>${t.name}</h4><p>Número: ${t.number}</p>`;
            available.appendChild(availCard);
        }
    });
}

// Renderizar préstamos
function renderLoans() {
    const list = document.getElementById("loansList");
    list.innerHTML = "";
    loans.forEach(l => {
        const tool = tools.find(t => t.number === l.toolNumber);
        if(tool){
            const card = document.createElement("div");
            card.className = "user-card user-card-loan";
            card.innerHTML = `<h4>${tool.name}</h4><p>Número: ${tool.number}</p><p>Usuario: ${l.user}</p>`;
            list.appendChild(card);
        }
    });
}

// Crear categoría
document.getElementById("createCategoryForm").addEventListener("submit", function(e){
    e.preventDefault();
    const cat = document.getElementById("newCategory").value;
    if(cat && !categories.includes(cat)){
        categories.push(cat);
        renderCategories();
        this.reset();
    }
});

// Crear herramienta
document.getElementById("createToolForm").addEventListener("submit", function(e){
    e.preventDefault();
    const name = document.getElementById("newToolName").value;
    const number = document.getElementById("newToolNumber").value;
    const category = document.getElementById("toolCategory").value;

    if(name && number && category){
        tools.push({name, number, category});
        renderTools();
        this.reset();
    }
});

// Eliminar categoría (también borra herramientas de esa categoría)
function deleteCategory(cat){
    categories = categories.filter(c => c !== cat);
    tools = tools.filter(t => t.category !== cat);
    renderCategories();
    renderTools();
}

// Eliminar herramienta
function deleteTool(number){
    tools = tools.filter(t => t.number !== number);
    renderTools();
}

// Inicializar
renderCategories();
renderTools();
renderLoans();


//dashboard profesores

// Datos compartidos con el Pañol (simulación)

// Función para mostrar herramientas disponibles
function renderAvailableTools() {
    const list = document.getElementById("availableTools");
    const select = document.getElementById("toolSelect");
    list.innerHTML = "";
    select.innerHTML = `<option value="">Seleccionar herramienta</option>`;

    tools.forEach(t => {
        const prestada = loans.find(l => l.toolNumber === t.number);
        if(!prestada){
            // Mostrar en lista
            const card = document.createElement("div");
            card.className = "user-card user-card-available";
            card.innerHTML = `<h4>${t.name}</h4><p>Número: ${t.number}</p>`;
            list.appendChild(card);

            // Agregar al select
            select.innerHTML += `<option value="${t.number}">${t.name} - ${t.number}</option>`;
        }
    });
}

// Función para mostrar los préstamos del profesor
function renderMyLoans(profName) {
    const list = document.getElementById("myLoans");
    list.innerHTML = "";
    loans.filter(l => l.user === profName).forEach(l => {
        const tool = tools.find(t => t.number === l.toolNumber);
        if(tool){
            const card = document.createElement("div");
            card.className = "user-card user-card-loan";
            card.innerHTML = `<h4>${tool.name}</h4><p>Número: ${tool.number}</p>`;
            list.appendChild(card);
        }
    });
}

// Manejar solicitud de herramienta
document.getElementById("requestToolForm").addEventListener("submit", function(e){
    e.preventDefault();
    const toolNumber = document.getElementById("toolSelect").value;
    const profName = document.getElementById("professorName").value;

    if(toolNumber && profName){
        // Registrar préstamo
        loans.push({toolNumber, user: profName});
        renderAvailableTools();
        renderMyLoans(profName);
        this.reset();
    }
});

// Inicializar al cargar
renderAvailableTools();

const ctx = document.getElementById('toolsChart').getContext('2d');

// Contar herramientas prestadas
const prestadas = loans.length;
const disponibles = tools.length - prestadas;

const toolsChart = new Chart(ctx, {
    type: 'doughnut', // tipo de gráfico
    data: {
        labels: ['Disponibles', 'Prestadas'],
        datasets: [{
            label: 'Estado de Herramientas',
            data: [disponibles, prestadas],
            backgroundColor: ['#4CAF50', '#FF5722'],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});

const API_URL = "http://127.0.0.1:8001"; // Cambiar si tu FastAPI corre en otra URL

// Crear usuario
document.getElementById("createUserForm").addEventListener("submit", async function(e){
    e.preventDefault();
    
    const name = document.getElementById("newName").value;
    const email = document.getElementById("newEmail").value;
    const password = document.getElementById("newPassword").value;
    const role_id = parseInt(document.getElementById("newRole").value);

    try {
        const res = await fetch(`${API_URL}/users`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name, email, password, role_id})
        });
        const data = await res.json();

        if(data.error){
            alert(data.error);
        } else {
            alert(`Usuario ${data.name} creado`);
            this.reset();
            obtenerUsuarios();
        }
    } catch(err){
        console.error(err);
        alert("Error al crear usuario");
    }
});

// Obtener lista de usuarios
async function obtenerUsuarios(){
    try {
        const res = await fetch(`${API_URL}/users`);
        const users = await res.json();
        const list = document.getElementById("userList");
        list.innerHTML = "";
        users.forEach(u => {
            const card = document.createElement("div");
            card.className = "user-card";
            card.innerHTML = `<h4>${u.name}</h4><p>Email: ${u.email}</p><p>Rol: ${u.role_id}</p>`;
            list.appendChild(card);
        });
    } catch(err){
        console.error(err);
    }
}

// Inicializar
obtenerUsuarios();
