# Image Processing Toolkit

An interactive, educational image-processing application built using **Python, OpenCV, NumPy, and Streamlit**.

The Image Processing Toolkit is a long-term learning project focused on understanding fundamental image-processing concepts through practical implementation and visual experimentation.

Rather than simply applying predefined image-processing operations, the objective is to explore **how digital images are represented, read, processed, and transformed**.

The project is being developed incrementally, with an emphasis on clear implementation, modular architecture, and accompanying educational documentation.

> **Project Status:** Active development. The Home page supports image uploading, previewing, and downloading. Dedicated image-processing operations will be introduced progressively.

---

## Technologies

The project uses:

- **Python** — Primary programming language.
- **OpenCV (`cv2`)** — Image processing and computer vision operations.
- **NumPy** — Image representation and array manipulation.
- **Streamlit** — Interactive web interface.
- **pytest** — Automated testing.
- **Git** — Version control.

---

## Current Functionality

### Home Page

The Home page provides a basic image input and output workflow.

Currently implemented features include:

- Uploading PNG, JPG, and JPEG images.
- Previewing uploaded images.
- Decoding uploaded images into NumPy arrays using OpenCV.
- Encoding output images for downloading.
- Downloading images in the same format as the uploaded image.
- Handling missing, empty, and invalid image uploads.
- Displaying contextual documentation alongside the workspace.

The Home page currently performs no image-processing transformations. The decoded input image also serves as the output image.

The downloaded image is re-encoded using OpenCV and may not be byte-for-byte identical to the original uploaded file.

### Processing Pages

The application currently contains four placeholder processing pages:

- Function1
- Function2
- Function3
- Function4

Each page has an independent image uploader and a corresponding processing module.

These pages establish the basic structure for future operations. Their current processing functions return the input image without applying transformations.

As development progresses, these placeholders will be replaced or extended with educational OpenCV operations.

---

## Application Layout

The Streamlit application is organized into three primary areas.

```text
+------------------+---------------------------+--------------------+
|                  |                           |                    |
|    Navigation    |         Workspace         |   Documentation    |
|                  |                           |                    |
|    Home          |    Image Upload           |    Page Overview   |
|                  |                           |                    |
|    Function1     |    Image Preview          |    Concepts        |
|    Function2     |                           |                    |
|    Function3     |    Processing Controls    |    Explanations    |
|    Function4     |                           |                    |
|                  |    Output and Download    |    Usage Notes     |
|                  |                           |                    |
+------------------+---------------------------+--------------------+
```

### Left Sidebar — Navigation

Provides navigation between the Home page and processing pages.

### Middle Workspace — Interactive Interface

Displays the interface associated with the selected page.

Depending on the operation, the workspace may contain image uploaders, previews, processing parameters, output images, and download controls.

### Right Panel — Documentation

Displays Markdown documentation corresponding to the selected page.

Documentation is maintained separately from the application's Python implementation.

---

## Application Architecture

The project follows a modular architecture that separates image-processing logic from the Streamlit interface.

The main components are:

### 1. Application Layer — `app.py`

Responsible for:

- Streamlit application configuration.
- Sidebar navigation.
- Page selection.
- Application layout.
- Rendering the selected view.
- Loading and displaying page-specific documentation.

The selected page is maintained through Streamlit session state.

### 2. View Layer — `views/`

Contains Streamlit interface implementations.

```text
views/
├── home_page.py
├── function1_page.py
├── function2_page.py
├── function3_page.py
└── function4_page.py
```

Each view is responsible for:

- Presenting its interface.
- Accepting user input.
- Invoking the corresponding processing functionality.
- Displaying images and processing results.
- Providing download controls where implemented.

Image-processing algorithms remain outside the view layer.

### 3. Image Processing Layer — `image_processing/`

Contains image-processing implementations independent of Streamlit.

```text
image_processing/
├── process1_function.py
├── process2_function.py
├── process3_function.py
└── process4_function.py
```

Functions in this layer operate on image data and processing parameters without depending on the web interface.

Currently, these modules contain placeholder implementations.

Future processing functionality will be introduced incrementally.

### 4. Shared Utilities — `utils/`

Contains reusable functionality and application mappings.

```text
utils/
├── constants.py
└── ui_utils.py
```

**`constants.py`**

Maintains mappings used for navigation, view selection, and documentation selection.

**`ui_utils.py`**

Contains shared image-handling utilities, including:

- Image uploading.
- Image decoding.
- Output image encoding for downloading.

These utilities reduce duplication between individual views.

### 5. Documentation Layer — `docs/`

Contains Markdown documentation for the Home page and processing pages.

```text
docs/
├── home.md
├── function1.md
├── function2.md
├── function3.md
└── function4.md
```

