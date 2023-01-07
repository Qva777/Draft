const cartImg = document.getElementById('cart');
const searchImg = document.getElementById('search');
const searchInputImg = document.getElementById('search-input');
const logoImg = document.getElementById('logo');
const menuImg = document.getElementById('menu');


const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

if (prefersDark) {
    cartImg.src = staticUrl + "img/cart.png";
    logoImg.src = staticUrl + "img/logo.png";
    searchImg.src = staticUrl + "img/search.png";
    searchInputImg.src = staticUrl + "img/search.png";
    menuImg.src = staticUrl + "img/menu.png";

} else {
    cartImg.src = staticUrl + "img/cart_dark.png";
    logoImg.src = staticUrl + "img/logo_dark.png";
    searchImg.src = staticUrl + "img/search_dark.png";
    searchInputImg.src = staticUrl + "img/search_dark.png";
    menuImg.src = staticUrl + "img/menu_dark.png";
}


const body = document.querySelector("body"),
    nav = document.querySelector("nav"),
    searchToggle = document.querySelector(".searchToggle"),
    sidebarOpen = document.querySelector(".sidebarOpen");

let getMode = localStorage.getItem("mode");
if (getMode && getMode === "dark-mode") {
    body.classList.add("dark");
}

let subMenu = document.getElementById("subMenu");

function toggleMenu() {
    subMenu.classList.toggle("open-menu");
    searchToggle.classList.remove("active");
}

searchToggle.addEventListener("click", () => {
    searchToggle.classList.toggle("active");
    // searchToggle.classList.toggle("deactivate");

    subMenu.classList.remove("open-menu");
});


body.addEventListener("click", e => {
    let clickedElm = e.target;
    if (!clickedElm.classList.contains("sidebarOpen") && !clickedElm.classList.contains("menu")) {
        nav.classList.remove("active");
    }
});


sidebarOpen.addEventListener("click", () => {
    nav.classList.add("active");
    searchToggle.classList.remove("active");
    subMenu.classList.remove("open-menu");
});


const searchBox = document.querySelector('.searchBox');
document.addEventListener('click', function (event) {
    const isClickInsideSearchBox = searchBox.contains(event.target);
    if (!isClickInsideSearchBox) {
        subMenu.classList.remove('open-menu');
        searchToggle.classList.remove('active');

    }
});
