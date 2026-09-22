# Image Processing Toolkit

An interactive web-based image processing toolkit for experimenting with image transformations, analysis techniques, filtering operations, feature extraction, and other computer vision primitives.

The application provides a visual interface where operations can be selected, configured through their available parameters, executed on user-provided images, and inspected directly from the browser.

Each operation is accompanied by contextual documentation describing the available parameters and their behavior.

---

## Application Layout

The interface is divided into three primary areas.

```text
┌───────────────────┬───────────────────────────────┬───────────────────────┐
│                   │                               │                       │
│    Navigation     │        Workspace              │     Documentation     │
│                   │                               │                       │
│  Operation groups │  Input image                  │  Operation overview   │
│                   │                               │                       │
│  Available        │  Parameters                   │  Parameter meanings   │
│  operations       │                               │                       │
│                   │  Execute operation            │  Usage information    │
│                   │                               │                       │
│                   │  Result                       │  Additional notes      │
│                   │                               │                       │
└───────────────────┴───────────────────────────────┴───────────────────────┘
```

The left navigation area is used to select an image-processing operation.

The central workspace contains the inputs and parameters required by the selected operation and displays its resulting output.

The documentation area presents contextual information loaded from Markdown documentation associated with the currently selected operation.

---

## Architecture

The project separates image-processing logic from the web interface.

```text
                         app.py
                            │
                            ▼
                       UI Layer
                            │
                            ▼
                       Page Layer
                            │
                            ▼
                Image Processing Layer
```

This separation keeps processing functions independent of the presentation framework.

### Image Processing Layer

```text
image_processing/
```

Contains the actual image-processing implementations.

Functions in this layer should operate on image data and parameters without depending on the web UI.

Example:

```text
image_processing/
└── geometric/
    └── resize.py
```

---

### Page Layer

```text
pages/
```

Contains the user-interface definition associated with each operation.

A page is responsible for collecting parameters, invoking the corresponding image-processing function, and presenting its result.

Example:

```text
pages/
└── geometric/
    └── resize_page.py
```

---

### Documentation Layer

```text
docs/
```

Contains Markdown documentation for individual operations.

Documentation may describe the operation itself, available parameters, valid values, behavior, usage considerations, and other relevant information.

Example:

```text
docs/
└── geometric/
    └── resize.md
```

The documentation for the currently selected operation is displayed alongside its interactive workspace.

---

### Shared UI Layer

```text
ui/
```

Contains reusable presentation and navigation functionality.

```text
ui/
├── sidebar.py
├── layout.py
└── common.py
```

`sidebar.py` manages application navigation.

`layout.py` defines the common workspace and documentation layout.

`common.py` contains reusable UI components shared by multiple operations.

Individual image-processing implementations should not depend on this layer.

---

## Operation Organization

Operations are organized by image-processing domain.

```text
image_processing/
├── image_io/
├── image_properties/
├── geometric/
├── color/
├── filtering/
├── thresholding/
├── morphology/
├── edge_detection/
├── histograms/
├── contours/
├── drawing/
└── feature_detection/
```

The `pages/` and `docs/` directories follow the same organization.

For example, a geometric resize operation is represented by:

```text
image_processing/geometric/resize.py
pages/geometric/resize_page.py
docs/geometric/resize.md
```

This keeps the processing implementation, interactive interface, and documentation independently maintainable while preserving a predictable project structure.

---

## Project Structure

```text
image-processing-toolkit/
│
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
│
├── image_processing/
│   ├── image_io/
│   ├── image_properties/
│   ├── geometric/
│   ├── color/
│   ├── filtering/
│   ├── thresholding/
│   ├── morphology/
│   ├── edge_detection/
│   ├── histograms/
│   ├── contours/
│   ├── drawing/
│   └── feature_detection/
│
├── pages/
│   ├── image_io/
│   ├── image_properties/
│   ├── geometric/
│   ├── color/
│   ├── filtering/
│   ├── thresholding/
│   ├── morphology/
│   ├── edge_detection/
│   ├── histograms/
│   ├── contours/
│   ├── drawing/
│   └── feature_detection/
│
├── docs/
│   ├── image_io/
│   ├── image_properties/
│   ├── geometric/
│   ├── color/
│   ├── filtering/
│   ├── thresholding/
│   ├── morphology/
│   ├── edge_detection/
│   ├── histograms/
│   ├── contours/
│   ├── drawing/
│   └── feature_detection/
│
├── ui/
│   ├── sidebar.py
│   ├── layout.py
│   └── common.py
│
├── assets/
│
└── tests/
```

---

## Design Principles

The processing layer remains independent of the web framework.

Each image-processing operation has a focused implementation.

UI-specific behavior remains outside processing modules.

Operation documentation is stored as Markdown rather than embedded into application code.

The directory structure mirrors operation categories across processing, interface, and documentation layers.

Shared UI functionality is implemented once and reused across operation pages.

The architecture is intended to allow new image-processing operations to be added without requiring changes to unrelated implementations.

---

## Technology

The toolkit is designed around:

* Python
* OpenCV
* NumPy
* Streamlit

Additional dependencies may be introduced as new image-processing capabilities are added.
