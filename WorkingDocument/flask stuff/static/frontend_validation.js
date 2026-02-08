const username_input = document.getElementById("username_input");
const email_input = document.getElementById("email_input");
const password_input = document.getElementById("password_input");
const confirm_password_input = document.getElementById("confirm_password_input");
const error_message = document.getElementById("error_message");
const form = document.querySelector("#form");

var inputs = [];

form.addEventListener('submit', (e) => {

    e.preventDefault();

    let errors = [];

    if (email_input){
        //Sign Up page
        errors = signUpErrors(username_input.value, email_input.value, password_input.value, confirm_password_input.value);
        inputs = [username_input, email_input, password_input, confirm_password_input];
    }
    else{
        //Log in page
        errors = logInErrors(username_input.value, password_input.value);
        inputs = [username_input, password_input];
    }

    if (errors.length > 0){
        error_message.innerText = errors.join(". ")
    }
    else {
        sendData();
    }
})

async function sendData(){
    const formData = new FormData(form);

        try{
            const response = await fetch("https://silver-halibut-9755xgqw64qxhp7rj-5000.app.github.dev/login", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData),
            });
            const content = await response.json();
            console.log(content);
        }
        catch (e){
            console.log(e);
        }
}

function signUpErrors(username, email, password, confirm_password){

    let errors = [];

    if (username === "" || username === null){
        errors.push("Username is missing");
        username_input.parentElement.classList.add('incorrect')
    }
    if (email === "" || email === null){
        errors.push("Email is missing");
        email_input.parentElement.classList.add('incorrect')
    }
    if (password === "" || password === null){
        errors.push("Password is missing");
        password_input.parentElement.classList.add('incorrect')
    }
    if (confirm_password === "" || confirm_password === null){
        errors.push("Please confirm password");
        confirm_password_input.parentElement.classList.add('incorrect')
    }
    if (password !== confirm_password){
        errors.push("Passwords do not match");
        confirm_password_input.parentElement.classList.add('incorrect')
    }

    return errors;
}

function logInErrors(username, password){

    let errors = [];

    if (username === "" || username === null){
        errors.push("Username is missing");
        username_input.parentElement.classList.add('incorrect')
    }
    if (password === "" || password === null){
        errors.push("Password is missing");
        password_input.parentElement.classList.add('incorrect')
    }

    return errors;
}



inputs.forEach(input => {
    input.addEventListener( "input", (e) => {
        if (input.parentElement.classList.contains("incorrect")){
            input.parentElement.classList.remove("incorrect")
        }
    })
})
