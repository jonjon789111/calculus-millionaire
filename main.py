
import streamlit as st
import time
import random
import json
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Calculus Millionaire",
    page_icon="🧮",
    layout="centered"
)

# ==========================================
# 2. GAME INFORMATION
# ==========================================

PRIZES = [
    100, 200, 300, 500, 1000,
    2000, 4000, 8000, 16000, 32000,
    64000, 125000, 250000, 500000, 1000000
]

QUESTIONS = [
    {
        "question": "What is the limit of x + 2 as x approaches 3?",
        "options": ["3", "5", "6", "2"],
        "answer": 1
    },
    {
        "question": "Evaluate the limit of x² as x approaches 4.",
        "options": ["8", "12", "16", "20"],
        "answer": 2
    },
    {
        "question": "What is the limit of 2x + 5 as x approaches 2?",
        "options": ["7", "9", "10", "12"],
        "answer": 1
    },
    {
        "question": "A function is continuous at a point when:",
        "options": [
            "The limit does not exist",
            "The function is undefined",
            "The limit equals the function value",
            "The graph has a gap"
        ],
        "answer": 2
    },
    {
        "question": "What is the derivative of f(x) = x²?",
        "options": ["x", "2x", "x²", "2"],
        "answer": 1
    },
    {
        "question": "What is the derivative of f(x) = 5x³?",
        "options": ["5x²", "15x²", "15x³", "3x²"],
        "answer": 1
    },
    {
        "question": "What is the derivative of f(x) = x² + 4x?",
        "options": ["2x + 4", "2x + 2", "x + 4", "2x"],
        "answer": 0
    },
    {
        "question": "Find the derivative of f(x) = x(x + 3).",
        "options": ["x + 3", "2x + 3", "2x", "x² + 3"],
        "answer": 1
    },
    {
        "question": "What is the derivative of f(x) = (x² + 1)/x?",
        "options": [
            "1 + 1/x²",
            "1 - 1/x²",
            "2x",
            "x + 1"
        ],
        "answer": 1
    },
    {
        "question": "What is the derivative of f(x) = (3x + 2)⁴?",
        "options": [
            "4(3x + 2)³",
            "12(3x + 2)³",
            "3(3x + 2)⁴",
            "12(3x + 2)⁴"
        ],
        "answer": 1
    },
    {
        "question": "What is the second derivative of f(x) = x³?",
        "options": ["3x", "6x", "6", "3x²"],
        "answer": 1
    },
    {
        "question": "What is the derivative of sin(x)?",
        "options": ["-sin(x)", "cos(x)", "-cos(x)", "tan(x)"],
        "answer": 1
    },
    {
        "question": "A car's position is s(t) = t² + 4t. What is its velocity at t = 3?",
        "options": ["8", "9", "10", "12"],
        "answer": 2
    },
    {
        "question": "A rectangle has a fixed perimeter of 20 units. Which dimensions maximize its area?",
        "options": [
            "2 by 8",
            "3 by 7",
            "4 by 6",
            "5 by 5"
        ],
        "answer": 3
    },
    {
        "question": "What is the derivative of f(x) = x² sin(x)?",
        "options": [
            "2x cos(x)",
            "2x sin(x) + x² cos(x)",
            "x² cos(x)",
            "2x + sin(x)"
        ],
        "answer": 1
    }
]

# ==========================================
# 3. WEBSITE DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #071426, #142c4c);
    color: white;
}

h1, h2, h3 {
    color: #f5c542 !important;
}

.stButton > button {
    background-color: #d9a928;
    color: #071426;
    border-radius: 10px;
    width: 100%;
    min-height: 48px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #f5c542;
    color: #071426;
}

