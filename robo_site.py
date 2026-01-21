import random
import streamlit as st
import pyttsx3

# --------- VOZ (pyttsx3) ----------
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# --------- Configuração do site ----------
st.set_page_config(
    page_title="English Study Robot",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🤖 ENGLISH STUDY ROBOT")
st.write("Welcome! 🇺🇸")

# --------- Banco de palavras (10 níveis) ----------
levels = {
    1: {"gato": "cat", "cachorro": "dog", "casa": "house", "livro": "book", "água": "water"},
    2: {"carro": "car", "escola": "school", "janela": "window", "comida": "food", "mesa": "table"},
    3: {"amigo": "friend", "família": "family", "trabalho": "work", "cidade": "city", "mundo": "world"},
    4: {"feliz": "happy", "triste": "sad", "cansado": "tired", "perto": "near", "longe": "far"},
    5: {"difícil": "difficult", "importante": "important", "interessante": "interesting", "seguro": "safe", "rápido": "fast"},
    6: {"praia": "beach", "montanha": "mountain", "viagem": "travel", "férias": "vacation", "hotel": "hotel"},
    7: {"música": "music", "filme": "movie", "jogo": "game", "esporte": "sport", "arte": "art"},
    8: {"saúde": "health", "medicina": "medicine", "doença": "disease", "remédio": "medicine", "hospital": "hospital"},
    9: {"tecnologia": "technology", "computador": "computer", "internet": "internet", "programação": "programming", "aplicativo": "app"},
    10: {"economia": "economy", "investimento": "investment", "negócio": "business", "mercado": "market", "empresa": "company"},
}

# --------- Histórico e Ranking ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "ranking" not in st.session_state:
    st.session_state.ranking = []

def reset_all():
    st.session_state.history = []
    st.session_state.ranking = []

# --------- Menu ----------
menu = st.sidebar.selectbox("Menu", ["Home", "Vocabulary", "Quiz", "Phrases", "Ranking", "History", "Settings", "Reset"])

# --------- HOME ----------
if menu == "Home":
    st.subheader("Welcome to your English Study Robot!")
    st.write("Use the menu on the left to choose a mode.")
    st.write("This site has the same features as the CMD version, but now with voice, ranking, and more.")

# --------- VOCABULARY ----------
if menu == "Vocabulary":
    st.subheader("Vocabulary Practice (10 levels)")
    level = st.slider("Choose level", 1, 10, 1)
    words = list(levels[level].items())
    random.shuffle(words)

    score = 0
    for pt, en in words:
        answer = st.text_input(f"Translate '{pt}'", key=f"v_{level}_{pt}")
        if answer:
            if answer.lower() == en:
                st.success("Correct!")
                score += 1
            else:
                st.error(f"Wrong. Correct: {en}")

    st.write(f"Score: {score}/{len(words)}")

    if score == len(words):
        st.balloons()
        st.write("Perfect! 🌟")
    elif score >= 3:
        st.write("Very good! 👍")
    else:
        st.write("Keep practicing 💙")

    # salvar no histórico e ranking
    st.session_state.history.append(
        {"mode": "Vocabulary", "level": level, "score": score, "total": len(words)}
    )
    st.session_state.ranking.append(score)

# --------- QUIZ ----------
if menu == "Quiz":
    st.subheader("Quiz (random questions)")

    quiz_questions = [
        ("What is the English word for 'gato'?", "cat"),
        ("What is the English word for 'cachorro'?", "dog"),
        ("What is the English word for 'casa'?", "house"),
        ("What is the English word for 'livro'?", "book"),
        ("What is the English word for 'água'?", "water"),
        ("What is the English word for 'carro'?", "car"),
        ("What is the English word for 'escola'?", "school"),
        ("What is the English word for 'janela'?", "window"),
        ("What is the English word for 'comida'?", "food"),
        ("What is the English word for 'mesa'?", "table"),
    ]

    q, correct = random.choice(quiz_questions)
    answer = st.text_input(q, key="quiz")

    if answer:
        if answer.lower() == correct:
            st.success("Correct!")
        else:
            st.error(f"Wrong. Correct: {correct}")

        st.session_state.history.append(
            {"mode": "Quiz", "question": q, "answer": answer, "correct": correct}
        )

# --------- PHRASES ----------
if menu == "Phrases":
    st.subheader("Phrases Practice")
    phrases = [
        ("Como você está?", "How are you?"),
        ("Qual é o seu nome?", "What is your name?"),
        ("Onde fica a escola?", "Where is the school?"),
        ("Eu gosto de música.", "I like music."),
        ("Eu quero viajar.", "I want to travel."),
    ]

    pt, en = random.choice(phrases)
    st.write(f"Portuguese: {pt}")
    answer = st.text_input("Type the English sentence:", key="phrases")

    if answer:
        if answer.lower() == en.lower():
            st.success("Correct!")
        else:
            st.error(f"Wrong. Correct: {en}")

        st.session_state.history.append(
            {"mode": "Phrases", "pt": pt, "answer": answer, "correct": en}
        )

# --------- RANKING ----------
if menu == "Ranking":
    st.subheader("Ranking (Top Scores)")
    ranking_sorted = sorted(st.session_state.ranking, reverse=True)
    for i, score in enumerate(ranking_sorted[:10], start=1):
        st.write(f"{i}º - {score} points")

# --------- HISTORY ----------
if menu == "History":
    st.subheader("History")
    st.write(st.session_state.history)

# --------- SETTINGS (VOZ) ----------
if menu == "Settings":
    st.subheader("Settings")

    st.write("Voice settings (text to speech)")
    if st.button("Speak: Hello!"):
        speak("Hello! Welcome to English Study Robot.")

# --------- RESET ----------
if menu == "Reset":
    st.subheader("Reset")
    if st.button("Reset All"):
        reset_all()
        st.write("All history and ranking cleared.")