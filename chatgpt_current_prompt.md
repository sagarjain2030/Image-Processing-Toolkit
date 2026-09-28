# Project: Image-Processing-Toolkit

Repository path:

```text
~/Documents/TODO_List/MasteringOpenCVWithPython/WebApp/Image-Processing-Toolkit
```

Current Git branch:

```text
develop
```

## Project Goal

The goal is to build a reusable **Image Processing Toolkit** using:

* OpenCV for image-processing functionality
* Streamlit for the interactive web UI

The important long-term goal is to reach a stage where adding one OpenCV topic follows a repeatable workflow:

```text
OpenCV function
    ↓
Processing implementation
    ↓
Interactive UI
    ↓
Tests
    ↓
Documentation
    ↓
Navigation entry
    ↓
Complete
```

The infrastructure should be built once so we do not redesign the Streamlit application for every OpenCV function.

The project should look like an actual image-processing toolkit, not like a learning/demo repository.

We also want to learn enough Streamlit to implement and maintain the UI ourselves instead of blindly copying generated code.

---

# Git Status

Previous work already completed:

* Added `app.py`
* Updated `.gitignore`
* Combined Python ignore rules with JetBrains/PyCharm rules
* Added:

```gitignore
.idea/
```

so the complete PyCharm `.idea` directory is ignored.

Changes were:

* staged
* committed
* pushed to `origin/develop`

Expected repository state before current uncommitted work:

```text
On branch develop
Your branch is up to date with 'origin/develop'.

nothing to commit, working tree clean
```

---

# Overall Infrastructure Plan

Before implementing actual OpenCV operations, these infrastructure pieces were identified:

```text
Repository foundation        ✅
Folder structure             ✅
README architecture          ✅
.gitignore                   ✅
Git/develop workflow         ✅
Minimal app.py               ✅

Application layout           🟡 IN PROGRESS
Image-input infrastructure   ⬜
Operation registry           ⬜
Page contract                ⬜
Processing contract          ⬜
Reusable UI components       ⬜
Documentation loader         ⬜
Output handling              ⬜
Error handling               ⬜
Testing convention           ⬜
First full OpenCV operation  ⬜
```

---

# Intended Application Layout

The target application structure is:

```text
┌────────────────┐  ┌──────────────────────────────┬─────────────────┐
│                │  │                              │                 │
│ Functionalities│  │                              │ Documentation   │
│                │  │       Main Workspace         │ / Help Panel    │
│ ▶ Category 1   │  │                              │                 │
│ ▶ Category 2   │  │                              │                 │
│ ▶ Category 3   │  │                              │                 │
│                │  │                              │                 │
└────────────────┘  └──────────────────────────────┴─────────────────┘
     Sidebar                   ~75%                       ~25%
```

Streamlit's native left sidebar is used for navigation.

The central Streamlit page is divided using:

```python
st.columns([3, 1])
```

where:

* main column = actual OpenCV operation UI
* right column = documentation/help panel

---

# Application Layout Work Completed

The following layout concepts are already implemented:

* `st.set_page_config`
* wide layout
* expanded sidebar
* application title
* left sidebar
* central workspace
* right documentation panel
* 3:1 column ratio

Current page configuration:

```python
st.set_page_config(
    page_title="Image Processing Toolkit",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

---

# Sidebar Design Decision

Initially `selectbox` was considered for choosing categories and operations.

That was rejected because the desired UI is:

```text
Functionalities

▶ Category1
▶ Category2
▶ Category3
```

and when expanded:

```text
▼ Category1
    Function1
    Function2

▶ Category2
▶ Category3
```

Therefore categories use:

```python
st.sidebar.expander(...)
```

Individual functions inside an expanded category currently use:

```python
st.button(...)
```

Example:

```python
with st.sidebar.expander("Category1"):
    st.button("Function1")
    st.button("Function2")
```

---

# app.py Structure

The code was also refactored slightly so the application structure is separated.

Current general structure:

```python
def run():
    ...
    add_sidebar_menu()
    ...


def add_sidebar_menu():
    ...


if __name__ == "__main__":
    run()
```

This is preferable to putting everything directly at module scope.

Eventually `app.py` should act mainly as an orchestrator rather than containing OpenCV implementations or large amounts of UI logic.

---

# Current Code

Current experimental `app.py` is:

```python
import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