div[data-testid="stMetric"] {
    background-color: #142c4c;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. SESSION VARIABLES
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "menu"

if "player" not in st.session_state:
    st.session_state.player = ""

if "question_number" not in st.session_state:
    st.session_state.question_number = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "deadline" not in st.session_state:
    st.session_state.deadline = 0

if "timer_total" not in st.session_state:
    st.session_state.timer_total = 30

if "used_5050" not in st.session_state:
    st.session_state.used_5050 = False

if "used_audience" not in st.session_state:
    st.session_state.used_audience = False

if "used_time" not in st.session_state:
    st.session_state.used_time = False

if "hidden_options" not in st.session_state:
    st.session_state.hidden_options = []

if "audience_votes" not in st.session_state:
    st.session_state.audience_votes = []

if "message" not in st.session_state:
    st.session_state.message = ""

if "saved_result" not in st.session_state:
    st.session_state.saved_result = False

# ==========================================
# 5. LEADERBOARD
# ==========================================

LEADERBOARD_FILE = Path(__file__).with_name("leaderboard.json")


def load_leaderboard():

    if LEADERBOARD_FILE.exists():

        try:
            with open(LEADERBOARD_FILE, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return []

    return []


def save_result():

    if st.session_state.saved_result:
        return

    leaderboard = load_leaderboard()

    new_player = {
        "name": st.session_state.player,
        "score": st.session_state.score,
        "questions": st.session_state.question_number
    }

    leaderboard.append(new_player)

    leaderboard.sort(
        key=lambda player: player["score"],
        reverse=True
    )

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard[:20], file, indent=4)

    st.session_state.saved_result = True


# ==========================================
# 6. TIMER
# ==========================================

def get_time_limit():

    number = st.session_state.question_number

    if number < 5:
        return 30

    elif number < 10:
        return 25

    else:
        return 20


def start_timer():

    duration = get_time_limit()

    st.session_state.timer_total = duration
    st.session_state.deadline = time.time() + duration


# ==========================================
# 7. SAFE MILESTONE SYSTEM
# ==========================================

def get_safe_score():

    completed = st.session_state.question_number

    if completed >= 10:
        return 32000

    elif completed >= 5:
        return 1000

    else:
        return 0


def end_game(message):

    st.session_state.score = get_safe_score()

    st.session_state.message = message
    st.session_state.page = "result"


# ==========================================
# 8. ANSWER SYSTEM
# ==========================================

def submit_answer(choice):

    number = st.session_state.question_number

    question = QUESTIONS[number]

    if time.time() >= st.session_state.deadline:

        end_game("TIME'S UP!")

    elif choice == question["answer"]:

        st.session_state.score = PRIZES[number]

        st.session_state.question_number += 1

        st.session_state.hidden_options = []
        st.session_state.audience_votes = []

        if st.session_state.question_number == 15:

            st.session_state.score = 1000000

            st.session_state.message = (
                "CONGRATULATIONS! YOU WON THE JACKPOT!"
            )

            st.session_state.page = "result"

        else:

            start_timer()

    else:

        end_game("WRONG ANSWER!")


# ==========================================
# 9. LIFELINE: 50:50
# ==========================================

def use_5050():

    number = st.session_state.question_number

    correct = QUESTIONS[number]["answer"]

    st.session_state.hidden_options = []

    while len(st.session_state.hidden_options) < 2:

        random_number = random.randint(0, 3)

        if random_number != correct:

            if random_number not in st.session_state.hidden_options:

                st.session_state.hidden_options.append(
                    random_number
                )

    st.session_state.used_5050 = True


# ==========================================
# 10. LIFELINE: ASK THE AUDIENCE
# ==========================================

def use_audience():

    number = st.session_state.question_number

    correct = QUESTIONS[number]["answer"]

    votes = []

    for i in range(4):

        votes.append(random.randint(5, 15))

    votes[correct] = votes[correct] + 60

    total = 0

    for i in range(4):

        total = total + votes[i]

    percentages = []

    for i in range(4):

        percentage = round(votes[i] / total * 100)

        percentages.append(percentage)

    st.session_state.audience_votes = percentages

    st.session_state.used_audience = True


# ==========================================
# 11. LIFELINE: EXTRA TIME
# ==========================================

def use_extra_time():

    st.session_state.deadline += 15

    st.session_state.timer_total += 15

    st.session_state.used_time = True


# ==========================================
# 12. LIVE TIMER DISPLAY
# ==========================================

@st.fragment(run_every="1s")
def timer_display():

    if st.session_state.page != "quiz":
        return

    remaining = int(
        st.session_state.deadline - time.time() + 0.999
    )

    if remaining < 0:
        remaining = 0

    st.subheader(
        "⏳ TIME LEFT: " + str(remaining) + " SECONDS"
    )

    progress = remaining / st.session_state.timer_total

    st.progress(progress)

    if remaining == 0:

        end_game("TIME'S UP!")

        st.rerun(scope="app")


# ==========================================
# 13. MAIN MENU
# ==========================================

def main_menu():

    st.title("🧮 CALCULUS")
    st.title("MILLIONAIRE")

    st.subheader("THE ULTIMATE MATH CHALLENGE")

    st.write("")

    st.markdown(
        "### Are you ready to become a Calculus Millionaire?"
    )

    st.write(
        "Answer 15 Differential Calculus questions "
        "and win 1,000,000 points!"
    )

    st.divider()

    if st.button("▶ PLAY GAME"):

        st.session_state.page = "player"

        st.rerun()

    if st.button("🏆 LEADERBOARD"):

        st.session_state.page = "leaderboard"

        st.rerun()

    if st.button("📖 HOW TO PLAY"):

        st.session_state.page = "instructions"

        st.rerun()


# ==========================================
# 14. PLAYER NAME SCREEN
# ==========================================

def player_screen():

    st.title("ENTER YOUR NAME")

    name = st.text_input("Player Name")

    if st.button("CONTINUE"):

        if name.strip() != "":

            st.session_state.player = name.strip()

            st.session_state.question_number = 0
            st.session_state.score = 0

            st.session_state.used_5050 = False
            st.session_state.used_audience = False
            st.session_state.used_time = False

            st.session_state.hidden_options = []
            st.session_state.audience_votes = []

            st.session_state.saved_result = False

            st.session_state.page = "quiz"

            start_timer()

            st.rerun()

        else:

            st.warning("Please enter your name!")


# ==========================================
# 15. QUIZ SCREEN
# ==========================================

def quiz_screen():

    number = st.session_state.question_number

    question = QUESTIONS[number]

    st.title("🧮 CALCULUS MILLIONAIRE")

    st.write("Player: " + st.session_state.player)

    st.progress((number + 1) / 15)

    # QUESTION NUMBER AND PRIZE

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "QUESTION",
            str(number + 1) + " / 15"
        )

    with col2:

        st.metric(
            "QUESTION PRIZE",
            str(PRIZES[number]) + " points"
        )

    st.divider()

    # TIMER

    timer_display()

    st.divider()

    # QUESTION

    st.header("QUESTION " + str(number + 1))

    st.info(question["question"])

    st.subheader("SELECT YOUR ANSWER")

    # ANSWER CHOICES

    for i in range(4):

        if i not in st.session_state.hidden_options:

            option = question["options"][i]

            if st.button(
                option,
                key="answer_" + str(number) + "_" + str(i)
            ):

                submit_answer(i)

                st.rerun()

    # LIFELINES

    st.divider()

    st.subheader("🛟 LIFELINES")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "50:50",
            disabled=st.session_state.used_5050
        ):

            use_5050()

            st.rerun()

    with col2:

        if st.button(
            "AUDIENCE",
            disabled=st.session_state.used_audience
        ):

            use_audience()

            st.rerun()

    with col3:

        if st.button(
            "+15 SEC",
            disabled=st.session_state.used_time
        ):

            use_extra_time()

            st.rerun()

    # AUDIENCE RESULTS

    if len(st.session_state.audience_votes) > 0:

        st.subheader("📊 AUDIENCE VOTING")

        for i in range(4):

            option = question["options"][i]

            vote = st.session_state.audience_votes[i]

            st.write(option + ": " + str(vote) + "%")

            st.progress(vote / 100)

    # PRIZE LADDER

    st.divider()

    st.subheader("🏆 PRIZE LADDER")

    for i in range(14, -1, -1):

        if i == number:

            st.markdown(
                "**➡️ QUESTION "
                + str(i + 1)
                + " — "
                + str(PRIZES[i])
                + " POINTS**"
            )

        elif i < number:

            st.write(
                "✅ Question "
                + str(i + 1)
                + " — "
                + str(PRIZES[i])
                + " points"
            )

        else:

            st.write(
                "Question "
                + str(i + 1)
                + " — "
                + str(PRIZES[i])
                + " points"
            )


