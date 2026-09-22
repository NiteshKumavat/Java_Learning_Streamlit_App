import json
from pathlib import Path

import streamlit as st


DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_json_files():
    files = {}
    errors = {}

    for file_path in sorted(DATA_DIR.glob("*.json")):
        try:
            with file_path.open("r", encoding="utf-8") as file:
                files[file_path.name] = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            errors[file_path.name] = str(error)

    return files, errors


def render_value(label, value, level=0):
    if isinstance(value, dict):
        if label:
            st.markdown(f"#### {label.replace('_', ' ').title()}")

        for child_label, child_value in value.items():
            render_value(child_label, child_value, level + 1)
        return

    if isinstance(value, list):
        if label:
            st.markdown(f"#### {label.replace('_', ' ').title()}")
        for item in value:
            if isinstance(item, (dict, list)):
                st.json(item, expanded=False)
            else:
                st.markdown(f"- {item}")
        return

    if label in {"code", "solution", "implementation"}:
        st.code(str(value), language="java")
    elif label:
        st.markdown(f"**{label.replace('_', ' ').title()}:** {value}")
    else:
        st.write(value)


def render_learning_data(data):
    if not isinstance(data, dict):
        render_value("", data)
        return

    for section_name, section_data in data.items():
        if section_name == "topics" and isinstance(section_data, dict):
            st.header("Topics")
            for topic_name, topic_data in section_data.items():
                with st.expander(topic_name, expanded=False):
                    render_value("", topic_data)
        elif isinstance(section_data, dict):
            with st.expander(section_name, expanded=True):
                render_value("", section_data)
        else:
            render_value(section_name, section_data)


def main():
    st.set_page_config(
        page_title="Java Learning Hub",
        page_icon="☕",
        layout="wide",
    )

    files, errors = load_json_files()

    st.title("Java Learning Hub")
    st.caption("Browse the complete learning content stored in the data folder.")

    if not files and not errors:
        st.error(f"No JSON files were found in {DATA_DIR}.")
        return

    total_items = sum(len(data) if isinstance(data, dict) else 1 for data in files.values())
    overview_columns = st.columns(2)
    overview_columns[0].metric("JSON files", len(files))
    overview_columns[1].metric("Top-level sections", total_items)

    if errors:
        with st.expander("Files that could not be loaded"):
            for file_name, error in errors.items():
                st.error(f"{file_name}: {error}")

    if not files:
        return

    st.sidebar.header("Learning content")
    selected_file = st.sidebar.selectbox("Choose a file", list(files))
    selected_data = files[selected_file]
    selected_json = json.dumps(selected_data, indent=2, ensure_ascii=False)

    st.sidebar.download_button(
        "Download selected JSON",
        data=selected_json,
        file_name=selected_file,
        mime="application/json",
        use_container_width=True,
    )

    st.subheader(selected_file.removesuffix(".json").replace("_", " ").title())
    render_learning_data(selected_data)


if __name__ == "__main__":
    main()


