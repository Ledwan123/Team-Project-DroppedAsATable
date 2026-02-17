const redButton = document.getElementById("redbutton");
const blueButton = document.getElementById("bluebutton");
const greenButton = document.getElementById("greenbutton");
const error = document.getElementById("errormessage");

redButton.addEventListener("click", (e) => {
    window.location.href = "/missions_t1";
    alert("Correct");
})

blueButton.addEventListener("click", (e) => {
    error.innerText = "Incorrect"
})

greenButton.addEventListener("click", (e) => {
    error.innerText = "Incorrect"
})

