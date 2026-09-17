import streamlit as st
import json
import os
import sys
import io

# 1. Configuration & Page Setup
st.set_page_config(
    page_title="Java Fundamentals Roadmap",
    page_icon="☕",
    layout="wide"
)

DATA_FILE = "data.json"

# Default JSON Content matching the exact structure requested
DEFAULT_JSON = {
    "module": "Java Fundamentals",
    "learning_objective": "Master core Java syntax, control structures, primitive data types, and fundamental object manipulation without framework abstractions.",
    "subtopics": [
        {
            "name": "Variables and Data Types",
            "description": "Primitives (int, double, boolean, char, byte, short, long, float) vs Reference Types. Memory layout (Stack vs Heap).",
            "code_snippet": "public class VariablesDemo {\n    public static void main(String[] args) {\n        int count = 10;\n        double price = 99.99;\n        boolean isActive = true;\n        char grade = 'A';\n        String name = \"Java\";\n        System.out.println(\"Count: \" + count + \", Price: \" + price);\n    }\n}"
        },
        {
            "name": "Operators",
            "description": "Arithmetic (+, -, *, /, %), Relational (==, !=, >, <), Logical (&&, ||, !), Bitwise (&, |, ^), and Assignment operators.",
            "code_snippet": "public class OperatorsDemo {\n    public static void main(String[] args) {\n        int a = 15, b = 4;\n        boolean complexCondition = (a > 10) && (b < 5);\n        System.out.println(\"Remainder: \" + (a % b) + \", Condition: \" + complexCondition);\n    }\n}"
        },
        {
            "name": "Control Flow - Conditionals",
            "description": "Branching execution paths using if, else if, else, and switch statements.",
            "code_snippet": "public class ConditionalsDemo {\n    public static void main(String[] args) {\n        int score = 85;\n        if (score >= 90) {\n            System.out.println(\"Grade A\");\n        } else if (score >= 80) {\n            System.out.println(\"Grade B\");\n        } else {\n            System.out.println(\"Grade C\");\n        }\n    }\n}"
        },
        {
            "name": "Control Flow - Loops",
            "description": "Iterative execution using standard for loops, enhanced for-each loops, while loops, and do-while loops.",
            "code_snippet": "public class LoopsDemo {\n    public static void main(String[] args) {\n        for (int i = 1; i <= 3; i++) {\n            System.out.println(\"For loop count: \" + i);\n        }\n    }\n}"
        },
        {
            "name": "Methods",
            "description": "Modularizing code into functions, parameter passing, return types, and method overloading.",
            "code_snippet": "public class MethodsDemo {\n    public static int add(int a, int b) {\n        return a + b;\n    }\n    public static void main(String[] args) {\n        System.out.println(\"Sum Int: \" + add(5, 10));\n    }\n}"
        },
        {
            "name": "Arrays",
            "description": "Fixed-size, contiguous memory data structures.",
            "algorithms_and_logic": "Linear Traversal, Finding Max/Min elements.",
            "code_snippet": "public class ArraysDemo {\n    public static void main(String[] args) {\n        int[] numbers = {4, 2, 9, 1, 7};\n        int max = numbers[0];\n        for (int num : numbers) {\n            if (num > max) max = num;\n        }\n        System.out.println(\"Max element: \" + max);\n    }\n}"
        },
        {
            "name": "Strings & StringBuilder",
            "description": "String immutability and StringBuilder performance optimization.",
            "code_snippet": "public class StringDemo {\n    public static void main(String[] args) {\n        StringBuilder sb = new StringBuilder(\"Hello\");\n        sb.append(\" World\");\n        System.out.println(sb.toString());\n    }\n}"
        },
        {
            "name": "Type Casting",
            "description": "Implicit conversion (widening) and explicit conversion (narrowing).",
            "code_snippet": "public class CastingDemo {\n    public static void main(String[] args) {\n        double pi = 3.14159;\n        int roundedPi = (int) pi;\n        System.out.println(\"Explicit cast: \" + roundedPi);\n    }\n}"
        },
        {
            "name": "Input/Output",
            "description": "Reading console input using java.util.Scanner and rendering outputs.",
            "code_snippet": "import java.util.Scanner;\n\npublic class IODemo {\n    public static void main(String[] args) {\n        System.out.println(\"Simulated Scanner reading 'Java User'...\");\n        String name = \"Java User\";\n        System.out.println(\"Hello, \" + name + \"!\");\n    }\n}"
        },
        {
            "name": "Basic Debugging",
            "description": "Handling exceptions and reading stack traces.",
            "code_snippet": "public class DebuggingDemo {\n    public static void main(String[] args) {\n        try {\n            int[] arr = {1, 2, 3};\n            System.out.println(arr[5]);\n        } catch (ArrayIndexOutOfBoundsException e) {\n            System.out.println(\"Caught Out Of Bounds Error\");\n        }\n    }\n}"
        }
    ],
    "practical_projects": [
        {
            "project_name": "Calculator",
            "description": "Console application that takes two numbers and an operator, executing mathematical calculations.",
            "implementation_code": "public class Calculator {\n    public static void main(String[] args) {\n        double num1 = 10, num2 = 5;\n        char op = '+';\n        double result = (op == '+') ? (num1 + num2) : 0;\n        System.out.println(\"Result: \" + result);\n    }\n}"
        },
        {
            "project_name": "Palindrome Checker",
            "description": "Checks if a string is identical forwards and backwards.",
            "algorithm": "Two-Pointer Strategy: O(N) Time, O(1) Auxiliary Space",
            "implementation_code": "public class PalindromeChecker {\n    public static boolean isPalindrome(String input) {\n        String cleaned = input.replaceAll(\"[^a-zA-Z0-9]\", \"\").toLowerCase();\n        int left = 0, right = cleaned.length() - 1;\n        while (left < right) {\n            if (cleaned.charAt(left) != cleaned.charAt(right)) return false;\n            left++; right--;\n        }\n        return true;\n    }\n    public static void main(String[] args) {\n        System.out.println(\"Is 'Panama' palindrome? \" + isPalindrome(\"A man, a plan, a canal: Panama\"));\n    }\n}"
        },
        {
            "project_name": "Prime Number Checker",
            "description": "Determines whether a given integer is a prime number.",
            "algorithm": "Trial Division up to sqrt(N)",
            "implementation_code": "public class PrimeChecker {\n    public static boolean isPrime(int n) {\n        if (n <= 1) return false;\n        for (int i = 2; i * i <= n; i++) {\n            if (n % i == 0) return false;\n        }\n        return true;\n    }\n    public static void main(String[] args) {\n        System.out.println(\"Is 29 prime? \" + isPrime(29));\n    }\n}"
        }
    ]
}


