import streamlit as st
import pandas as pd

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="Study Planner Assistant",
                   page_icon="📚", layout="wide")

# Title
st.markdown("<h1 style='text-align:center;'>📚 Study Session Planner – AI Assistant</h1>",
            unsafe_allow_html=True)
st.write("Welcome! I will help you generate a personalized study schedule based on your goals, topics, and available time.")


# ------------------------------------------------
# SESSION VARIABLES
# ------------------------------------------------
if "goal" not in st.session_state:
    st.session_state.goal = None

if "topics" not in st.session_state:
    st.session_state.topics = []

if "hours" not in st.session_state:
    st.session_state.hours = None

if "step" not in st.session_state:
    st.session_state.step = "goal"   # goal → topics → hours → done


# ================================================================
# ------------------------- STEP 1: GOAL INPUT --------------------
# ================================================================
if st.session_state.step == "goal":
    st.subheader("🎯 Step 1: What is your academic goal?")
    goal = st.text_input("Example: Prepare for Data Structures Midterm")

    if st.button("Next ➡"):
        if goal.strip():
            st.session_state.goal = goal
            st.session_state.step = "topics"
        else:
            st.error("Please enter a goal!")


# ================================================================
# ------------------- STEP 2: DYNAMIC TOPICS --------------------
# ================================================================
if st.session_state.step == "topics":
    st.subheader("📘 Step 2: Add Topics with Individual Difficulty")

    # Initialize topics list in session_state
    if "topics" not in st.session_state:
        st.session_state.topics = []

    # Add a new empty topic
    if st.button("➕ Add New Topic"):
        st.session_state.topics.append({"name": "", "difficulty": 3})

    # Display all topics with input and slider
    if st.session_state.topics:
        for idx, topic in enumerate(st.session_state.topics):
            cols = st.columns([3, 2, 1])
            with cols[0]:
                topic["name"] = st.text_input(
                    f"Topic {idx+1} Name",
                    value=topic["name"],
                    key=f"topic_name_{idx}"
                )
            with cols[1]:
                topic["difficulty"] = st.slider(
                    "Difficulty",
                    min_value=1,
                    max_value=5,
                    value=topic["difficulty"],
                    key=f"topic_diff_{idx}"
                )
            with cols[2]:
                if st.button("❌ Remove", key=f"remove_{idx}"):
                    st.session_state.topics.pop(idx)
                    st.experimental_rerun()  # Refresh the page to remove the topic

        st.write("### 📂 Topics Added")
        df_top = pd.DataFrame(
            [(t["name"], t["difficulty"]) for t in st.session_state.topics],
            columns=["Topic", "Difficulty"]
        )
        st.dataframe(df_top, use_container_width=True)

        if st.button("Next Step ➡"):
            # Filter out empty topic names
            st.session_state.topics = [
                (t["name"], t["difficulty"]) for t in st.session_state.topics if t["name"].strip()
            ]
            if st.session_state.topics:
                st.session_state.step = "hours"
            else:
                st.error("Please add at least one topic!")


# ================================================================
# ---------------------- STEP 3: HOURS INPUT ---------------------
# ================================================================
if st.session_state.step == "hours":
    st.subheader("🕒 Step 3: Available Study Hours")

    # Ask user for duration of the plan
    plan_duration = st.number_input(
        "How many weeks do you want to plan for?",
        min_value=1,
        max_value=2,
        value=1,
        step=1
    )

    st.write("Enter your available study hours for each day.")

    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]

    # Initialize the hours dict
    if "hours_dict" not in st.session_state:
        st.session_state.hours_dict = {}

    # Loop over each week
    for week in range(1, plan_duration + 1):
        st.markdown(f"### Week {week}")
        cols = st.columns(7)
        for idx, day in enumerate(days):
            # Use a unique key for each day in each week
            key = f"week{week}_{day}"
            default_val = st.session_state.hours_dict.get(key, 2.0)
            st.session_state.hours_dict[key] = cols[idx].number_input(
                day,
                min_value=0.0,
                max_value=10.0,
                value=default_val,
                key=key
            )

    # When ready, save to session state and move to next step
    if st.button("Generate Study Plan 🎉"):
        st.session_state.hours = st.session_state.hours_dict
        st.session_state.step = "done"


# ================================================================
# ------------------ STEP 4: GENERATE SCHEDULE -------------------
# ================================================================
def generate_schedule(goal, topics, hours_dict):
    df_topics = pd.DataFrame(topics, columns=["Topic", "Difficulty"])
    df_topics["Hours_Needed"] = df_topics["Difficulty"] * 1.5

    schedule = []
    remaining = df_topics["Hours_Needed"].values.copy()
    topic_idx = 0

    for day, available in hours_dict.items():
        hrs = available

        while hrs > 0 and topic_idx < len(df_topics):
            need = remaining[topic_idx]

            if need <= hrs:
                schedule.append(
                    [day, df_topics.iloc[topic_idx]["Topic"], need])
                hrs -= need
                topic_idx += 1
            else:
                schedule.append([day, df_topics.iloc[topic_idx]["Topic"], hrs])
                remaining[topic_idx] -= hrs
                hrs = 0

        # revision time for difficult topics
        if topic_idx > 0 and df_topics.iloc[topic_idx - 1]["Difficulty"] >= 4 and hrs >= 0.5:
            schedule.append([day, "Revision Session", 0.5])

    df = pd.DataFrame(schedule, columns=["Day", "Task", "Hours"])
    return df


# SHOW OUTPUT
if st.session_state.step == "done":
    st.header("📅 Your Personalized Study Schedule")

    df_plan = generate_schedule(
        st.session_state.goal,
        st.session_state.topics,
        st.session_state.hours
    )

    st.success(f"Goal: **{st.session_state.goal}**")
    st.dataframe(df_plan, use_container_width=True)
