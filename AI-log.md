# 🤖 AI Development Log

# 🧠 Overview

Throughout this project, AI assistance played a major role in the entire development lifecycle.  
Some of it includes:

✨ I had an idea of techstack and working then I used Chatgpt to polish it.

✨ Writing the scheduling logic

✨ Generating the CSV output logic

✨ Formatting documentation (README, MD files, Use Cases, TestPlan, Release Roadmap)

### **Benefits**

- **Massive time savings** during coding, design, and documentation.
- Helped generate **cleaner explanations**, tables, and markdown.
- Assisted in tricky debugging.
- Helped translate requirements into **flowcharts + architecture diagrams**.
- You can use it for **enhancing** your thoughts.

### **Risks**

- AI-generated code sometimes contained:
  - Hidden logical issues (e.g., unbalanced topic allocation)
  - Overly simplified logic for real-world use
  - Incorrect assumptions about expected study plan behavior
- AI-written documentation could sound too generic and must be out of your scope.
- Architecture suggestions sometimes need alignment with actual implemented code.
- Overreliance can reduce understanding if code is not reviewed manually.

# 🤖 AI Tools Used

| Tool             | Purpose                                          | Notes                                                                                    |
| ---------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| _ChatGPT_        | Main assistant for coding, debugging, Formatting | Used extensively for fixing code according to my need, fixing logic, formatting MD files |
| _lovable_        | UI/UX and logic explanation for future prototype | Not part of this MVP                                                                     |
| _Github Copilot_ | For Plan debugging                               | Only for a function, fixing logic                                                        |

# Chat gpt prompt

### For TechStack

"I've only 24 hours to build a project of AI , I want to create a study planner agent in which I also want a good UI what is the preferable techstack. Now the problem is recently I've been working on python and for UI streamlit, so now how can I build a good UI with this."

"But how can I make customize UI, can I customize my UI in chainlit , streamlit cuz in streamlit we can make multiple pages"

### For polishing

"""
I provided a code along this prompt:
I want a good interactive UI and not hardcoded user will give input according to that the agent will reply"""

"give slider for asking difficulty level and also mention high and low"

### Error solving

"if st.session_state.step == "hours":

    st.subheader("🕒 Step 3: Available Study Hours This Week")

    st.write("Enter how many hours you can study each day.")

    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    hours_dict = {}

    cols = st.columns(7)
    for idx, day in enumerate(days):
        hours_dict[day] = cols[idx].number_input(
            day, min_value=0.0, max_value=10.0, value=2.0)

    if st.button("Generate Study Plan 🎉"):
        st.session_state.hours = hours_dict
        st.session_state.step = "done"

first ask user for how what duration he/she wants the plan and then asked for the free time time according

in this if user wants for 2 weeks maybe there are different free slots for both mondays"

# Lovable prompt

"This is my current projects ui i have been asked to imagine how an upgraded refined version of this fully finished would look like im tasked to submit this in 2 hours i tried to find a template from canva or visily but i cant im done tired building this project alone can you help me build a template of this project but more advanced in every way basically my project is a Study session planner it asks user for whta price, fuel type, and other tags of his choices are then fetches data from the internet and brings relevant data from there which are in form of car suggestions and it also ranks them and shows the scoring acc to each of the preference added it take inputs from user his academic goals , topics , how many weeks they have(1-2) and then generate a plan in a table (using pandas) what could be future things that could be added and i want to imagine that in ui as an future mvp of my project I have some ideas 1.currently I have only 1-2 weeks rn we can add more flexibility in time frame 2.I will also add a feature of subtopics of the topic Right now I just have this"
Along with my current projects.

# Github Copilot prompt

"my planner is not perfect , If it is ignoring the topics if hours are finished instead of dividing time accordingly
Every topic should be covered in a limited time frame
No topic should be ignored
Topic with more difficulty level should be given more time"

In response: It fixed my plan scheduling.