st.set_page_config(
    page_title="Image Processing Toolkit",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run():
    header = st.container()
    header.title("Image Processing Toolkit")

    function_selected = add_sidebar_menu()

    if function_selected is not None:
        st.session_state["Function"] = function_selected

    main_content, doc_panel = st.columns([3, 1])

    main_content.write("This is where we show content")
    main_content.write("")
    main_content.write(st.session_state["Function"])

    doc_panel.write("It is document sidebar")


def add_sidebar_menu():
    st.sidebar.header("Functionalities")

    function_selected = None

    with st.sidebar.expander("Category1"):
        function_selected = st.button("Function1")
        function_selected = st.button("Function2")

    with st.sidebar.expander("Category2"):
        function_selected = st.button("Function3")
        function_selected = st.button("Function4")

    return function_selected


if __name__ == "__main__":
    run()
```

---

# Important Streamlit Behavior Learned

`st.button()` returns a boolean.

For example:

```python
clicked = st.button("Function1")
```

returns:

```text
True
```

only on the Streamlit rerun caused by clicking that button.

Otherwise it returns:

```text
False
```

Therefore a button itself does not represent a persistent "currently selected operation".

---

# Current Bug / Learning Point

This code:

```python
function_selected = st.button("Function1")
function_selected = st.button("Function2")
function_selected = st.button("Function3")
function_selected = st.button("Function4")
```

does not work for navigation because the same variable is overwritten repeatedly.

If `Function1` is clicked:

```text
Function1 → True
Function2 → False
Function3 → False
Function4 → False
```

The final value returned is therefore:

```text
False
```

If `Function4` is clicked, the final assignment is:

```text
True
```

so only Function4 appears to work.

The user correctly identified that this happens because the value from Button 4 is the final value assigned to `function_selected`.

---

# Important Navigation Requirement

`add_sidebar_menu()` should eventually return the **name of the selected operation**, not a boolean.

Desired result:

```text
"Function1"
```

or:

```text
"Function2"
```

or:

```text
"Function3"
```

etc.

Conceptually:

```text
if Function1 button clicked
    selected function = "Function1"

if Function2 button clicked
    selected function = "Function2"
```

The exact implementation has NOT yet been completed.

This is the immediate next task.

---

# Session State

We identified that navigation also needs:

```python
st.session_state
```

because the selected operation must remain active after other Streamlit interactions cause reruns.

Desired behavior:

```text
User clicks Function1
        ↓
Function1 becomes selected
        ↓
Main panel displays Function1 UI
        ↓
Right panel displays Function1 documentation
        ↓
User adjusts another control
        ↓
Streamlit reruns
        ↓
Function1 should still remain selected
```

However, session-state handling should be addressed only after `add_sidebar_menu()` correctly returns the selected function name.

---

# Another Current Problem

This line:

```python
st.session_state["Function"]
```

can fail during the first application run because `"Function"` may not exist yet.

Session state therefore needs to be initialized before reading it.

This has NOT yet been implemented.

It is the task immediately after fixing button selection.

---

# Immediate Next Steps

Continue in this exact order:

### Step 1 — Fix sidebar function selection

Change `add_sidebar_menu()` so clicking a button returns its function name instead of `True`/`False`.

Target behavior:

```text
Click Function1 → return "Function1"
Click Function2 → return "Function2"
Click Function3 → return "Function3"
Click Function4 → return "Function4"
```

Do this before working further on session state.

### Step 2 — Initialize session state

Handle the situation where:

```python
st.session_state["Function"]
```

does not exist on the first application run.

### Step 3 — Persist selected operation

Store the selected function in session state so Streamlit reruns do not lose navigation state.

### Step 4 — Display selected function

Temporarily show the active function inside:

```text
main_content
```

This is only for verifying navigation behavior.

### Step 5 — Finish sidebar/navigation infrastructure

Once persistent function selection works, we can consider the sidebar portion of Application Layout Infrastructure complete.

---

# Do NOT Implement Yet

At this stage, do not start:

* OpenCV functions
* `cv2`
* image upload
* image processing
* real OpenCV categories
* Markdown file loading
* operation registry
* tests
* custom CSS
* dynamic documentation loading

Dummy names such as:

```text
Category1
Category2

Function1
Function2
Function3
Function4
```

should remain until the navigation mechanism itself works correctly.

---

# Development Philosophy

Work incrementally.

Do not provide a complete finished implementation immediately.

When a new Streamlit feature is needed, first identify which Streamlit component/concept should be studied, allow the user to implement it, then review the code.

The current focus is learning enough Streamlit to build the application infrastructure independently.

The immediate problem to resume with is:

> Modify `add_sidebar_menu()` so each button identifies which function was clicked, rather than repeatedly overwriting `function_selected` with boolean values.
