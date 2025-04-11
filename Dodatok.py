import streamlit as st
import pandas as pd
from datetime import datetime

# --- ЗАМІСТЬ ЦЬОГО МОЖНА ПІДКЛЮЧИТИ РЕАЛЬНУ БАЗУ ДАНИХ ---
# Простий список дозволених одноразових токенів
ALLOWED_TOKENS = {
    "abc123": False,
    "xyz456": False,
    "test789": False
}

def is_token_valid(token):
    return token in ALLOWED_TOKENS and not ALLOWED_TOKENS[token]

def mark_token_used(token):
    ALLOWED_TOKENS[token] = True

# --- Початок додатку ---
st.title("📊 Шпаргалка оцінювання (тільки з дозволом)")

# Перевірка токена в URL (наприклад: ?token=abc123)
token = st.query_params.get("token")

if not token:
    st.warning("🔐 Для доступу потрібен спеціальний токен у посиланні. Зверніться до адміністратора.")
    st.stop()

if not is_token_valid(token):
    st.error("🚫 Токен недійсний або вже використаний. Доступ заборонено.")
    st.stop()

# --- Дозволено доступ ---
mark_token_used(token)

st.success("✅ Доступ дозволено. Починайте роботу з оцінювання!")

# --- Основна логіка оцінювання ---
levels = ["Початковий", "Середній", "Достатній", "Високий"]
boundaries = [3, 6, 9, 12]
criteria = ["Знання", "Уміння", "Навички", "Цінності"]

level_scores_12 = list(range(1, 13))
level_scores_percent = [int(i * 100 / 12) for i in level_scores_12]

score_values = {}
for crit in criteria:
    score_values[crit] = st.slider(f"Оцініть критерій '{crit}'", 1, 12, 6)

def get_level(score):
    for i, b in enumerate(boundaries):
        if score <= b:
            return levels[i]
    return levels[-1]

# --- Вивід результатів ---
st.subheader("📈 Результати")
total_score = 0
total_percent = 0
for crit in criteria:
    score = score_values[crit]
    level = get_level(score)
    percent = level_scores_percent[score - 1]
    st.write(f"**{crit}**: {level} — {score}/12 ({percent}%)")
    total_score += score
    total_percent += percent

avg_score = total_score / len(criteria)
avg_percent = total_percent / len(criteria)
avg_level = get_level(int(round(avg_score)))

st.markdown("---")
st.success(f"**Середній рівень:** {avg_level}\n\n**Бал:** {avg_score:.2f} з 12\n\n**Відсоток:** {avg_percent:.0f}%")
