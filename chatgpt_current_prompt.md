# Project: Image Processing Toolkit

## Goal

Build a reusable **Image Processing Toolkit** using:

- Streamlit for the interactive web interface
- OpenCV for image-processing operations
- NumPy for image-data handling

The main architectural goal is to build the surrounding application infrastructure first, so that adding future OpenCV operations follows a predictable structure instead of redesigning the application for every new operation.

The project is being developed incrementally.

Do not jump ahead into real OpenCV processing until the infrastructure concepts are understood and implemented.

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

Reusable UI components       ⬜ NEXT
Documentation loader         ⬜
Output handling              ⬜
Error handling               ⬜
Testing convention           ⬜
First full OpenCV operation  ⬜
```

The original infrastructure roadmap places reusable UI components after the processing contract and before documentation/output/error/testing work.

---

# Current Application Layout

The application uses:

```python
main_content, doc_panel = st.columns([3, 1])
```

Conceptually:

```text
┌────────────────┐  ┌──────────────────────────────┬─────────────────┐
│                │  │                              │                 │
│ Functionalities│  │                              │ Documentation   │
│                │  │       Main Workspace         │ / Help Panel    │
│ ▶ Category 1   │  │                              │                 │
│ ▶ Category 2   │  │                              │                 │
│                │  │                              │                 │
└────────────────┘  └──────────────────────────────┴─────────────────┘
     Sidebar                   ~75%                       ~25%
```

Responsibilities currently are:

```text
sidebar
    navigation

main_content
    uploader
    selected operation page
    image-processing result

doc_panel
    future documentation/help
```

---

# Sidebar Navigation

The sidebar is generated dynamically from:

```python
sidebar_dictionary = {
    "category1": ["Function1", "Function2"],
    "category2": ["Function3", "Function4"]
}
```

The menu is generated with nested loops:

```python
for key, values in sidebar_dictionary.items():
    with st.sidebar.expander(key, True):
        for value in values:
            st.button(...)
```

Navigation state is stored using:

```python
st.session_state["Function"]
```

It is initialized during the first application run:

```python
if "Function" not in st.session_state:
    st.session_state["Function"] = None
```

The callback only changes state:

```python
def on_click_function(string: str):
    st.session_state["Function"] = string
```

This is intentionally separate from page rendering.

Conceptually:

```text
button click
    ↓
callback
    ↓
store selected function name
    ↓
Streamlit reruns
    ↓
normal page rendering reads session state
```

---

# Image-Input Infrastructure

The uploader currently accepts:

```python
png
jpg
jpeg
```

The input pipeline is:

```text
Streamlit UploadedFile
        ↓
uploaded_file.getvalue()
        ↓
bytes
        ↓
np.frombuffer(..., dtype=np.uint8)
        ↓
1-D encoded uint8 ndarray
        ↓
cv2.imdecode(..., cv2.IMREAD_COLOR)
        ↓
decoded OpenCV image ndarray
```

Important distinction:

```text
np.frombuffer()
```

does NOT decode the image.

It only exposes the encoded file bytes as a NumPy array.

The actual decoding boundary is:

```python
opencv_img = cv2.imdecode(
    image,
    cv2.IMREAD_COLOR
)
```

We deliberately stop there.

Do NOT start studying or implementing:

```text
BGR/RGB conversion
resize
threshold
blur
filters
edge detection
etc.
```

yet.

`cv2.imdecode()` is currently used only to complete the common image-input infrastructure.

---

# Page Contract

The problem we solved was:

```text
sidebar
    ↓
"Function1"
    ↓
st.session_state["Function"]
    ↓
???
    ↓
Function1-specific UI
```

The page contract now says:

```text
Every operation page receives:

main_content
image
```

So pages follow this shape:

```python
def function1_page(main_content, image):
    ...
```

The current convention is therefore:

```text
PAGE CONTRACT

page(main_content, image)
```

The `image` argument may be:

```text
None
```

when no image has been uploaded, or:

```text
OpenCV image ndarray
```

when an image has been successfully decoded.

This allows an operation page to exist even before an image has been uploaded.

Example:

```python
def function1_page(main_content, image):
    main_content.write("Inside function1 page")

    if image is not None:
        ...
    else:
        main_content.write("No image received")
```

---

# Page Routing

The selected operation name is mapped to its page function through:

```python
function_dictionary = {
    "Function1": function1_page,
    "Function2": function2_page,
    "Function3": function3_page,
    "Function4": function4_page,
}
```

These dictionary values are actual Python function objects, not strings.

For example:

```python
function_dictionary["Function1"]
```

returns:

```python
function1_page
```

The current routing logic is:

```python
if st.session_state["Function"] is not None:
    s = function_dictionary[st.session_state["Function"]]
    s(main_content, opencv_img)
