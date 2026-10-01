import streamlit as st
import random
import time
from streamlit_keyup import st_keyup

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Snake: Add to 700!",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 Snake: Add to 700!")
st.write("Eat the numbers and add them up. Reach **700** to win!")

# -----------------------------
# Constants
# -----------------------------
WIDTH = 20
HEIGHT = 15

NUMBERS = [10, 20, 25, 30, 40, 50, 75, 100]


# -----------------------------
# Initialize game
# -----------------------------
if "snake" not in st.session_state:
    st.session_state.snake = [
        (5, 5),
        (4, 5),
        (3, 5)
    ]

if "direction" not in st.session_state:
    st.session_state.direction = (1, 0)

if "number_position" not in st.session_state:
    st.session_state.number_position = (10, 10)

if "number" not in st.session_state:
    st.session_state.number = random.choice(NUMBERS)

if "total" not in st.session_state:
    st.session_state.total = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "won" not in st.session_state:
    st.session_state.won = False

if "running" not in st.session_state:
    st.session_state.running = False


# -----------------------------
# Reset game
# -----------------------------
def reset_game():
    st.session_state.snake = [
        (5, 5),
        (4, 5),
        (3, 5)
    ]

    st.session_state.direction = (1, 0)

    st.session_state.number_position = (10, 10)

    st.session_state.number = random.choice(NUMBERS)

    st.session_state.total = 0

    st.session_state.game_over = False

    st.session_state.won = False

    st.session_state.running = False


# -----------------------------
# Change direction
# -----------------------------
def change_direction(direction):
    current = st.session_state.direction

    # Don't allow snake to instantly reverse
    if (
        direction[0] == -current[0]
        and direction[1] == -current[1]
    ):
        return

    st.session_state.direction = direction


# -----------------------------
# Keyboard input
# -----------------------------
st.subheader("🎮 Controls")

st.write("Use **⬆️ ⬇️ ⬅️ ➡️** on your keyboard to move.")

key = st_keyup(
    "Press an arrow key ",
    key="snake_keyboard",
    debounce=50
)

if key:

    if key == "ArrowUp":
        change_direction((0, -1))

    elif key == "ArrowDown":
        change_direction((0, 1))

    elif key == "ArrowLeft":
        change_direction((-1, 0))

    elif key == "ArrowRight":
        change_direction((1, 0))


# -----------------------------
# Button controls
# -----------------------------
col1, col2, col3 = st.columns(3)

with col2:
    if st.button("⬆️ Up", use_container_width=True):
        change_direction((0, -1))

with col1:
    if st.button("⬅️ Left", use_container_width=True):
        change_direction((-1, 0))

with col3:
    if st.button("➡️ Right", use_container_width=True):
        change_direction((1, 0))

with col2:
    if st.button("⬇️ Down", use_container_width=True):
        change_direction((0, 1))


# -----------------------------
# Start / New Game
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start Game", use_container_width=True):
        st.session_state.running = True

with col2:
    if st.button("🔄 New Game", use_container_width=True):
        reset_game()
        st.rerun()


# -----------------------------
# Move snake
# -----------------------------
if (
    st.session_state.running
    and not st.session_state.game_over
    and not st.session_state.won
):

    head_x, head_y = st.session_state.snake[0]

    dx, dy = st.session_state.direction

    new_head = (
        head_x + dx,
        head_y + dy
    )

    # -------------------------
    # Wall collision
    # -------------------------
    if (
        new_head[0] < 0
        or new_head[0] >= WIDTH
        or new_head[1] < 0
        or new_head[1] >= HEIGHT
    ):

        st.session_state.game_over = True
        st.session_state.running = False

    else:

        # Add new head
        st.session_state.snake.insert(
            0,
            new_head
        )

        # -------------------------
        # Eat number
        # -------------------------
        if new_head == st.session_state.number_position:

            st.session_state.total += (
                st.session_state.number
            )

            # Win
            if st.session_state.total >= 700:

                st.session_state.won = True
                st.session_state.running = False

            else:

                # Find empty position
                while True:

                    new_position = (
                        random.randint(0, WIDTH - 1),
                        random.randint(0, HEIGHT - 1)
                    )

                    if new_position not in st.session_state.snake:
                        break

                st.session_state.number_position = (
                    new_position
                )

                st.session_state.number = random.choice(
                    NUMBERS
                )

        else:

            # Remove tail
            st.session_state.snake.pop()


# -----------------------------
# Score
# -----------------------------
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🔢 Total",
        st.session_state.total
    )

with col2:
    st.metric(
        "🎯 Goal",
        700
    )


# -----------------------------
# Game board
# -----------------------------
st.subheader("Game Board")

board = []

for y in range(HEIGHT):

    row = []

    for x in range(WIDTH):

        position = (x, y)

        if position == st.session_state.snake[0]:

            cell = "🟢"

        elif position in st.session_state.snake:

            cell = "🟩"

        elif position == st.session_state.number_position:

            cell = f"**{st.session_state.number}**"

        else:

            cell = "⬜"

        row.append(cell)

    board.append(" ".join(row))


for row in board:
    st.markdown(row)


# -----------------------------
# Messages
# -----------------------------
if st.session_state.game_over:

    st.error("💥 Game Over! You hit the wall.")

    st.info(
        f"You scored **{st.session_state.total}**."
    )

elif st.session_state.won:

    st.success("🏆 YOU WIN!")

    st.balloons()

    st.write(
        f"You reached **{st.session_state.total}**!"
    )

elif not st.session_state.running:

    st.info(
        "Press **Start Game** to begin."
    )


# -----------------------------
# Game loop
# -----------------------------
if st.session_state.running:

    time.sleep(0.25)

    st.rerun()
