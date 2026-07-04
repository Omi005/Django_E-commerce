console.log("theme.js loaded");

const themeToggle = document.getElementById("theme-toggle");

console.log("Button found:", themeToggle);

themeToggle.addEventListener("click", function () {

    console.log("Button clicked!");

    document.body.classList.toggle("dark-mode");

    console.log("Body classes:", document.body.className);

    if (document.body.classList.contains("dark-mode")) {
        themeToggle.textContent = "☀️ Light Mode";
    } else {
        themeToggle.textContent = "🌙 Dark Mode";
    }

});