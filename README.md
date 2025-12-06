# Study_Planner_Assisstant
A Streamlit web app that helps you generate a personalized study schedule based on your academic goals, topics, difficulty levels, and available study hours.

# Features

Set Your Goal: Enter your academic goal (e.g., "Prepare for Data Structures Midterm").
Add Topics: Add multiple topics with difficulty levels (1–5) dynamically.
Set Study Hours: Specify available study hours for each day of the week.
Generate Schedule: Get a clear, structured study plan with time allocated per topic and revision sessions for difficult topics.

# Installation

Clone the repository:
git clone https://github.com/safiyah-asif/study-planner-assistant.git
cd study-planner-assistant

# Create a virtual environment and activate it:

python -m venv .venv
### For Windows
.venv\Scripts\activate
### macOS/Linux
source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py

# How to Use

Open the app in your browser.

Step 1: Enter your academic goal.

Step 2: Add your study topics and set difficulty for each.

Step 3: Enter your available study hours for each day and plan duration.

Step 4: Click Generate Study Plan to see your personalized schedule.

# Built With

### Streamlit
 – For interactive web interface

### Pandas
 – For data handling and scheduling logic
