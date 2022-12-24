// Initialize Websocket
const socket = io("https://bangames.jjhost.tk/tictactoe");

socket.on("message", (data) => {
    console.log(data);
});


// Get the avaliable rooms
socket.on("games", (rooms) => {
    // Get the room list
    console.log(rooms);
    const roomList = document.getElementById("room-list");

    // Clear the room list
    roomList.innerHTML = "";
    roms = "";
    for (const [key, value] of Object.entries(rooms)) {
        roms += `<button id="gam" onclick='join_room("` + key + `")'><a>Stake: ` + value.stake + "</a><br><a>Players: " + value.players + "</a></button>";
    }
    if (roms != "") {
        document.getElementById("no-games").style.display = "none";
        document.getElementById("room-list").style.display = "block";
    }
    roomList.innerHTML = roms;
    // Add the rooms to the room list

});


function startGame() {
    document.getElementById("game").style.display = "block";
    document.getElementById("create").style.display = "none";
}

function join_room(id) {
    console.log("Joining Room " + id);
    socket.emit("join_ttt_game", { "game_id": id, "key": localStorage.getItem("token") });
}

function createSession() {
    socket.emit("create_ttt_game", { "key": localStorage.getItem("token"), "stake": document.getElementById("stake").value });
}

// Get all the cells in the grid
const cells = document.querySelectorAll('[data-cell]');

// Keep track of the current player (X or O)
let currentPlayer = "X";

// Add an event listener to each cell to handle clicks
cells.forEach(cell => {
    cell.addEventListener('click', handleClick);
});

function handleRemoteClick(cellIndex) {
    // Get the cell that was clicked
    const cell = cells[cellIndex];

    // Place the player's symbol in the cell
    if (cell.innerText === "") {
        cell.innerText = currentPlayer;

        // Toggle the current player
        currentPlayer = currentPlayer === "X" ? "O" : "X";
    }
}

function handleClick(e) {
    // Get the cell that was clicked
    const cell = e.target;

    // Place the player's symbol in the cell
    if (cell.innerText === "") {
        cell.innerText = currentPlayer;

        // Toggle the current player
        currentPlayer = currentPlayer === "X" ? "O" : "X";
    }

}