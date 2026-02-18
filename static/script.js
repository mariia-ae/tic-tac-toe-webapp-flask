let mode = "pvp";
let gameOver = false;

const board = document.getElementById("board");
const spielerAnzeige = document.getElementById("spieler");

let aktullerSpieler = "X";
spielerAnzeige.innerText = "Aktueller Spieler: " + aktullerSpieler;

for (let i = 0; i < 9; i++) {
    let button = document.createElement("button");
    button.onclick = () => move(Math.floor(i/3), i%3);
    board.appendChild(button);
}
function setMode(selecteMode) {
    mode = selecteMode;
    resetGame();
}
function move(row, col) {
    if (gameOver){
        return;
    }
    fetch("/move", {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            row: row,
            col: col,
            mode: mode
        })
    })
    .then(responce => responce.json())
    .then(data => {
        if (data.status === "error") {
            alert("Dieses Feld ist besetzt");
            return
        }
        if (data.score) {
            document.getElementById("score").innerText =
            "Player (X): " + data.score.x +
            "| Computer (O): " + data.score.o +
            "| Draw: " + data.score.draw;
        }

        let index = row * 3 + col;
        let buttons = document.querySelectorAll("#board button");

        if (buttons[index].innerText !=="") return;

        if (mode === "pvp") {
            buttons[index].innerText = data.symbol.toUpperCase();
        } else {
            buttons[index].innerText = "X";
        }
        buttons[index].disabled = true
        if (mode === "ai" && data.computer) {
            let i = data.row * 3 + data.col;
            setTimeout(() => {
                buttons[i].innerText = "O";
                buttons[i].classList.add("pop");
                buttons[i].disabled = true;
            }, 400);
        }
        if (data.status === "continue") {
            if (mode === "pvp") {
            spielerAnzeige.innerText =
            "Aktueller Spieler: " + data.player.toUpperCase();
        }
        } else {
            if (data.computer) {
                spielerAnzeige.innerText = "Aktuller Spieler: X";
            }else {
                spielerAnzeige.innerText = "Aktueller Spieler: O";
            }
        }

        if (data.status === "win") {
            gameOver = true;
            data.line.forEach(pos => {
                let i = pos[0] * 3 + pos[1];
                buttons[i].classList.add("win");
            });
            spielerAnzeige.innerText =
            "Gewinner: " + data.winner.toUpperCase();
            spielerAnzeige.classList.add("win-text");
        }

        if (data.status === "draw") {
            gameOver= true;
            spielerAnzeige.innerText = "Unentschieden";
        }
    });
}
function resetGame() {
    fetch("/reset", {
        method: "POST"
    })
    .then(() => { 
       let buttons = document.querySelectorAll("#board button");
       buttons.forEach(btn => {
        btn.innerText ="";
        btn.disabled = false;
        btn.classList.remove("win");
       });
       gameOver = false;
       spielerAnzeige.innerText = "Aktueller Spieler: X";
       spielerAnzeige.classList.remove("win-text");
    })
}
