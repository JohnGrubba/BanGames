const socket = io("127.0.0.1:5500");


if (localStorage.getItem("key") != null) {
    // Show Home Screen
    document.getElementsByClassName("home-screen")[0].style.display = "";
}

function switch_screen(screen) {
    if (screen == "login") {
        document.getElementsByClassName("signup-screen")[0].style.display = "none";
        document.getElementsByClassName("login-screen")[0].style.display = "";
    }
    else if (screen == "signup") {
        document.getElementsByClassName("login-screen")[0].style.display = "none";
        document.getElementsByClassName("signup-screen")[0].style.display = "";
    }

}
function signup() {

}