from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, 
                            QComboBox, QTextEdit, QPushButton, QFileDialog, 
                            QSlider, QDateEdit, QTimeEdit, QDateTimeEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator, QDoubleValidator


class QMonoAttrItemFactory:
    """属性项工厂，根据数据类型创建合适的编辑控件"""
    
    @staticmethod
    def create_item(name, value, parent=None):
        """根据值类型创建合适的属性项"""
        if isinstance(value, bool):
            return QBoolItem(name, value, parent)
        elif isinstance(value, int):
            return QIntItem(name, value, parent)
        elif isinstance(value, float):
            return QFloatItem(name, value, parent)
        elif isinstance(value, str):
            if self._is_path_like(name):
                return QFilePathItem(name, value, parent)
            elif '\n' in value or len(value) > 100:
                return QTextItem(name, value, parent)
            else:
                return QStringItem(name, value, parent)
        elif isinstance(value, list):
            return QListItem(name, value, parent)
        elif isinstance(value, dict):
            return QDictItem(name, value, parent)
        else:
            return QStringItem(name, str(value), parent)
    
    @staticmethod
    def _is_path_like(name):
        """判断是否为路径类型的属性名"""
        path_keywords = ['path', 'file', 'dir', 'folder', 'directory', 'location']
        return any(keyword in name.lower() for keyword in path_keywords)


class QBaseItem(QWidget):
    """基础属性项"""
    
    value_changed = pyqtSignal(str, object)  # 属性名, 新值
    
    def __init__(self, name, value, parent=None):
        super().__init__(parent)
        self.name = name
        self.value = value
        self._setup_ui()
        
    def _setup_ui(self):
        """设置基础UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 属性名称
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.name_label)
        
    def get_value(self):
        """获取当前值"""
        raise NotImplementedError
        
    def set_value(self, value):
        """设置值"""
        raise NotImplementedError


class QBoolItem(QBaseItem):
    """布尔类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(value)
        self.checkbox.stateChanged.connect(lambda: self.value_changed.emit(self.name, self.checkbox.isChecked()))
        self.layout().addWidget(self.checkbox)
        
    def get_value(self):
        return self.checkbox.isChecked()
        
    def set_value(self, value):
        self.checkbox.setChecked(bool(value))


class QIntItem(QBaseItem):
    """整数类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        self.spinbox = QSpinBox()
        self.spinbox.setRange(-999999, 999999)
        self.spinbox.setValue(value)
        self.spinbox.valueChanged.connect(lambda: self.value_changed.emit(self.name, self.spinbox.value()))
        self.layout().addWidget(self.spinbox)
        
    def get_value(self):
        return self.spinbox.value()
        
    def set_value(self, value):
        self.spinbox.setValue(int(value))


class QFloatItem(QBaseItem):
    """浮点数类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        
        # 创建水平布局
        h_layout = QHBoxLayout()
        
        # 双精度旋转框
        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(-999999.0, 999999.0)
        self.spinbox.setDecimals(6)
        self.spinbox.setValue(value)
        self.spinbox.valueChanged.connect(lambda: self.value_changed.emit(self.name, self.spinbox.value()))
        h_layout.addWidget(self.spinbox)
        
        # 滑块
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(int(value * 100))
        self.slider.valueChanged.connect(lambda: self._on_slider_changed())
        h_layout.addWidget(self.slider)
        
        self.layout().addLayout(h_layout)
        
    def _on_slider_changed(self):
        """滑块值变化处理"""
        value = self.slider.value() / 100.0
        self.spinbox.setValue(value)
        
    def get_value(self):
        return self.spinbox.value()
        
    def set_value(self, value):
        self.spinbox.setValue(float(value))
        self.slider.setValue(int(float(value) * 100))


class QStringItem(QBaseItem):
    """字符串类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        self.lineedit = QLineEdit()
        self.lineedit.setText(str(value))
        self.lineedit.textChanged.connect(lambda: self.value_changed.emit(self.name, self.lineedit.text()))
        self.layout().addWidget(self.lineedit)
        
    def get_value(self):
        return self.lineedit.text()
        
    def set_value(self, value):
        self.lineedit.setText(str(value))


class QTextItem(QBaseItem):
    """文本类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        self.textedit = QTextEdit()
        self.textedit.setText(str(value))
        self.textedit.textChanged.connect(lambda: self.value_changed.emit(self.name, self.textedit.toPlainText()))
        self.layout().addWidget(self.textedit)
        
    def get_value(self):
        return self.textedit.toPlainText()
        
    def set_value(self, value):
        self.textedit.setText(str(value))


class QFilePathItem(QBaseItem):
    """文件路径类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        
        # 创建水平布局
        h_layout = QHBoxLayout()
        
        self.lineedit = QLineEdit()
        self.lineedit.setText(str(value))
        self.lineedit.textChanged.connect(lambda: self.value_changed.emit(self.name, self.lineedit.text()))
        h_layout.addWidget(self.lineedit)
        
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self._browse_file)
        h_layout.addWidget(self.browse_btn)
        
        self.layout().addLayout(h_layout)
        
    def _browse_file(self):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.lineedit.setText(file_path)
            
    def get_value(self):
        return self.lineedit.text()
        
    def set_value(self, value):
        self.lineedit.setText(str(value))


class QListItem(QBaseItem):
    """列表类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        
        # 创建垂直布局
        v_layout = QVBoxLayout()
        
        # 列表显示
        self.textedit = QTextEdit()
        self.textedit.setPlainText('\n'.join(map(str, value)))
        self.textedit.textChanged.connect(lambda: self.value_changed.emit(self.name, self._parse_list()))
        v_layout.addWidget(self.textedit)
        
        self.layout().addLayout(v_layout)
        
    def _parse_list(self):
        """解析文本为列表"""
        text = self.textedit.toPlainText()
        return [line.strip() for line in text.split('\n') if line.strip()]
        
    def get_value(self):
        return self._parse_list()
        
    def set_value(self, value):
        self.textedit.setPlainText('\n'.join(map(str, value)))


class QDictItem(QBaseItem):
    """字典类型属性项"""
    
    def __init__(self, name, value, parent=None):
        super().__init__(name, value, parent)
        
        # 创建垂直布局
        v_layout = QVBoxLayout()
        
        # 字典显示
        self.textedit = QTextEdit()
        import json
        self.textedit.setPlainText(json.dumps(value, indent=2, ensure_ascii=False))
        self.textedit.textChanged.connect(lambda: self.value_changed.emit(self.name, self._parse_dict()))
        v_layout.addWidget(self.textedit)
        
        self.layout().addLayout(v_layout)
        
    def _parse_dict(self):
        """解析文本为字典"""
        try:
            import json
            return json.loads(self.textedit.toPlainText())
        except:
            return {}
            
    def get_value(self):
        return self._parse_dict()
        
    def set_value(self, value):
        import json
        self.textedit.setPlainText(json.dumps(value, indent=2, ensure_ascii=False))