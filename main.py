
import streamlit as st
import json
from pathlib import Path
import random


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Java Learning Hub",
    page_icon="☕",
    layout="wide"
)


# ============================================================
# DATA CONFIGURATION
# ============================================================

DATA_DIR = Path("data")

TOPICS = {
    "Basic Java": "basic_java.json",
    "Arrays": "array.json",
    "Strings": "strings.json",
    "Recursion": "recursion.json",
    "Java Collections": "java_collections.json",
    "File Handling": "file_handling.json",
    "Graph": "graph.json",
    "Multithreading & Concurrency":
        "Multithreading_and_Concurrency.json"
}


# ============================================================
# LOAD JSON
# ============================================================

@st.cache_data
def load_data(filename):

    file_path = DATA_DIR / filename

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        return []

    except json.JSONDecodeError:

        st.error(f"Invalid JSON file: {filename}")

        return []


# ============================================================
# GET ALL DATA
# ============================================================

def get_all_data():

    all_data = []

    for topic, filename in TOPICS.items():

        data = load_data(filename)

        if isinstance(data, list):

            for item in data:

                if isinstance(item, dict):

                    all_data.append(
                        {
                            "topic": topic,
                            "data": item
                        }
                    )

    return all_data


# ============================================================
# DYNAMIC VALUE RENDERER
# ============================================================

def render_value(key, value, level=0):

    """
    Dynamically render different JSON value types.
    """

    if value is None:
        return

    # --------------------------------------------
    # String
    # --------------------------------------------

    if isinstance(value, str):

        # Code-related fields
        code_fields = [
            "code",
            "java_code",
            "example_code",
            "implementation",
            "solution",
            "program"
        ]

        if key.lower() in code_fields:

            st.code(
                value,
                language="java"
            )

        else:

            st.write(value)

        return

    # --------------------------------------------
    # Number / Boolean
    # --------------------------------------------

    if isinstance(value, (int, float, bool)):

        st.write(value)

        return

    # --------------------------------------------
    # List
    # --------------------------------------------

    if isinstance(value, list):

        for index, item in enumerate(value):

            if isinstance(item, dict):

                with st.container():

                    for sub_key, sub_value in item.items():

                        st.markdown(
                            f"**{format_key(sub_key)}**"
                        )

                        render_value(
                            sub_key,
                            sub_value,
                            level + 1
                        )

            elif isinstance(item, str):

                st.markdown(f"• {item}")

            else:

                st.write(item)

        return

    # --------------------------------------------
    # Dictionary
    # --------------------------------------------

    if isinstance(value, dict):

        for sub_key, sub_value in value.items():

            st.markdown(
                f"**{format_key(sub_key)}**"
            )

            render_value(
                sub_key,
                sub_value,
                level + 1
            )

        return


# ============================================================
# FORMAT JSON KEYS
# ============================================================

def format_key(key):

    return (
        key.replace("_", " ")
           .replace("-", " ")
           .title()
    )


# ============================================================
# RENDER SINGLE ITEM
# ============================================================

