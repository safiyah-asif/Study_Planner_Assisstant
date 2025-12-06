import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Study Planner Assistant", page_icon="📚")

st.title("📚 Study Session Planner – Interactive Assistant")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "goal" not in st.session_state:
    st.session_state.goal = None
if "topics" not in st.session_state:
    st.session_state.topics = None
if "hours" not in st.session_state:
    st.session_state.hours = None
if "waiting_for" not in st.session_state:
    st.session_state.waiting_for = "goal"


# ------------------------------------
# CHAT DISPLAY
# ------------------------------------
def display_message(role, content):
    if role == "assistant":
        st.markdown(
            f"<div class='assistant-box'><b>Assistant:</b> {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div class='user-box'><b>You:</b> {content}</div>", unsafe_allow_html=True)


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ------------------------------------
# AGENT RESPONSE HANDLER
# ------------------------------------
def assistant_reply(text):
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.query_params = st.query_params  # to refresh UI


def generate_schedule(goal, topics, hours_dict):
    df_topics = pd.DataFrame(topics, columns=["Topic", "Difficulty"])
    df_topics["Estimated_Hours"] = df_topics["Difficulty"] * 1.5

    days = list(hours_dict.keys())
    schedule = []

    topic_idx = 0
    remaining = df_topics["Estimated_Hours"].values.copy()

    for day in days:
        hrs = hours_dict[day]

        while hrs > 0 and topic_idx < len(df_topics):
            needed = remaining[topic_idx]

            if needed <= hrs:
                schedule.append(
                    [day, df_topics.iloc[topic_idx]["Topic"], needed])
                hrs -= needed
                topic_idx += 1
            else:
                schedule.append([day, df_topics.iloc[topic_idx]["Topic"], hrs])
                remaining[topic_idx] -= hrs
                hrs = 0

        # Add revision if difficult
        if topic_idx > 0:
            if df_topics.iloc[topic_idx - 1]["Difficulty"] >= 4 and hrs >= 0.5:
                schedule.append([day, "Revision Session", 0.5])

    df_schedule = pd.DataFrame(schedule, columns=["Day", "Task", "Hours"])
    return df_schedule


# ------------------------------------
# USER INPUT HANDLING
# ------------------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Step 1: Ask for Goal
    if st.session_state.waiting_for == "goal":
        st.session_state.goal = user_input
        st.session_state.waiting_for = "topics"
        assistant_reply(
            "Great! Now please list the topics and their difficulty (1–5). Example:\n\n`Stacks - 3, Trees - 5, Graphs - 4`")

    # Step 2: Get Topics
    elif st.session_state.waiting_for == "topics":
        try:
            raw = [t.strip() for t in user_input.split(",")]
            topic_list = []
            for item in raw:
                name, diff = item.split("-")
                topic_list.append((name.strip(), int(diff.strip())))

            st.session_state.topics = topic_list
            st.session_state.waiting_for = "hours"
            assistant_reply(
                "Awesome! Now tell me how many hours you can study **each day**.\n\nExample:\n`Mon 2, Tue 1, Wed 3, Thu 2, Fri 2, Sat 4, Sun 3`")

        except:
            assistant_reply(
                "Please follow the format: `Topic - Difficulty` separated by commas.")

    # Step 3: Get Hours per Day
    elif st.session_state.waiting_for == "hours":
        try:
            raw = [t.strip() for t in user_input.split(",")]
            hours_dict = {}
            for item in raw:
                day, hr = item.split()
                hours_dict[day.capitalize()] = float(hr)

            st.session_state.hours = hours_dict

            # All data collected → Generate plan
            plan = generate_schedule(
                st.session_state.goal,
                st.session_state.topics,
                st.session_state.hours
            )

            assistant_reply(
                "Your study plan is ready! 🎉 Scroll down to see it.")

            st.session_state.waiting_for = "done"

        except:
            assistant_reply("Please follow the format: `Mon 2, Tue 1, Wed 3`")


# DISPLAY PLAN
if st.session_state.waiting_for == "done":
    st.write("### 📅 Your Study Schedule")
    plan = generate_schedule(
        st.session_state.goal,
        st.session_state.topics,
        st.session_state.hours
    )
    st.dataframe(plan)
