import { register } from "../js/user.js";

const from = document.getElementById('form');
const userInput = document.getElementById("user");
const nameInput = document.getElementById("name");
const lastnameInput = document.getElementById("lastname");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const _passwordInput = document.getElementById ("_password");

const _successToast = document.getElementById("successToast");
const _errorToast = document.getElementById("errorToast");

from.addEventListener('submit', async (e) => {

    e.preventDefault();

    const successToast = bootstrap.Toast.getOrCreateInstance(_successToast)
    const errorToast = bootstrap.Toast.getOrCreateInstance(_errorToast)

    const username = userInput.value;
    const firstname = nameInput.value;
    const lastname = lastnameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;
    const _password = _passwordInput.value;

    if(
        username === '' || firstname === '' || lastname === '' || email === '' || password === '' || _password === ''
    ){
        alert("Rellena todos los campos")
        return;
    }

    if(password !== _password){
        alert("Las contraseñas no son iguales")
        return;
    }

    const res = await register({
        username,
        email,
        name: firstname,
        lastname,
        password
    })
    if(res.id){
        successToast.show()

        setTimeout(() => {
            window.location.href = '/html/' ;
        }, 1000);
        
    }else{
        errorToast.show()
    }

});