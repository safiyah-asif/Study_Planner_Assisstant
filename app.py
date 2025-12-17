import streamlit as st
import pandas as pd

st.set_page_config(page_title="Study Planner Assistant",
                   page_icon="📚", layout="wide")

st.markdown(
    """
    <style>
    body {
        background:
            radial-gradient(circle at 20% 50%, rgba(76, 175, 80, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(129, 199, 132, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(76, 175, 80, 0.2) 0%, transparent 50%),
            linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
        background-size: 400px 400px, 300px 300px, 500px 500px, 100% 100%;
        background-attachment: fixed;
        animation: gradientShift 20s ease infinite;
        color: white;
        min-height: 100vh;
    }

    @keyframes gradientShift {
        0% {
            background-position: 0% 0%, 0% 0%, 0% 0%, 0% 0%;
        }
        50% {
            background-position: 100% 100%, 100% 100%, 100% 100%, 0% 0%;
        }
        100% {
            background-position: 0% 0%, 0% 0%, 0% 0%, 0% 0%;
        }
    }

    .main {
        background: linear-gradient(145deg,
            rgba(255, 255, 255, 0.95) 0%,
            rgba(255, 255, 255, 0.9) 50%,
            rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin: 20px auto;
        box-shadow:
            0 8px 32px rgba(76, 175, 80, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 1000px;
        position: relative;
    }

    .main::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4CAF50, #81C784, #4CAF50);
        border-radius: 15px 15px 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Title
st.markdown("<h1 style='text-align:center;'>📚 Study Session Planner – AI Assistant</h1>",
            unsafe_allow_html=True)
st.write("Welcome! I will help you generate a personalized study schedule based on your goals, topics, and available time.")


# SESSION VARIABLES

if "goal" not in st.session_state:
    st.session_state.goal = None

if "topics" not in st.session_state:
    st.session_state.topics = []

if "hours" not in st.session_state:
    st.session_state.hours = None

if "step" not in st.session_state:
    st.session_state.step = "goal"   # goal → topics → hours → done


# ------------------------- STEP 1: GOAL INPUT --------------------

if st.session_state.step == "goal":
    st.subheader("🎯 Step 1: What is your academic goal?")
    goal = st.text_input("Example: Prepare for Data Structures Midterm")

    if st.button("Next ➡"):
        if goal.strip():
            st.session_state.goal = goal
            st.session_state.step = "topics"
        else:
            st.error("Please enter a goal!")

# ------------------- STEP 2: DYNAMIC TOPICS --------------------

if st.session_state.step == "topics":
    st.subheader("📘 Step 2: Add Topics with Individual Difficulty")

    # Initialize topics list in session_state
    if "topics" not in st.session_state:
        st.session_state.topics = []

    # Add a new empty topic
    if st.button("➕ Add New Topic"):
        # add a new topic that contains both
        st.session_state.topics.append({"name": "", "difficulty": 3})

    # Display all topics with input and slider
    if st.session_state.topics:
        # enumerate for index to an iterable value
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
                    st.experimental_rerun()  # not working throwing error

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

# ---------------------- STEP 3: HOURS INPUT ---------------------

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


# ------------------ STEP 4: GENERATE SCHEDULE -------------------

def generate_schedule(goal, topics, hours_dict):
    # Create a DataFrame for topics
    df_topics = pd.DataFrame(topics, columns=["Topic", "Difficulty"])

    total_difficulty = df_topics["Difficulty"].sum()  # Example: 3 + 5 = 8
    # Math: 3 / 8 = 0.375 , Physics: 5 / 8 = 0.625
    df_topics["Weight"] = df_topics["Difficulty"] / total_difficulty

    # Calculate total available hours
    total_hours = sum(hours_dict.values())

    # Allocate hours proportionally based on weight
    df_topics["Hours_Allocated"] = df_topics["Weight"] * total_hours

    # Generate the schedule
    schedule = []
    topic_idx = 0
    remaining_hours = df_topics["Hours_Allocated"].values.copy()

    for day, available_hours in hours_dict.items():
        hrs = available_hours

        while hrs > 0 and topic_idx < len(df_topics):
            need = remaining_hours[topic_idx]

            if need <= hrs:
                schedule.append(
                    [day, df_topics.iloc[topic_idx]["Topic"], need])
                hrs -= need
                topic_idx += 1
            else:
                schedule.append([day, df_topics.iloc[topic_idx]["Topic"], hrs])
                remaining_hours[topic_idx] -= hrs
                hrs = 0

        # Add revision time for difficult topics if time permits
        if topic_idx > 0 and df_topics.iloc[topic_idx - 1]["Difficulty"] >= 4 and hrs >= 0.5:
            schedule.append([day, "Revision Session", 0.5])
            hrs -= 0.5 

    # Create a DataFrame for the schedule
    df_schedule = pd.DataFrame(schedule, columns=["Day", "Task", "Hours"])
    return df_schedule


if st.session_state.step == "done":
    st.header("📅 Your Personalized Study Schedule")

    df_plan = generate_schedule(
        st.session_state.goal,
        st.session_state.topics,
        st.session_state.hours
    )

    st.success(f"Goal: **{st.session_state.goal}**")
    st.dataframe(df_plan, use_container_width=True)
