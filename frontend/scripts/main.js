const socket = io("https://bangames.jjhost.tk/");
var stats = {};

if (localStorage.getItem("token") != null) {
    document.getElementsByClassName("form")[0].style.display = "none";
    document.getElementsByClassName("home")[0].style.display = "";
    socket.emit("status", { "key": localStorage.getItem("token") });
}


socket.on("connect", () => {
    console.log("Connected to server");
});

socket.on("disconnect", () => {
    console.log("Disconnected from server");
});

socket.on("stats", (data) => {
    stats = data;
    console.log(data);
    // Update everything locally
    document.getElementById("deposit-address").innerHTML = data.deposit_address;
    document.getElementById("balance").innerHTML = "Balance: " + data.balance + " BAN";
});


socket.on("message", (data) => {
    if (data["status"] != "ok") {
        alert(data["message"]);
    } else {
        if (data["data"]) {
            localStorage.setItem("token", data["data"]);
            location.reload();
        }
    };
});


function checkDeposit() {
    socket.emit("deposit", { "key": localStorage.getItem("token") });
}

function logout() {
    localStorage.removeItem("token");
    location.reload();
}

function withdraw() {
    amount = document.getElementById("withdraw-amount").value;
    address = document.getElementById("withdraw-address").value;
    socket.emit("withdraw", { "key": localStorage.getItem("token"), "amount": amount, "address": address });
}

function signup() {
    email = document.getElementById("signup-email").value;
    username = document.getElementById("signup-username").value;
    password = document.getElementById("signup-password").value;
    socket.emit("account_request", { "email": email, "username": username, "pswd": password });

    // Switch screen to Email Verification screen
    $(this).parent().addClass('active');
    $(this).parent().siblings().removeClass('active');

    target = "#email"

    $('.tab-content > div').not(target).hide();
    $('.tab-group').fadeOut(600);

    $(target).fadeIn(600);
}
function login() {
    email = document.getElementById("login-email").value;
    password = document.getElementById("login-password").value;
    socket.emit("login", { "email": email, "pswd": password });
}

$('.form').find('input, textarea').on('keyup blur focus', function (e) {

    var $this = $(this),
        label = $this.prev('label');

    if (e.type === 'keyup') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
        } else {
            label.removeClass('highlight');
        }
    } else if (e.type === 'focus') {

        if ($this.val() === '') {
            label.removeClass('highlight');
        }
        else if ($this.val() !== '') {
            label.addClass('highlight');
        }
    }

});

$('.tab a').on('click', function (e) {

    e.preventDefault();

    $(this).parent().addClass('active');
    $(this).parent().siblings().removeClass('active');

    target = $(this).attr('href');

    $('.tab-content > div').not(target).hide();

    $(target).fadeIn(600);

});