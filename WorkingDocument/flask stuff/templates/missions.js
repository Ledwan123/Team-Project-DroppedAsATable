const currentPage = document.title;

if (currentPage === "Missions Tier 1"){
    selected = document.getElementById("tier1")
}
else if (currentPage === "Missions Tier 2"){
    selected = document.getElementById("tier2");
}
else{
    selected = document.getElementById("tier3");
}

selected.style.backgroundColor = "rgb(187, 218, 248)";
selected.style.border = "3px solid black"

// selected.addEventListener("mouseenter", (e) => {
//     selected.style.backgroundColor = "red";
// });

// selected.addEventListener("mouseleave", (e) => {
//     selected.style.backgroundColor = "blue";
// });