```

Conceptually:

```text
"Function1"
      ↓
function_dictionary
      ↓
function1_page
      ↓
function1_page(main_content, opencv_img)
```

The callback does NOT render the page.

Rendering happens during the application's normal rerun.

This keeps responsibilities separated:

```text
callback
    remembers selection

function_dictionary
    maps selection → page

create_main_content()
    chooses and renders selected page
```

---

# Processing Contract

We also established a separate processing layer.

Dummy processors currently look like:

```python
def process_function1(image):
    return image
```

The processing contract is:

```text
PROCESSING CONTRACT

process(image) → result
```

Processing functions:

- receive image data
- perform processing
- return the result
- do NOT receive Streamlit containers
- do NOT render UI
- do NOT know about `main_content`

The page owns Streamlit/UI behavior.

The processor owns image-processing behavior.

Conceptually:

```text
operation page
      ↓
collect operation-specific UI values
      ↓
call processing function
      ↓
processing function receives image + parameters
      ↓
returns result
      ↓
page displays result
```

For now the processors simply return the original image because actual OpenCV operations have not started.

---

# Page → Processor Relationship

Each page currently directly calls its corresponding processor.

Example:

```python
def function1_page(main_content, image):
    main_content.write("Inside function1 page")

    if image is not None:
        out = process_function1(image)
        main_content.image(out)
    else:
        main_content.write("No image received")
```

So:

```text
function1_page → process_function1
function2_page → process_function2
function3_page → process_function3
function4_page → process_function4
```

This means the page does not need to look at:

```python
st.session_state["Function"]
```

to rediscover which processor belongs to it.

That keeps the operation page self-contained.

---

# Handling No Uploaded Image

Inside `create_main_content()`:

```python
opencv_img = None
```

is created before checking the uploader.

If an image exists:

```python
opencv_img = cv2.imdecode(...)
```

replaces `None` with the decoded image.

Then the selected page is called regardless of whether an image exists:

```python
s(main_content, opencv_img)
```

Therefore:

```text
No upload
    ↓
opencv_img = None
    ↓
function1_page(main_content, None)
```

while:

```text
Image uploaded
    ↓
opencv_img = decoded ndarray
    ↓
function1_page(main_content, opencv_img)
```

The page protects the processor using:

```python
if image is not None:
```

Therefore the processor itself does not currently need to handle `None`.

---

# Current Responsibility Separation

The current architecture is approximately:

```text
run()
 │
 ├── application layout
 │
 ├── sidebar
 │
 └── main workspace
          │
          ▼
 create_main_content()
          │
          ├── common uploader
          │
          ├── bytes → NumPy buffer
          │
          ├── cv2.imdecode()
          │
          ▼
    decoded image / None
          │
          ▼
 function_dictionary
          │
          ▼
 operation page
          │
          ├── operation-specific UI
          ├── checks whether image exists
          │
          ▼
 processing function
          │
          ▼
        result
          │
          ▼
 operation page displays result
```

The intended separation is:

```text
APPLICATION LAYER
run()
create_main_content()
sidebar/navigation

PAGE/UI LAYER
function1_page()
function2_page()
...

PROCESSING LAYER
process_function1()
process_function2()
...
```

---

# Temporary Debugging Output

`create_main_content()` still intentionally contains many debugging statements such as:

```python
main_content.write(...)
```

for:

```text
uploaded filename
MIME type
file size
bytes type
bytes length
NumPy dtype
NumPy size
NumPy shape
NumPy ndim
decoded image dtype
decoded image size
decoded image shape
decoded image ndim
```

These were useful while learning and verifying the image-input pipeline.

They can be cleaned up later.

There is no need to remove them before continuing infrastructure work.

---

# Current app.py

```python
import numpy as np
import streamlit as st
from streamlit.logger import get_logger
import cv2

LOGGER = get_logger(__name__)

st.set_page_config(
    page_title="Image Processing Toolkit",
    layout="wide",
    initial_sidebar_state="expanded",
)

sidebar_dictionary = {
    "category1": ["Function1", "Function2"],
    "category2": ["Function3", "Function4"]
}


def process_function1(image):
    return image


def process_function2(image):
    return image


def process_function3(image):
    return image


def process_function4(image):
    return image


def function1_page(main_content, image):
    main_content.write("Inside function1 page")
    if image is not None:
        out = process_function1(image)
        main_content.image(out)
    else:
        main_content.write("No image received")


def function2_page(main_content, image):
    main_content.write("Inside function2 page")
    if image is not None:
        out = process_function2(image)
        main_content.image(out)
    else:
        main_content.write("No image received")


def function3_page(main_content, image):
    main_content.write("Inside function3 page")
    if image is not None:
        out = process_function3(image)
        main_content.image(out)
    else:
        main_content.write("No image received")


