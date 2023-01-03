document.addEventListener("DOMContentLoaded", init);
const URL_API = 'http://localhost:3000/api/'

var customers = []

function init() {
    search()
}

function add() {
    clean()
    openForm()
}

function openForm() {
    htmlmodal = document.getElementById("modal");
    htmlmodal.setAttribute("class", "modale opened");
}

function cerrarModal() {
    htmlmodal = document.getElementById("modal");
    htmlmodal.setAttribute("class", "modale");
}

async function search() {
    var url = URL_API + 'customers'
    var response = await fetch(url, {
        "method": 'GET',
        "headers": {
            "Content-Type": 'application/json'
        }
    })

    customers = await response.json();

    var html = ''
    for (customer of customers) {
        var row = `<tr>
        <td>${customer.nombre}</td>
        <td>${customer.apellido}</td>
        <td>${customer.email}</td>
        <td>${customer.telefono}</td>
        <td>
            <a href="#" onclick="edit(${customer.id})" class="myButtonEd">Editar</a>
            <a href="#" onclick="remove(${customer.id})" class="myButton">Eliminar</a>
        </td>
    </tr>`
        html = html + row;
    }


    document.querySelector('#customers > tbody').outerHTML = html
}

function edit(id) {
    openForm()
    var customer = customers.find(x => x.id == id)
    document.getElementById('txtId').value = customer.id
    document.getElementById('txtAdress').value = customer.adress
    document.getElementById('txtApellido').value = customer.apellido
    document.getElementById('txtEmail').value = customer.email
    document.getElementById('txtNombre').value = customer.nombre
    document.getElementById('txtTelefono').value = customer.telefono
}

async function remove(id) {
    respuesta = confirm('¿Está seguro de eliminarlo?')
    if (respuesta) {
        var url = URL_API + 'customers/' + id
        await fetch(url, {
            "method": 'DELETE',
            "headers": {
                "Content-Type": 'application/json'
            }
        })
        window.location.reload();
    }
}

function clean() {
    document.getElementById('txtId').value = ''
    document.getElementById('txtAdress').value = ''
    document.getElementById('txtApellido').value = ''
    document.getElementById('txtEmail').value = ''
    document.getElementById('txtNombre').value = ''
    document.getElementById('txtTelefono').value = ''
}


async function save() {

    var data = {
        "adress": document.getElementById('txtAdress').value,
        "apellido": document.getElementById('txtApellido').value,
        "email": document.getElementById('txtEmail').value,
        "nombre": document.getElementById('txtNombre').value,
        "telefono": document.getElementById('txtTelefono').value
    }

    var id = document.getElementById('txtId').value
    if (id != '') {
        data.id = id
    }


    var url = URL_API + 'customers'
    await fetch(url, {
        "method": 'POST',
        "body": JSON.stringify(data),
        "headers": {
            "Content-Type": 'application/json'
        }
    })
    window.location.reload();
}



