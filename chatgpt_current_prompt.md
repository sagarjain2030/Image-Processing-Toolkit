# Project: Image Processing Toolkit

## Goal

I am building a reusable **Image Processing Toolkit** using:

- Streamlit for UI
- OpenCV for image-processing operations
- NumPy for image-data handling
- pytest for automated testing

The project is being developed incrementally.

Until now, the focus has deliberately been on understanding and building the surrounding application architecture before implementing real OpenCV operations.

Teaching style:

1. Explain concepts before implementing them.
2. Explain why they matter in this project.
3. Do not dump a finished architecture immediately.
4. Work through the actual project rather than doing excessive question/answer exercises.
5. Let me implement things and correct problems when they appear.
6. Avoid premature abstractions.
7. Do not create reusable systems merely because a roadmap topic exists.
8. We are now ready to start real OpenCV operations.

---

# Current Infrastructure Status

```text
Repository foundation        ✅
Folder structure             ✅
README architecture          ✅
.gitignore                   ✅
Git/develop workflow         ✅
Minimal app.py               ✅

Application layout           ✅
Image-input infrastructure   ✅
Operation registry           ✅ basic
Page contract                ✅ basic
Processing contract          ✅ basic

Reusable UI components       ✅ concept understood; no extraction needed yet
Documentation loader         ✅ basic
Output handling              ✅ basic
Error handling               ✅ basic
Testing convention           ✅ basic

First full OpenCV operation  ⬜ NEXT
```

---

# Current Application Layout

The app uses:

```python
main_content, doc_panel = st.columns([3, 1])
```

Conceptually:

```text
Sidebar                    Main Workspace              Documentation
───────                    ──────────────              ─────────────
navigation                 uploader                    selected-operation docs
categories                 operation page
operations                 processing result
```

Responsibilities:

```text
sidebar
    navigation

main_content
    uploader
    selected operation page
    processing result

doc_panel
    documentation/help
```

---

# Navigation

Dummy categories and operations are still being used:

```text
category1
category2

Function1
Function2
Function3
Function4
```

Do not replace these prematurely unless we explicitly decide to start converting them into real operations.

Navigation is based on:

```python
sidebar_dictionary = {
    "category1": ["Function1", "Function2"],
    "category2": ["Function3", "Function4"]
}
```

Selected operation:

```python
st.session_state["Function"]
```

Callback:

```python
def on_click_function(string: str):
    st.session_state["Function"] = string
```

Flow:

```text
button click
    ↓
callback changes session state
    ↓
Streamlit reruns
    ↓
normal rendering reads state
```

Callbacks do not render operation pages.

---

# Image Input Infrastructure

There is one common uploader.

Pipeline:

```text
Streamlit UploadedFile
        ↓
uploaded_file.getvalue()
        ↓
bytes
        ↓
np.frombuffer(..., dtype=np.uint8)
        ↓
encoded-byte ndarray
        ↓
cv2.imdecode(..., cv2.IMREAD_COLOR)
        ↓
decoded OpenCV ndarray
```

Important:

```python
np.frombuffer(...)
```

does not decode the image.

Actual decoding happens with:

```python
opencv_img = cv2.imdecode(
    image,
    cv2.IMREAD_COLOR
)
```

Basic failed-decode handling has now been added:

```python
if opencv_img is None:
    main_content.write("Could not decode the uploaded image")
```

If decoding succeeds, `opencv_img` contains the decoded OpenCV image.

There are still temporary debugging `write()` calls showing file metadata, array shape, dtype, size, etc. These can be cleaned up later.

---

# Page Contract

Every operation page follows:

```text
page(main_content, image)
```

Example:

```python
def function1_page(main_content, image):
    if image is not None:
        out = process_function1(image)
        main_content.image(out)
    else:
        main_content.write("No image received")
```

Important fix already established:

```python
def function2_page(main_content, image):
```

not:

```python
def function2_page(main_content, doc_cont, image):
```

---

# Page Routing

Pages are registered as actual function objects:

```python
function_dictionary = {
    "Function1": function1_page,
    "Function2": function2_page,
    "Function3": function3_page,
    "Function4": function4_page,
}
```

Routing is currently protected against an invalid key:

```python
if st.session_state["Function"] is not None:
    main_content.write(st.session_state["Function"])

    try:
        s = function_dictionary[st.session_state["Function"]]
    except KeyError:
        main_content.write("Could not find function")
    else:
        s(main_content, opencv_img)
```

The `try` contains only the dictionary lookup so a future `KeyError` inside an operation page is not incorrectly reported as a routing error.

---

# Processing Contract

Each operation page has a corresponding processor.

Currently processors are placeholders such as:

```python
def process_function1(image):
    return image
```

Contract:

```text
process(image) → result
```

Processing functions:

```text
receive image/data
perform processing
return result

do NOT receive Streamlit containers
do NOT render UI
do NOT know about main_content
```

