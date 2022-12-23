// Initialize Websocket

const socket = new WebSocket("ws://localhost:2004");

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