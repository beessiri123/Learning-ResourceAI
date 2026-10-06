import streamlit as st
import ollama
import json

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Learning Resource AI",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 Learning Resource AI")

st.subheader(
    "Personalized Learning Resource Recommendation System"
)

st.write(
    "Enter your learning preferences and our AI will "
    "recommend resources based on your skill level, "
    "learning goal and preferred difficulty."
)

st.divider()

# --------------------------------------------------
# LEARNING RESOURCE DATABASE
# --------------------------------------------------
# The AI chooses from these resources.
# This prevents the model from inventing random URLs.

resources = [
    {
        "id": 1,
        "title": "Python Official Documentation",
        "topic": "Python",
        "difficulty": "Moderate",
        "type": "Documentation",
        "url": "https://docs.python.org/3/"
    },
    {
        "id": 2,
        "title": "W3Schools Python Tutorial",
        "topic": "Python",
        "difficulty": "Easy",
        "type": "Tutorial",
        "url": "https://www.w3schools.com/python/"
    },
    {
        "id": 3,
        "title": "freeCodeCamp Python",
        "topic": "Python",
        "difficulty": "Easy",
        "type": "Course",
        "url": "https://www.freecodecamp.org/"
    },
    {
        "id": 4,
        "title": "Kaggle Python Course",
        "topic": "Python",
        "difficulty": "Moderate",
        "type": "Course",
        "url": "https://www.kaggle.com/learn/python"
    },
    {
        "id": 5,
        "title": "Kaggle Pandas Course",
        "topic": "Data Science",
        "difficulty": "Moderate",
        "type": "Course",
        "url": "https://www.kaggle.com/learn/pandas"
    },
    {
        "id": 6,
        "title": "Kaggle Data Visualization",
        "topic": "Data Science",
        "difficulty": "Easy",
        "type": "Course",
        "url": "https://www.kaggle.com/learn/data-visualization"
    },
    {
        "id": 7,
        "title": "Kaggle Intro to Machine Learning",
        "topic": "Machine Learning",
        "difficulty": "Moderate",
        "type": "Course",
        "url": "https://www.kaggle.com/learn/intro-to-machine-learning"
    },
    {
        "id": 8,
        "title": "Kaggle Intermediate Machine Learning",
        "topic": "Machine Learning",
        "difficulty": "Difficult",
        "type": "Course",
        "url": "https://www.kaggle.com/learn/intermediate-machine-learning"
    },
    {
        "id": 9,
        "title": "Scikit-learn User Guide",
        "topic": "Machine Learning",
        "difficulty": "Difficult",
        "type": "Documentation",
        "url": "https://scikit-learn.org/stable/user_guide.html"
    },
    {
        "id": 10,
        "title": "NumPy Documentation",
        "topic": "Data Science",
        "difficulty": "Moderate",
        "type": "Documentation",
        "url": "https://numpy.org/doc/stable/"
    },
    {
        "id": 11,
        "title": "Pandas Documentation",
        "topic": "Data Science",
        "difficulty": "Difficult",
        "type": "Documentation",
        "url": "https://pandas.pydata.org/docs/"
    },
    {
        "id": 12,
        "title": "SQLBolt",
        "topic": "SQL",
        "difficulty": "Easy",
        "type": "Interactive Tutorial",
        "url": "https://sqlbolt.com/"
    }
]

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

st.header("👤 Learner Profile")

col1, col2 = st.columns(2)

