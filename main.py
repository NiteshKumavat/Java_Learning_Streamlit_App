import json
from pathlib import Path
import streamlit as st

DATA_FILE = Path(__file__).parent / "data.json"

@st.cache_data
def load_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def show_code(code):
    st.code(code, language="java")

def show_topic(topic):
    st.header(topic.get("name", "Untitled Topic"))
    if topic.get("explanation"):
        st.markdown("### Explanation")
        st.write(topic["explanation"])
    if topic.get("code"):
        st.markdown("### Code")
        show_code(topic["code"])
    points = topic.get("points_to_remember", [])
    if points:
        st.markdown("### Points to Remember")
        for point in points:
            st.markdown(f"- {point}")
    nested = topic.get("subtopics", [])
    if nested:
        st.markdown("### Subtopics")
        for subtopic in nested:
            with st.expander(subtopic.get("name", "Subtopic")):
                if subtopic.get("explanation"):
                    st.write(subtopic["explanation"])
                if subtopic.get("code"):
                    show_code(subtopic["code"])
                points = subtopic.get("points_to_remember", [])
                if points:
                    st.markdown("**Points to Remember**")
                    for point in points:
                        st.markdown(f"- {point}")

def main():
    st.set_page_config(page_title="Java Fundamentals", page_icon="☕", layout="wide")
    data = load_data()
    st.title(f"☕ {data.get('module', 'Java Learning Guide')}")
    st.write(data.get("learning_objective", ""))
    if data.get("how_to_use_this_guide"):
        st.info(data["how_to_use_this_guide"])

    topics = data.get("subtopics", [])
    names = [t.get("name", f"Topic {i+1}") for i, t in enumerate(topics)]
    if not names:
        st.warning("No topics found in data.json")
        return

    selected_name = st.sidebar.radio("Select a topic", names)
    index = names.index(selected_name)
    st.sidebar.progress((index + 1) / len(names))
    st.sidebar.caption(f"Topic {index + 1} of {len(names)}")
    show_topic(topics[index])

    projects = data.get("practical_projects", [])
    if projects:
        st.divider()
        st.header("🚀 Practical Projects")
        for project in projects:
            with st.expander(project.get("project_name", "Project")):
                st.write(project.get("description", ""))
                if project.get("algorithm"):
                    st.markdown("### Algorithm")
                    st.write(project["algorithm"])
                if project.get("implementation_code"):
                    st.markdown("### Implementation")
                    show_code(project["implementation_code"])

if __name__ == "__main__":
    main()