# ==========================================
# 16. RESULTS SCREEN
# ==========================================

def result_screen():

    save_result()

    st.title("🏆 GAME OVER")

    st.subheader(st.session_state.message)

    st.write("Player: " + st.session_state.player)

    st.metric(
        "FINAL SCORE",
        str(st.session_state.score) + " points"
    )

    st.metric(
        "QUESTIONS COMPLETED",
        str(st.session_state.question_number) + " / 15"
    )

    if st.session_state.question_number == 15:

        st.success("YOU ARE A CALCULUS MILLIONAIRE!")

    else:

        st.info(
            "You secured "
            + str(st.session_state.score)
            + " points."
        )

    if st.button("🔄 PLAY AGAIN"):

        st.session_state.page = "menu"

        st.rerun()

    if st.button("🏆 LEADERBOARD"):

        st.session_state.page = "leaderboard"

        st.rerun()

    if st.button("🏠 MAIN MENU"):

        st.session_state.page = "menu"

        st.rerun()


# ==========================================
# 17. LEADERBOARD SCREEN
# ==========================================

def leaderboard_screen():

    st.title("🏆 LEADERBOARD")

    leaderboard = load_leaderboard()

    if len(leaderboard) > 0:

        for i in range(len(leaderboard)):

            player = leaderboard[i]

            st.write(
                str(i + 1)
                + ". "
                + player["name"]
                + " — "
                + str(player["score"])
                + " points"
            )

    else:

        st.info("No scores recorded yet!")

    if st.button("BACK TO MENU"):

        st.session_state.page = "menu"

        st.rerun()


