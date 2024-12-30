let button_burger = document.querySelector(".burger-menu");
let burger_list = document.querySelector(".burger-menu-wrapper");

button_burger.addEventListener("click", function (e){
    burger_list.classList.toggle("active-burger");
})