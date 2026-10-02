import streamlit as st
import random
import time

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
# Direction controls
# -----------------------------
st.subheader("Controls")

st.write("Use the direction buttons to move. The snake cannot turn directly back into itself.")

# -----------------------------
# Button controls
# -----------------------------
col1, col2, col3 = st.columns(3)

with col2:
    if st.button("↑ Up", use_container_width=True):
        change_direction((0, -1))

with col1:
    if st.button("← Left", use_container_width=True):
        change_direction((-1, 0))

with col3:
    if st.button("→ Right", use_container_width=True):
        change_direction((1, 0))

with col2:
    if st.button("↓ Down", use_container_width=True):
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

snake = st.session_state.snake
cells = []
for y in range(HEIGHT):
    for x in range(WIDTH):
        position = (x, y)
        if position == snake[0]:
            cells.append('<div class="cell snake-head" aria-label="Snake head">●</div>')
        elif position in snake:
            cells.append('<div class="cell snake-body" aria-label="Snake">●</div>')
        elif position == st.session_state.number_position:
            cells.append(f'<div class="cell food" aria-label="Number {st.session_state.number}">{st.session_state.number}</div>')
        else:
            cells.append('<div class="cell empty"></div>')

st.markdown(
    f"""
    <style>
    .snake-board {{
        display: grid;
        grid-template-columns: repeat({WIDTH}, minmax(0, 1fr));
        width: 100%;
        max-width: 760px;
        aspect-ratio: {WIDTH} / {HEIGHT};
        border: 2px solid #334155;
        border-radius: 10px;
        overflow: hidden;
        background: #f8fafc;
    }}
    .cell {{
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 0;
        border: 1px solid #e2e8f0;
        font-size: clamp(8px, 1.8vw, 18px);
        font-weight: 700;
    }}
    .snake-head {{ color: #166534; background: #86efac; }}
    .snake-body {{ color: #15803d; background: #bbf7d0; }}
    .food {{ color: #9a3412; background: #fed7aa; border-radius: 50%; }}
    </style>
    <div class="snake-board">{''.join(cells)}</div>
    """,
    unsafe_allow_html=True,
)


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