# ==========================================
# 18. INSTRUCTIONS SCREEN
# ==========================================

def instructions_screen():

    st.title("📖 HOW TO PLAY")

    st.markdown("""
    ### GAME RULES

    1. Enter your player name.
    2. Answer 15 Differential Calculus questions.
    3. Each correct answer increases your prize.
    4. A wrong answer ends your game.
    5. Running out of time also ends your game.

    ### LIFELINES

    - **50:50:** Removes two incorrect answers.
    - **AUDIENCE:** Shows simulated audience votes.
    - **EXTRA TIME:** Adds 15 seconds.

    ### SAFE MILESTONES

    - Question 5: 1,000 points.
    - Question 10: 32,000 points.

    ### JACKPOT

    Reach Question 15 and win 1,000,000 points!
    """)

    if st.button("BACK TO MENU"):

        st.session_state.page = "menu"

        st.rerun()


# ==========================================
# 19. PAGE NAVIGATION
# ==========================================

if st.session_state.page == "menu":

    main_menu()

elif st.session_state.page == "player":

    player_screen()

elif st.session_state.page == "quiz":

    quiz_screen()

elif st.session_state.page == "result":

    result_screen()

elif st.session_state.page == "leaderboard":

    leaderboard_screen()

elif st.session_state.page == "instructions":

    instructions_screen()