The documentation for the selected page appears in the application's right-side panel.

As processing functionality is introduced, its documentation will explain the underlying concepts, parameters, implementation details, and expected results.

### 6. Tests — `tests/`

Contains automated tests for verifying processing behavior.

Testing coverage will expand as new image-processing operations are implemented.

---

## Project Structure

```text
Image-Processing-Toolkit/
│
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── views/
│   ├── __init__.py
│   ├── home_page.py
│   ├── function1_page.py
│   ├── function2_page.py
│   ├── function3_page.py
│   └── function4_page.py
│
├── image_processing/
│   ├── __init__.py
│   ├── process1_function.py
│   ├── process2_function.py
│   ├── process3_function.py
│   └── process4_function.py
│
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   └── ui_utils.py
│
├── docs/
│   ├── home.md
│   ├── function1.md
│   ├── function2.md
│   ├── function3.md
│   └── function4.md
│
├── tests/
│   ├── __init__.py
│   └── test_processing.py
│
├── assets/
│   └── img/
│
└── ui/
    └── __init__.py
```

The `ui/` directory is currently reserved and does not contain separate navigation or layout implementations. These responsibilities are handled by `app.py`.

---

## Image Processing Workflow

The application uses a consistent workflow for image input and output.

```text
Upload Image
     |
     v
Read Uploaded File Bytes
     |
     v
Decode Image Using OpenCV
     |
     v
Represent Image as NumPy Array
     |
     v
Display Input Image
     |
     v
Apply Processing Operation
     |
     v
Display Output Image
     |
     v
Encode and Download Output
```

Processing operations will provide their own controls and transformations while following this common workflow.

Currently, the Home page uses the decoded input image directly as its output.

### Independent Image Uploads

Each view maintains its own image uploader.

When navigating away from a page and returning later, the previous upload is cleared.

This keeps individual processing pages independent and prevents unintended reuse of uploaded images across operations.

---

## Installation and Setup

### 1. Prerequisites

Install Python and ensure it is available from your terminal.

### 2. Navigate to the Project Directory

```bash
cd Image-Processing-Toolkit
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL for accessing it through your browser.

---

## Using the Toolkit

1. Launch the Streamlit application.
2. Open the **Home** page.
3. Upload a PNG, JPG, or JPEG image.
4. Preview the uploaded image.
5. Download the output image using the **Download Output Image** button.
6. Use the sidebar to explore other pages.
7. Read the corresponding documentation in the right-side panel.

Additional interactive processing capabilities will be introduced as development progresses.

---

## Testing

Automated tests are maintained in the `tests/` directory.

Install pytest if it is not already available:

```bash
python -m pip install pytest
```

Run the tests from the project root:

```bash
python -m pytest
```

The current test coverage is limited and will be expanded as image-processing operations are developed.

---

## Development Principles

The project follows these principles:

- **Incremental development:** Introduce and verify functionality in manageable steps.
- **Educational understanding:** Understand the concepts behind each operation before implementing it.
- **Separation of responsibilities:** Keep image-processing logic independent of Streamlit.
- **Reusability:** Share common upload, decoding, and downloading functionality.
- **Simplicity:** Avoid unnecessary abstractions and architectural complexity.
- **Documentation:** Maintain educational explanations alongside processing functionality.
- **Testing:** Verify implementations through automated tests and interactive application checks.
- **Maintainability:** Preserve a clear, organized project structure.

The objective is to build a toolkit that is both practical and useful for learning.

---

## Development Roadmap

The following topics are planned for future development.

### Image Input and Output

- Reading images using OpenCV.
- Understanding image decoding.
- Writing and saving images.
- Understanding image file formats.

### Image Representation

- Representing images using NumPy arrays.
- Image dimensions, shapes, and data types.
- Pixel values and channels.
- Grayscale and color images.

### Image Processing Operations

- Color-space conversions.
- Image resizing.
- Geometric transformations.
- Thresholding.
- Image filtering.
- Additional fundamental computer vision operations.

### Future Extensions

- Expanded automated testing.
- Additional interactive processing controls.
- Video processing.
- Video-frame manipulation.

These features are planned and should not be considered implemented until their respective development stages are complete.

---

## Project Objective

The Image Processing Toolkit aims to provide a structured, hands-on environment for understanding image processing using Python and OpenCV.

Each new operation will be approached by exploring:

- What the operation does.
- Why the operation is useful.
- How it works conceptually.
- How OpenCV implements it.
- How to use it correctly.
- How to verify its behavior.

The long-term objective is to develop a growing collection of understandable, independently maintainable, and well-documented image-processing operations.

This project is a work in progress and will continue to evolve through incremental development.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.