def function4_page(main_content, image):
    main_content.write("Inside function4 page")
    if image is not None:
        out = process_function4(image)
        main_content.image(out)
    else:
        main_content.write("No image received")


function_dictionary = {
    "Function1": function1_page,
    "Function2": function2_page,
    "Function3": function3_page,
    "Function4": function4_page,
}


def create_main_content(main_content):
    main_content.write("This is where we show content")
    main_content.write("")

    uploaded_file = main_content.file_uploader(
        label="Upload an image",
        type=["png", "jpg", "jpeg"],
    )

    opencv_img = None

    if uploaded_file is not None:
        main_content.write(f"Name :{uploaded_file.name}")
        main_content.write(f"Type :{uploaded_file.type}")
        main_content.write(f"Size :{uploaded_file.size}")

        main_content.image(uploaded_file)

        image_bytes = uploaded_file.getvalue()

        main_content.write(type(image_bytes))
        main_content.write(len(image_bytes))

        image = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        main_content.write(type(image).__name__)
        main_content.write(image.dtype)
        main_content.write(image.size)
        main_content.write(image.shape)
        main_content.write(image.ndim)

        opencv_img = cv2.imdecode(
            image,
            cv2.IMREAD_COLOR
        )

        main_content.write(type(opencv_img).__name__)
        main_content.write(opencv_img.dtype)
        main_content.write(opencv_img.size)
        main_content.write(opencv_img.shape)
        main_content.write(opencv_img.ndim)

    if st.session_state["Function"] is not None:
        main_content.write(st.session_state["Function"])

        page_function = function_dictionary[
            st.session_state["Function"]
        ]

        page_function(main_content, opencv_img)


def run():
    header = st.container()
    header.title("Image Processing Toolkit")

    if "Function" not in st.session_state:
        st.session_state["Function"] = None

    main_content, doc_panel = st.columns([3, 1])

    add_sidebar_menu()

    create_main_content(main_content)

    doc_panel.write("It is document sidebar")


def on_click_function(string: str):
    st.session_state["Function"] = string


def add_sidebar_menu():
    st.sidebar.header("Functionalities")

    for key, values in sidebar_dictionary.items():
        with st.sidebar.expander(key, True):
            for value in values:
                st.button(
                    label=value,
                    on_click=on_click_function,
                    args=(value,)
                )


if __name__ == "__main__":
    run()
```

Note: the earlier temporary `process_dictionary` has been omitted because it is no longer used. Each operation page directly calls its corresponding processing function.

---

# What We Have Learned During the Page/Processing Work

## Python

- Functions are objects.
- A dictionary can store function objects.
- `"function1_page"` is a string.
- `function1_page` is the function object.
- A stored function can be retrieved and called:

```python
page_function = function_dictionary["Function1"]
page_function(main_content, image)
```

- Module execution order matters when constructing dictionaries containing function references.
- A function body can refer to global names that exist by the time the function is actually called.

---

## Streamlit

- Callbacks should primarily update persistent state.
- Streamlit reruns the application after widget interaction.
- UI that must persist should be rendered during the normal rerun rather than only inside a callback.
- `st.session_state` stores the selected operation across reruns.

---

## Architecture

We established two basic contracts:

```text
Page Contract
─────────────
page(main_content, image)
```

and:

```text
Processing Contract
───────────────────
process(image) → result
```

The page is responsible for:

```text
Streamlit widgets
operation-specific UI
checking whether an image exists
calling its processing function
displaying output
```

The processing function is responsible for:

```text
receiving valid image data
performing processing
returning the result
```

The processing layer should remain independent of Streamlit.

---

# Things NOT To Implement Yet

Continue using dummy categories and operations:

```text
category1
category2

Function1
Function2
Function3
Function4
```

Do not yet start:

- resize
- threshold
- blur
- filters
- edge detection
- BGR/RGB conversion work
- real OpenCV categories
- real OpenCV processing
- Markdown documentation loading
- tests
- custom CSS
- elaborate output handling

The architecture is still being built incrementally.

---

# NEXT STEP

The next infrastructure topic is:

```text
Reusable UI Components
```

Do NOT immediately create a large components system.

Start by understanding:

1. What does a reusable UI component mean in this project?
2. What duplication/problem would it solve?
3. Which UI currently belongs to common infrastructure versus operation-specific pages?
4. What is the smallest useful reusable component we could extract?
5. Should we even extract anything yet, or wait until duplication actually appears?

Continue using the same incremental teaching approach:

1. Explain the concept first.
2. Explain why this project needs it.
3. Do not immediately provide a finished architecture.
4. Give the smallest exercise needed so I can implement it myself.
5. Review my implementation before moving forward.
6. Do not begin real OpenCV processing yet.