# 2. File Initialization Helper
def load_or_create_json():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_JSON, f, indent=2)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


data = load_or_create_json()

# 3. Streamlit Layout
st.title("☕ " + data.get("module", "Java Fundamentals"))
st.caption(f"**Objective:** {data.get('learning_objective', '')}")

st.divider()

# Sidebar Navigation
mode = st.sidebar.radio("Navigation", ["📚 Concepts & Topics", "🛠️ Practice Projects", "⚙️ Edit data.json"])

# Mode 1: Core Concepts & Topics
if mode == "📚 Concepts & Topics":
    st.header("Fundamental Topics")

    topics = data.get("subtopics", [])
    selected_topic_name = st.selectbox("Select a Topic to Study:", [t["name"] for t in topics])

    # Find selected topic
    topic = next((t for t in topics if t["name"] == selected_topic_name), None)

    if topic:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Overview")
            st.write(topic["description"])

            if "algorithms_and_logic" in topic:
                st.info(f"**Algorithms & Logic:** {topic['algorithms_and_logic']}")

        with col2:
            st.subheader("Code Example")
            st.code(topic.get("code_snippet", "// No code provided"), language="java")

# Mode 2: Practice Projects
elif mode == "🛠️ Practice Projects":
    st.header("Practice Projects")

    projects = data.get("practical_projects", [])
    selected_proj_name = st.selectbox("Select a Project:", [p["project_name"] for p in projects])

    project = next((p for p in projects if p["project_name"] == selected_proj_name), None)

    if project:
        st.subheader(project["project_name"])
        st.write(project["description"])

        if "algorithm" in project:
            st.warning(f"**Algorithm Strategy:** {project['algorithm']}")

        st.subheader("Java Implementation")
        st.code(project.get("implementation_code", "// Code coming soon"), language="java")

# Mode 3: JSON File Editor
elif mode == "⚙️ Edit data.json":
    st.header("Direct JSON Data Management")
    st.write(f"Modifications saved here directly update **`{DATA_FILE}`**.")

    raw_json = json.dumps(data, indent=2)
    updated_json_str = st.text_area("JSON Editor", value=raw_json, height=450)

    if st.button("💾 Save Changes to data.json"):
        try:
            parsed = json.loads(updated_json_str)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2)
            st.success("Successfully updated data.json!")
            st.rerun()
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {e}")

st.sidebar.divider()
st.sidebar.write(f"📁 Local File: `{os.path.abspath(DATA_FILE)}`")