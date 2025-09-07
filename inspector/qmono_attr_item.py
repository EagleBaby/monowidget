from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, 
                            QComboBox, QTextEdit, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class QMonoAttrItem(QWidget):
    """单个属性编辑项"""
    
    value_changed = pyqtSignal(str, object)  # 属性名, 新值
    
    def __init__(self, name, value, parent=None):
        super().__init__(parent)
        self.name = name
        self.value = value
        self._setup_ui()
        self._set_value(value)
        
    def _setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 属性名称标签
        name_label = QLabel(self.name)
        name_font = QFont()
        name_font.setBold(True)
        name_label.setFont(name_font)
        layout.addWidget(name_label)
        
        # 值编辑控件
        self.value_widget = self._create_value_widget()
        layout.addWidget(self.value_widget)
        
    def _create_value_widget(self):
        """根据值的类型创建合适的编辑控件"""
        if isinstance(self.value, bool):
            widget = QCheckBox()
            widget.stateChanged.connect(lambda: self._on_value_changed(widget.isChecked()))
            return widget
            
        elif isinstance(self.value, int):
            widget = QSpinBox()
            widget.setRange(-999999, 999999)
            widget.valueChanged.connect(lambda: self._on_value_changed(widget.value()))
            return widget
            
        elif isinstance(self.value, float):
            widget = QDoubleSpinBox()
            widget.setRange(-999999.0, 999999.0)
            widget.setDecimals(6)
            widget.valueChanged.connect(lambda: self._on_value_changed(widget.value()))
            return widget
            
        elif isinstance(self.value, str):
            if '\n' in str(self.value) or len(str(self.value)) > 50:
                widget = QTextEdit()
                widget.textChanged.connect(lambda: self._on_value_changed(widget.toPlainText()))
                return widget
            else:
                widget = QLineEdit()
                widget.textChanged.connect(lambda: self._on_value_changed(widget.text()))
                return widget
                
        elif isinstance(self.value, list):
            widget = QComboBox()
            widget.addItems([str(item) for item in self.value])
            widget.currentTextChanged.connect(lambda: self._on_value_changed(widget.currentText()))
            return widget
            
        else:
            widget = QLineEdit(str(self.value))
            widget.textChanged.connect(lambda: self._on_value_changed(widget.text()))
            return widget
            
    def _on_value_changed(self, new_value):
        """处理值变化"""
        self.value = new_value
        self.value_changed.emit(self.name, new_value)
        
    def get_value(self):
        """获取当前值"""
        return self.value
        
    def set_value(self, value):
        """设置值"""
        self.value = value
        self._set_value(value)
        
    def _set_value(self, value):
        """设置控件值"""
        widget = self.value_widget
        
        if isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))
        elif isinstance(widget, QSpinBox):
            widget.setValue(int(value))
        elif isinstance(widget, QDoubleSpinBox):
            widget.setValue(float(value))
        elif isinstance(widget, QLineEdit):
            widget.setText(str(value))
        elif isinstance(widget, QTextEdit):
            widget.setText(str(value))
        elif isinstance(widget, QComboBox):
            index = widget.findText(str(value))
            if index >= 0:
                widget.setCurrentIndex(index)