def render_item(item):

    if not isinstance(item, dict):
        st.write(item)
        return

    # --------------------------------------------
    # Title
    # --------------------------------------------

    title = item.get(
        "title",
        item.get(
            "name",
            "Learning Resource"
        )
    )

    st.subheader(title)

    # --------------------------------------------
    # Difficulty
    # --------------------------------------------

    if "difficulty" in item:

        difficulty = item["difficulty"]

        if str(difficulty).lower() == "easy":

            st.success(f"Difficulty: {difficulty}")

        elif str(difficulty).lower() == "medium":

            st.warning(f"Difficulty: {difficulty}")

        elif str(difficulty).lower() == "hard":

            st.error(f"Difficulty: {difficulty}")

        else:

            st.info(f"Difficulty: {difficulty}")

    # --------------------------------------------
    # Concept
    # --------------------------------------------

    if "concept" in item:

        st.markdown(
            f"**Concept:** {item['concept']}"
        )

    # --------------------------------------------
    # Description
    # --------------------------------------------

    if "description" in item:

        st.markdown("### Description")

        st.write(item["description"])

    # --------------------------------------------
    # Definition
    # --------------------------------------------

    if "definition" in item:

        st.markdown("### Definition")

        st.write(item["definition"])

    # --------------------------------------------
    # Question
    # --------------------------------------------

    if "question" in item:

        st.markdown("### Question")

        st.write(item["question"])

    # --------------------------------------------
    # Algorithm
    # --------------------------------------------

    if "algorithm" in item:

        st.markdown("### Algorithm")

        algorithm = item["algorithm"]

        if isinstance(algorithm, list):

            for index, step in enumerate(
                algorithm,
                start=1
            ):

                st.write(
                    f"**{index}.** {step}"
                )

        else:

            st.write(algorithm)

    # --------------------------------------------
    # Complexity
    # --------------------------------------------

    if (
        "time_complexity" in item
        or
        "space_complexity" in item
    ):

        st.markdown("### Complexity")

        col1, col2 = st.columns(2)

        if "time_complexity" in item:

            col1.metric(
                "Time Complexity",
                item["time_complexity"]
            )

        if "space_complexity" in item:

            col2.metric(
                "Space Complexity",
                item["space_complexity"]
            )

    # --------------------------------------------
    # Example
    # --------------------------------------------

    if "example" in item:

        st.markdown("### Example")

        example = item["example"]

        if isinstance(example, dict):

            for key, value in example.items():

                st.markdown(
                    f"**{format_key(key)}**"
                )

                if isinstance(value, str):

                    st.code(
                        value,
                        language="text"
                    )

                else:

                    st.write(value)

        else:

            st.write(example)

    # --------------------------------------------
    # Input / Output
    # --------------------------------------------

    if (
        "input" in item
        or
        "output" in item
    ):

        st.markdown("### Input / Output")

        col1, col2 = st.columns(2)

        if "input" in item:

            with col1:

                st.markdown("**Input**")

                st.code(
                    str(item["input"])
                )

        if "output" in item:

            with col2:

                st.markdown("**Output**")

                st.code(
                    str(item["output"])
                )

    # --------------------------------------------
    # Java Code
    # --------------------------------------------

    code_fields = [
        "java_code",
        "code",
        "example_code",
        "implementation",
        "solution",
        "program"
    ]

    for field in code_fields:

        if field in item:

            st.markdown(
                f"### {format_key(field)}"
            )

            st.code(
                item[field],
                language="java"
            )

    # --------------------------------------------
    # Notes
    # --------------------------------------------

    if "notes" in item:

        st.markdown("### Notes")

        st.info(item["notes"])

    # --------------------------------------------
    # Remaining fields
    # --------------------------------------------

    known_fields = {
        "title",
        "name",
        "difficulty",
        "concept",
        "description",
        "definition",
        "question",
        "algorithm",
        "time_complexity",
        "space_complexity",
        "example",
        "input",
        "output",
        "java_code",
        "code",
        "example_code",
        "implementation",
        "solution",
        "program",
        "notes"
    }

    remaining_fields = [
        key
        for key in item.keys()
        if key not in known_fields
    ]

    if remaining_fields:

        st.markdown("### Additional Information")

        for key in remaining_fields:

            st.markdown(
                f"**{format_key(key)}**"
            )

            render_value(
                key,
                item[key]
            )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.title("☕ Java Learning Hub")

    st.markdown(
        """
        ### Your personal Java learning platform

        Explore Java fundamentals, data structures,
        algorithms, collections, file handling,
        recursion, graphs and concurrency.
        """
    )

    st.divider()

    # --------------------------------------------
    # Statistics
    # --------------------------------------------

    total_resources = 0

    for filename in TOPICS.values():

        data = load_data(filename)

        if isinstance(data, list):

            total_resources += len(data)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Topics",
        len(TOPICS)
    )

    col2.metric(
        "Resources",
        total_resources
    )

    col3.metric(
        "JSON Files",
        len(TOPICS)
    )

    st.divider()

    # --------------------------------------------
    # Topics
    # --------------------------------------------

    st.subheader("📚 Topics")

    cols = st.columns(4)

    for index, (topic, filename) in enumerate(
        TOPICS.items()
    ):

        data = load_data(filename)

        with cols[index % 4]:

            st.markdown(
                f"### {topic}"
            )

            st.write(
                f"{len(data)} resources"
            )


# ============================================================
# TOPICS PAGE
# ============================================================

