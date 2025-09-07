# MonoWidget User Guide

## Project Overview

MonoWidget is a Python tool for creating and managing parameter interfaces. It generates visual interface components through a simple API for defining parameters. It is particularly suitable for rapidly developing configuration interfaces, debugging tools, and parameter debuggers that require user interaction.

## Quick Start

### Installation

MonoWidget is currently a local development library. Simply clone or download the source code to your project.

### Basic Usage Example

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from monowidget import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MonoWidget Example")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Define attribute list
        attrs = [
            MonoAttr("username", "Alice", label="Username"),
            MonoAttr("age", 30, range=(18, 100), label="Age"),
            MonoAttr("active", True, label="Active"),
            MonoAttr("theme", "dark", enum=["light", "dark", "auto"], label="Theme"),
        ]
        
        # Create Mono object
        mono = Mono(attrs)
        
        # Create Inspector and add to layout
        inspector = QMonoInspector(mono)
        main_layout.addWidget(inspector)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

## Core Concepts

### MonoAttr
`MonoAttr` is a parameter definition class used to describe all properties of a single parameter, including name, value, type, range, etc.

### Mono
`Mono` is a data model class that contains multiple `MonoAttr` properties and serves as the data source for `QMonoInspector`.

### QMonoInspector
`QMonoInspector` is the interface renderer responsible for rendering `Mono` objects into visual interfaces.

## Using MonoAttr to Create Inspector

### 1. Import Necessary Modules
```python
from monowidget import *
```

### 2. Define MonoAttr Properties
`MonoAttr` supports multiple parameter types. The system will automatically identify and generate corresponding interface controls based on the `value` type:

#### Supported Type Comparison Table

| Type | Python Value Example | Interface Control |
|------|---------------------|-------------------|
| **String** | `"text"` | Text input box |
| **Integer** | `42` | Number input box |
| **Float** | `3.14` | Float input box |
| **Boolean** | `True` | Checkbox |
| **Enum** | `"option1"` | Dropdown selection |
| **List** | `[1, 2, 3]` | List editor |
| **Dict** | `{"key": "value"}` | Dictionary editor |
| **Function Button** | `lambda: print("hi")` | Button |
| **DateTime** | `datetime.now()` | DateTime picker |
| **Color** | `"#ff0000"` | Color picker |

#### Usage Example
```python
from datetime import datetime

attrs = [
    # Basic types
    MonoAttr("name", "Example", label="Name"),           # String
    MonoAttr("count", 42, label="Count"),                # Integer
    MonoAttr("price", 29.99, label="Price"),             # Float
    MonoAttr("enabled", True, label="Enabled"),          # Boolean
    
    # Range-limited numbers
    MonoAttr("volume", 75, range=(0, 100, 5), label="Volume"),
    
    # Enum type
    MonoAttr("mode", "normal", enum=["easy", "normal", "hard"], label="Mode"),
    
    # Complex types
    MonoAttr("tags", ["python", "qt"], label="Tags"),      # List
    MonoAttr("settings", {"theme": "dark", "font": 14}, label="Settings"),  # Dict
    
    # Function button
    MonoAttr("save_button", lambda: print("Saved"), label="Save Settings"),
    
    # DateTime
    MonoAttr("start_time", datetime.now(), label="Start Time"),
    
    # Color
    MonoAttr("bg_color", "#ffffff", label="Background Color")
]
```

### 3. Create Mono Object
Use the attribute list to create a `Mono` object:
```python
mono = Mono(attrs)
```

### 4. Create and Display Inspector
```python
# Create QMonoInspector instance
inspector = QMonoInspector(mono)

# Add to layout
layout.addWidget(inspector)
```

### 5. Advanced Configuration - Grouping and Titles
You can use `group`, `header`, and `title` parameters to organize the interface layout:

```python
attrs = [
    # Page title
    MonoAttr("app_title", "Configuration Center", title="Application Configuration Center"),
    
    # User info group
    MonoAttr("username", "admin", label="Username", group="User Info", header="👤 User Configuration"),
    MonoAttr("email", "admin@example.com", label="Email", group="User Info"),
    
    # Interface settings group
    MonoAttr("theme", "dark", enum=["light", "dark"], label="Theme", group="Interface Settings", header="🎨 Appearance Settings"),
]
```

## Data Read and Write Methods

### Method 1: Read all parameter values as dictionary
```python
# Get all parameter values (as dictionary)
values = inspector.params  # Returns dictionary with all parameter values
print(values)  # Output: {'username': 'Alice', 'age': 30, ...}

# Set multiple parameter values
inspector.params = {
    'username': 'Bob',
    'age': 25
}
```

### Method 2: Access individual attributes using inspector.vs
```python
# Read single parameter value
username = inspector.vs.username
print(f"Current username: {username}")

# Modify single parameter value
inspector.vs.username = "Charlie"
inspector.vs.age = 35

# Batch update multiple attribute values
new_values = {
    'username': 'David',
    'age': 40,
    'active': False
}
for key, value in new_values.items():
    setattr(inspector.vs, key, value)
```

### Method 3: Listen to parameter change events
```python
# Listen to single parameter changes
inspector.paramChanged.connect(lambda name, value: print(f"Parameter {name} changed to: {value}"))

# Listen to all parameter changes
inspector.paramsChanged.connect(lambda params: print(f"All parameters updated: {params}"))

# Listen to specific parameter changes (using conditional checks)
def on_param_changed(name, value):
    if name == "username":
        print(f"Username changed to: {value}")
    elif name == "volume":
        print(f"Volume set to: {value}")
        # Add actual processing logic here
        update_audio_volume(value)

inspector.paramChanged.connect(on_param_changed)
```

## Common Questions

### 1. How to control component read-only state?
Use `readonly=True` parameter:
```python
MonoAttr("server_url", "https://api.example.com", readonly=True, label="Server Address")
```

### 2. How to add separators and blank spaces?
Use `separator=True` and `space=True` parameters:
```python
attrs = [
    MonoAttr("section1", "Part 1", title="Part 1"),
    MonoAttr("param1", "value1", label="Parameter 1"),
    MonoAttr("param2", "value2", label="Parameter 2", separator=True),  # Add separator line
    MonoAttr("section2", "Part 2", title="Part 2"),
    MonoAttr("param3", "value3", label="Parameter 3", space=True),     # Add top margin
]
```

### 3. How to handle parameter change events?
Use signal-slot mechanism to listen for parameter changes:
```python
# Listen to single parameter changes
inspector.paramChanged.connect(lambda name, value: print(f"Parameter {name} changed to: {value}"))

# Listen to all parameter changes
inspector.paramsChanged.connect(lambda params: print(f"All parameters updated: {params}"))

# Listen to specific parameter changes (using conditional checks)
def on_param_changed(name, value):
    if name == "username":
        print(f"Username changed to: {value}")
    elif name == "volume":
        print(f"Volume set to: {value}")
        # Add actual processing logic here
        update_audio_volume(value)

inspector.paramChanged.connect(on_param_changed)
```

## Example Application Description

The project contains multiple example files demonstrating various uses of MonoWidget:

- **main.py**: Basic example showing how to create simple parameter interfaces
- **debug_type_change_value.py**: Debug example showing parameter interfaces for various data types
- **inspector/**: Inspector-related modules containing implementations of all interface components
- **_utils/**: Utility modules containing various helper classes and components

You can view the basic example by running `main.py`, or refer to the source code of each module for more detailed implementations.