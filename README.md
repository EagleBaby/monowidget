# MonoWidget

A Python tool for creating and managing parameter interfaces with automatic visual component generation.

## Features

- **Automatic UI Generation**: Generate visual interface components based on parameter definitions
- **Rich Data Types**: Support for strings, numbers, booleans, enums, lists, dicts, functions, datetime, and colors
- **Grouping & Organization**: Group parameters with headers and titles for better organization
- **Real-time Updates**: Listen to parameter changes with signal-slot mechanism
- **Customizable Interface**: Control read-only states, separators, and spacing
- **PyQt6 Integration**: Built on PyQt6 for modern and responsive interfaces

## Quick Start

### Installation

```bash
pip install monowidget
```

### Basic Usage

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from monowidget import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MonoWidget Example")
        
        # Create parameter definitions
        attrs = [
            MonoAttr("username", "Alice", label="Username"),
            MonoAttr("age", 30, range=(18, 100), label="Age"),
            MonoAttr("active", True, label="Active"),
            MonoAttr("theme", "dark", enum=["light", "dark", "auto"], label="Theme"),
        ]
        
        # Create Mono object and inspector
        mono = Mono(attrs)
        inspector = QMonoInspector(mono)
        
        # Add to layout
        layout = QVBoxLayout()
        layout.addWidget(inspector)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

## Documentation

- [English Documentation](README_EN.md)
- [中文文档](README_CN.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.