def topics_page():

    st.title("📚 Java Topics")

    topic = st.selectbox(
        "Select a topic",
        list(TOPICS.keys())
    )

    data = load_data(
        TOPICS[topic]
    )

    if not data:

        st.warning(
            "No data found for this topic."
        )

        return

    st.markdown(
        f"### {topic}"
    )

    st.write(
        f"Total resources: {len(data)}"
    )

    st.divider()

    # --------------------------------------------
    # Filters
    # --------------------------------------------

    difficulties = []

    for item in data:

        if isinstance(item, dict):

            if "difficulty" in item:

                difficulties.append(
                    str(item["difficulty"])
                )

    if difficulties:

        difficulties = sorted(
            set(difficulties)
        )

        selected_difficulty = st.selectbox(
            "Filter by difficulty",
            ["All"] + difficulties
        )

    else:

        selected_difficulty = "All"

    st.divider()

    # --------------------------------------------
    # Display
    # --------------------------------------------

    for index, item in enumerate(data):

        if (
            selected_difficulty != "All"
            and
            isinstance(item, dict)
            and
            str(
                item.get("difficulty", "")
            ) != selected_difficulty
        ):

            continue

        title = (
            item.get(
                "title",
                item.get(
                    "name",
                    f"Resource {index + 1}"
                )
            )
            if isinstance(item, dict)
            else f"Resource {index + 1}"
        )

        with st.expander(
            f"{index + 1}. {title}"
        ):

            render_item(item)


# ============================================================
# SEARCH PAGE
# ============================================================

def search_page():

    st.title("🔍 Search Java Knowledge")

    query = st.text_input(
        "Search",
        placeholder=(
            "Try: binary search, HashMap, recursion, "
            "thread, graph..."
        )
    )

    if not query:

        st.info(
            "Enter something to search your Java knowledge base."
        )

        return

    query = query.lower()

    results = []

    all_data = get_all_data()

    for entry in all_data:

        topic = entry["topic"]

        item = entry["data"]

        searchable_text = json.dumps(
            item,
            ensure_ascii=False
        ).lower()

        if query in searchable_text:

            results.append(
                (
                    topic,
                    item
                )
            )

    st.write(
        f"Found **{len(results)}** result(s)"
    )

    st.divider()

    if not results:

        st.warning(
            "No matching results found."
        )

        return

    for topic, item in results:

        title = item.get(
            "title",
            item.get(
                "name",
                "Untitled"
            )
        )

        with st.expander(
            f"{title} — {topic}"
        ):

            render_item(item)


# ============================================================
# PRACTICE PAGE
# ============================================================

def practice_page():

    st.title("🧠 Practice Mode")

    all_data = get_all_data()

    questions = []

    for entry in all_data:

        item = entry["data"]

        if isinstance(item, dict):

            if "question" in item:

                questions.append(
                    entry
                )

    if not questions:

        st.warning(
            "No practice questions found in your JSON files."
        )

        st.info(
            """
            Add a `question` field to your JSON data.

            Example:

            {
                "title": "Binary Search",
                "question": "Find the index of 7.",
                "answer": "3"
            }
            """
        )

        return

    # --------------------------------------------
    # Random question
    # --------------------------------------------

    if "practice_question" not in st.session_state:

        st.session_state.practice_question = random.choice(
            questions
        )

    topic, item = st.session_state.practice_question[
        "topic"
    ], st.session_state.practice_question[
        "data"
    ]

    st.markdown(
        f"### {item.get('title', 'Practice Question')}"
    )

    st.caption(
        f"Topic: {topic}"
    )

    st.divider()

    st.markdown(
        "### Question"
    )

    st.write(
        item["question"]
    )

    # --------------------------------------------
    # Input
    # --------------------------------------------

    user_answer = st.text_area(
        "Your Answer"
    )

    # --------------------------------------------
    # Check Answer
    # --------------------------------------------

    if st.button(
        "Check Answer",
        type="primary"
    ):

        correct_answer = str(
            item.get(
                "answer",
                ""
            )
        ).strip().lower()

        user_answer_clean = (
            user_answer
            .strip()
            .lower()
        )

        if (
            correct_answer
            and
            user_answer_clean == correct_answer
        ):

            st.success(
                "Correct! 🎉"
            )

        elif correct_answer:

            st.error(
                "Incorrect. Try again."
            )

        else:

            st.info(
                "This question does not have an answer field."
            )

    # --------------------------------------------
    # Next Question
    # --------------------------------------------

    if st.button(
        "➡️ Next Question"
    ):

        st.session_state.practice_question = random.choice(
            questions
        )

        st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("☕ Java Learning Hub")

st.sidebar.markdown(
    "### Navigation"
)

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Dashboard",
        "📚 Topics",
        "🔍 Search",
        "🧠 Practice"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    "### Topics"
)

for topic in TOPICS:

    data = load_data(
        TOPICS[topic]
    )

    st.sidebar.write(
        f"• {topic}: {len(data)}"
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "🏠 Dashboard":

    dashboard()

elif page == "📚 Topics":

    topics_page()

elif page == "🔍 Search":

    search_page()

elif page == "🧠 Practice":

    practice_page()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "☕ Java Learning Hub • Built with Streamlit"
)