Page responsibility:

```text
collect parameters
call processor
receive result
decide how result is displayed
```

Processor responsibility:

```text
perform the operation
produce result
return result
```

---

# Output Handling

Basic output handling is already sufficient.

Current example:

```python
out = process_function1(image)
main_content.image(out)
```

Important distinction:

```text
processor
    decides WHAT result is produced

page
    decides HOW result is presented
```

Not every future processor must return exactly one image.

Possible future results could include:

```text
one image
multiple images
image + metadata
numeric result
textual result
structured result
```

No universal output abstraction exists yet.

That is intentional.

A shared output helper should only be introduced if actual repeated presentation logic appears across operation pages.

Principle:

```text
same output type ≠ same output behavior
```

For example, one operation showing one image and another showing two images side-by-side does not justify forcing them through one universal renderer.

---

# Reusable UI Components

No component framework has been created yet.

Principle:

```text
reusable ≠ universal
```

Do not invent abstractions before duplication exists.

Potential helpers may appear later when real operations reveal repeated UI patterns.

---

# Documentation Loader

Current loader:

```python
def load_documentation(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"
```

Contract:

```text
file path
    ↓
load_documentation()
    ↓
Python string
```

Rendering remains separate:

```python
doc_panel.markdown(text)
```

So:

```text
loader
    file → text

doc_panel
    text → rendered Markdown
```

Documentation mapping:

```python
doc_file_dictionary = {
    "Function1": "function1.md",
    "Function2": "function2.md",
    "Function3": "function3.md",
    "Function4": "function4.md",
}
```

`docs/test.md` remains the default documentation when no operation is selected.

---

# Error Handling

Only basic, concrete error handling has been added.

Current cases:

```text
missing documentation file
    → catch FileNotFoundError

image decoder produces no usable image
    → check returned result

selected operation missing from function_dictionary
    → catch KeyError
```

Important concepts learned:

```text
expected state
    ≠
invalid returned result
    ≠
exception
    ≠
programming/configuration bug
```

And:

```text
returned value is unusable
    → validate/check result

operation raises an exception
    → exception handling
```

No centralized error manager, custom exceptions, logging framework, or large error abstraction exists yet.

Do not create one until the project demonstrates a real need.

---

# Testing Convention

pytest has now been installed successfully.

Convention:

```text
tests directory:
    tests/

test files:
    test_*.py

test functions:
    test_*

primary initial target:
    processing functions
```

Current test file:

```text
tests/test_processing.py
```

Current test:

```python
import numpy as np

from app import process_function1


def test_process_function1_returns_image():
    image = np.array([
        [[10, 20, 30], [40, 50, 60]],
        [[70, 80, 90], [100, 110, 120]]
    ], dtype=np.uint8)

    result = process_function1(image)

    assert np.array_equal(result, image)
```

The test has been run successfully:

```text
collected 1 item

tests/test_processing.py .    [100%]

1 passed
```

Do not create duplicate tests for Function2–Function4 merely to increase test count.

Tests should accompany actual behavior as real operations are implemented.

---

# Current Architectural Layers

```text
APPLICATION / INFRASTRUCTURE

run()
create_main_content()
add_sidebar_menu()
load_documentation()
routing dictionaries
image loading/decoding


PAGE / UI

function1_page()
function2_page()
function3_page()
function4_page()


PROCESSING

process_function1()
process_function2()
process_function3()
process_function4()


TESTING

tests/test_processing.py
```

---

# Current Design Philosophy

Do not build abstractions just because an architecture diagram suggests they might eventually exist.

Preferred process:

```text
implement real feature
    ↓
observe duplication/problem
    ↓
understand the repeated responsibility
    ↓
extract abstraction if justified
```

Not:

```text
imagine every future possibility
    ↓
create universal abstraction
    ↓
force operations into it
```

---

# Important Things Not To Add Prematurely

Do not immediately introduce:

```text
large component systems
universal output managers
centralized error managers
custom exception hierarchies
pytest fixtures
mocking frameworks
coverage configuration
complex test classes
custom CSS
large refactors
```

Only add these when real project requirements justify them.

---

# NEXT STAGE

The surrounding basic infrastructure is now complete enough to start the first real OpenCV operation.

```text
First full OpenCV operation  ⬜ NEXT
```

The intended next approach is:

```text
choose Function1
    ↓
understand one real OpenCV operation
    ↓
implement its processor
    ↓
run through existing page architecture
    ↓
observe actual UI/output issues
    ↓
write meaningful automated test
    ↓
update documentation
```

A likely first operation discussed was grayscale conversion, but implementation has NOT started yet.

Before writing code, explain what the chosen operation actually does to image data and then implement it incrementally.

Do not return to long sequences of classification questions. Work on the project directly and correct mistakes as they arise.