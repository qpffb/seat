import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="WASD 스네이크 게임", page_icon="🐍", layout="centered")

st.title("🐍 WASD 스네이크 게임")
st.caption(
    "WASD 키 또는 방향키를 사용하여 뱀을 조종하세요! 초록색 먹이를 먹으면 몸집이 길어지고 점수가 올라갑니다."
)

# HTML5 Canvas + JavaScript Snake Game Implementation with WASD Support
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 10px;
        }
        .game-container {
            position: relative;
            text-align: center;
        }
        #gameCanvas {
            background-color: #1a1c23;
            border: 3px solid #4CAF50;
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
        }
        .stats {
            display: flex;
            justify-content: space-between;
            width: 400px;
            margin-bottom: 10px;
            font-size: 18px;
            font-weight: bold;
        }
        .controls-hint {
            margin-top: 12px;
            color: #b0b0b0;
            font-size: 14px;
            line-height: 1.5;
        }
        .key-badge {
            background-color: #333644;
            color: #4CAF50;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #4CAF50;
            font-family: monospace;
            font-weight: bold;
        }
        .btn-reset {
            margin-top: 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .btn-reset:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>

<div class="game-container">
    <div class="stats">
        <div>현재 점수: <span id="score" style="color: #4CAF50;">0</span></div>
        <div>최고 점수: <span id="highScore" style="color: #FFD700;">0</span></div>
    </div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <br>
    <button class="btn-reset" onclick="resetGame()">🎮 다시 시작 (R)</button>
    <div class="controls-hint">
        조작법: <span class="key-badge">W</span> 위 / <span class="key-badge">A</span> 왼쪽 / <span class="key-badge">S</span> 아래 / <span class="key-badge">D</span> 오른쪽<br>
        (방향키 <span class="key-badge">↑</span> <span class="key-badge">←</span> <span class="key-badge">↓</span> <span class="key-badge">→</span> 로도 조작 가능)
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    const gridSize = 20;
    const tileCount = canvas.width / gridSize;

    let score = 0;
    let highScore = 0;
    let dx = gridSize;
    let dy = 0;
    let snake = [
        { x: 160, y: 200 },
        { x: 140, y: 200 },
        { x: 120, y: 200 }
    ];
    let food = { x: 0, y: 0 };
    let gameInterval = null;
    let isGameOver = false;
    let changingDirection = false;

    function main() {
        if (isGameOver) return;
        changingDirection = false;
        clearCanvas();
        drawFood();
        advanceSnake();
        drawSnake();
    }

    function clearCanvas() {
        ctx.fillStyle = "#1a1c23";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.strokeStyle = "#252833";
        ctx.lineWidth = 0.5;
        for (let i = 0; i < canvas.width; i += gridSize) {
            ctx.beginPath();
            ctx.moveTo(i, 0);
            ctx.lineTo(i, canvas.height);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(0, i);
            ctx.lineTo(canvas.width, i);
            ctx.stroke();
        }
    }

    function drawSnake() {
        snake.forEach((part, index) => {
            if (index === 0) {
                ctx.fillStyle = "#4CAF50";
            } else {
                ctx.fillStyle = "#81C784";
            }
            ctx.fillRect(part.x, part.y, gridSize - 1, gridSize - 1);
        });
    }

    function advanceSnake() {
        const head = { x: snake[0].x + dx, y: snake[0].y + dy };

        if (head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height) {
            handleGameOver();
            return;
        }

        for (let i = 0; i < snake.length; i++) {
            if (head.x === snake[i].x && head.y === snake[i].y) {
                handleGameOver();
                return;
            }
        }

        snake.unshift(head);

        const hasEaten = snake[0].x === food.x && snake[0].y === food.y;
        if (hasEaten) {
            score += 10;
            document.getElementById("score").innerText = score;
            if (score > highScore) {
                highScore = score;
                document.getElementById("highScore").innerText = highScore;
            }
            generateFood();
        } else {
            snake.pop();
        }
    }

    function generateFood() {
        food.x = Math.floor(Math.random() * tileCount) * gridSize;
        food.y = Math.floor(Math.random() * tileCount) * gridSize;

        snake.forEach(part => {
            if (part.x === food.x && part.y === food.y) {
                generateFood();
            }
        });
    }

    function drawFood() {
        ctx.fillStyle = "#FF5252";
        ctx.beginPath();
        ctx.arc(food.x + gridSize / 2, food.y + gridSize / 2, gridSize / 2 - 2, 0, Math.PI * 2);
        ctx.fill();
    }

    function handleGameOver() {
        isGameOver = true;
        clearInterval(gameInterval);
        
        ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#FF5252";
        ctx.font = "bold 30px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 10);

        ctx.fillStyle = "#FFFFFF";
        ctx.font = "16px 'Segoe UI', sans-serif";
        ctx.fillText("최종 점수: " + score + "점", canvas.width / 2, canvas.height / 2 + 25);
        ctx.fillText("'R' 키나 아래 버튼을 눌러 다시 시작", canvas.width / 2, canvas.height / 2 + 55);
    }

    function changeDirection(event) {
        const key = event.key.toLowerCase();
        
        if (key === 'r' && isGameOver) {
            resetGame();
            return;
        }

        if (changingDirection) return;

        const goingUp = dy === -gridSize;
        const goingDown = dy === gridSize;
        const goingRight = dx === gridSize;
        const goingLeft = dx === -gridSize;

        if ((key === 'a' || key === 'arrowleft') && !goingRight) {
            dx = -gridSize;
            dy = 0;
            changingDirection = true;
        }
        if ((key === 'w' || key === 'arrowup') && !goingDown) {
            dx = 0;
            dy = -gridSize;
            changingDirection = true;
        }
        if ((key === 'd' || key === 'arrowright') && !goingLeft) {
            dx = gridSize;
            dy = 0;
            changingDirection = true;
        }
        if ((key === 's' || key === 'arrowdown') && !goingUp) {
            dx = 0;
            dy = gridSize;
            changingDirection = true;
        }
    }

    function resetGame() {
        score = 0;
        document.getElementById("score").innerText = score;
        dx = gridSize;
        dy = 0;
        snake = [
            { x: 160, y: 200 },
            { x: 140, y: 200 },
            { x: 120, y: 200 }
        ];
        isGameOver = false;
        generateFood();
        if (gameInterval) clearInterval(gameInterval);
        gameInterval = setInterval(main, 100);
    }

    document.addEventListener("keydown", changeDirection);

    generateFood();
    gameInterval = setInterval(main, 100);
</script>
</body>
</html>
"""

components.html(html_code, height=580)