with col1:

    topic = st.selectbox(
        "What do you want to learn?",
        [
            "Python",
            "Data Science",
            "Machine Learning",
            "SQL"
        ]
    )

    skill_level = st.selectbox(
        "What is your current skill level?",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    difficulty = st.selectbox(
        "Preferred difficulty",
        [
            "Automatic",
            "Easy",
            "Moderate",
            "Difficult"
        ]
    )

with col2:

    learning_goal = st.text_area(
        "What is your learning goal?",
        placeholder=(
            "Example: I want to learn Python "
            "for Data Science and get an internship."
        )
    )

    resource_type = st.selectbox(
        "Preferred resource type",
        [
            "Any",
            "Course",
            "Tutorial",
            "Documentation",
            "Interactive Tutorial"
        ]
    )

    study_time = st.selectbox(
        "Available study time",
        [
            "1-2 hours per week",
            "3-5 hours per week",
            "5-10 hours per week",
            "10+ hours per week"
        ]
    )

# --------------------------------------------------
# RECOMMENDATION BUTTON
# --------------------------------------------------

if st.button(
    "🤖 Generate Personalized Recommendations",
    use_container_width=True
):

    if not learning_goal.strip():

        st.warning(
            "Please enter your learning goal."
        )

    else:

        # ------------------------------------------
        # Prepare resource information for Ollama
        # ------------------------------------------

        resource_text = ""

        for resource in resources:

            resource_text += (
                f"ID: {resource['id']}\n"
                f"Title: {resource['title']}\n"
                f"Topic: {resource['topic']}\n"
                f"Difficulty: {resource['difficulty']}\n"
                f"Type: {resource['type']}\n\n"
            )

        # ------------------------------------------
        # Difficulty instruction
        # ------------------------------------------

        if difficulty == "Automatic":

            difficulty_instruction = """
Choose the appropriate difficulty yourself based
on the learner's skill level and learning goal.

You may recommend Easy, Moderate and Difficult
resources in a progression.
"""

        else:

            difficulty_instruction = f"""
The learner prefers {difficulty} resources.
Prioritize resources with this difficulty.
"""

        # ------------------------------------------
        # Ollama Prompt
        # ------------------------------------------

        prompt = f"""
You are an intelligent personalized learning
resource recommendation system.

Your task is to recommend learning resources
from the provided resource database.

LEARNER INFORMATION:

Topic:
{topic}

Current Skill Level:
{skill_level}

Learning Goal:
{learning_goal}

Preferred Resource Type:
{resource_type}

Available Study Time:
{study_time}

{difficulty_instruction}

RESOURCE DATABASE:

{resource_text}

IMPORTANT RULES:

1. Recommend ONLY resources that exist in the database.
2. Never invent resource IDs.
3. Never invent URLs.
4. Consider the learner's skill level.
5. Consider the learner's learning goal.
6. Consider the preferred difficulty.
7. Give a personalized reason for every recommendation.
8. Recommend up to 5 resources.
9. Sort recommendations from most suitable to least suitable.
10. If the learner is a beginner, avoid recommending
   too many difficult resources.

Return ONLY valid JSON in this exact structure:

{{
    "summary": "short explanation of the recommendation",
    "recommendations": [
        {{
            "id": 1,
            "difficulty": "Easy",
            "reason": "why this resource is suitable"
        }}
    ]
}}
"""

        # ------------------------------------------
        # Call Ollama
        # ------------------------------------------

        with st.spinner(
            "🤖 AI is analyzing your learning profile..."
        ):

            try:

                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    format="json"
                )

                result = json.loads(
                    response["message"]["content"]
                )

                recommendations = result.get(
                    "recommendations",
                    []
                )

                summary = result.get(
                    "summary",
                    ""
                )

                # ----------------------------------
                # Display AI summary
                # ----------------------------------

                st.divider()

                st.header("🎯 Your Personalized Learning Plan")

                st.info(summary)

                # ----------------------------------
                # Display recommendations
                # ----------------------------------

                if not recommendations:

                    st.warning(
                        "No suitable resources were found."
                    )

                else:

                    st.subheader(
                        "📚 Recommended Resources"
                    )

                    for index, recommendation in enumerate(
                        recommendations,
                        start=1
                    ):

                        resource_id = recommendation.get(
                            "id"
                        )

                        # Find resource in database
                        resource = next(
                            (
                                r for r in resources
                                if r["id"] == resource_id
                            ),
                            None
                        )

                        if resource is None:
                            continue

                        # Difficulty
                        resource_difficulty = resource[
                            "difficulty"
                        ]

                        # Difficulty icon
                        if resource_difficulty == "Easy":
                            difficulty_icon = "🟢"

                        elif resource_difficulty == "Moderate":
                            difficulty_icon = "🟡"

                        else:
                            difficulty_icon = "🔴"

                        # --------------------------------
                        # Resource card
                        # --------------------------------

                        with st.container(
                            border=True
                        ):

                            st.subheader(
                                f"{index}. "
                                f"{resource['title']}"
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:

                                st.write(
                                    f"**Topic:** "
                                    f"{resource['topic']}"
                                )

                            with col2:

                                st.write(
                                    f"**Type:** "
                                    f"{resource['type']}"
                                )

                            with col3:

                                st.write(
                                    f"**Difficulty:** "
                                    f"{difficulty_icon} "
                                    f"{resource_difficulty}"
                                )

                            st.write(
                                "**Why this is "
                                "recommended:**"
                            )

                            st.write(
                                recommendation.get(
                                    "reason",
                                    "Suitable for your learning profile."
                                )
                            )

                            st.link_button(
                                "📖 Open Resource",
                                resource["url"]
                            )

            except Exception as e:

                st.error(
                    "Unable to connect to Ollama."
                )

                st.code(
                    str(e)
                )

                st.info(
                    "Make sure Ollama is installed, "
                    "the model is downloaded, and "
                    "Ollama is running."
                )