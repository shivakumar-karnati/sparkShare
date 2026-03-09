document.addEventListener("DOMContentLoaded", function () {

const searchInput = document.getElementById("search-box");
const resources = document.querySelectorAll(".resource-item");

function filterResources(){

const filter = searchInput.value.toLowerCase();

resources.forEach(function(card){

const title = card.querySelector(".resource-title").textContent.toLowerCase();
const subject = card.querySelector(".resource-subject").textContent.toLowerCase();

if(title.includes(filter) || subject.includes(filter)){
card.style.display = "";
}else{
card.style.display = "none";
}

});

}

/* FILTER WHILE TYPING */

searchInput.addEventListener("input", filterResources);


/* FILTER WHEN PRESSING ENTER */

searchInput.addEventListener("keydown", function(e){

if(e.key === "Enter"){

e.preventDefault();

filterResources();

}

});

});