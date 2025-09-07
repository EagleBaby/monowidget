from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                            QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from mono import Mono
from .qmono_attr_item import QMonoAttrItem
import json


class QMonoInspector(QWidget):
    """参数检查器主窗口"""
    
    parameter_changed = pyqtSignal(str, object)  # 参数名, 新值
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mono = None
        self.attr_items = {}
        self._setup_ui()
        self._setup_timer()
        
    def _setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("MonoWidget - Parameter Inspector")
        self.setGeometry(100, 100, 400, 600)
        
        # 主布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 标题
        title = QLabel("Parameter Inspector")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll)
        
        # 滚动内容
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_content.setLayout(self.scroll_layout)
        scroll.setWidget(self.scroll_content)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self._save_config)
        button_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self._load_config)
        button_layout.addWidget(self.load_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self._reset_config)
        button_layout.addWidget(self.reset_btn)
        
        layout.addLayout(button_layout)
        
    def _setup_timer(self):
        """设置定时器用于参数变化检测"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._check_changes)
        self.timer.start(100)  # 100ms检查一次
        
    def set_mono(self, mono):
        """设置要检查的Mono对象"""
        self.mono = mono
        self._update_ui()
        
    def _update_ui(self):
        """更新UI显示"""
        # 清除现有项目
        for item in self.attr_items.values():
            item.setParent(None)
        self.attr_items.clear()
        
        if not self.mono:
            return
            
        # 获取所有属性
        attrs = []
        for attr_name in dir(self.mono):
            if not attr_name.startswith('_') and not callable(getattr(self.mono, attr_name)):
                attrs.append(attr_name)
                
        # 创建属性项
        for attr_name in sorted(attrs):
            attr_item = QMonoAttrItem(attr_name, getattr(self.mono, attr_name))
            attr_item.value_changed.connect(self._on_value_changed)
            self.scroll_layout.addWidget(attr_item)
            self.attr_items[attr_name] = attr_item
            
        # 添加弹簧
        self.scroll_layout.addStretch()
        
    def _on_value_changed(self, name, value):
        """处理属性值变化"""
        if self.mono:
            setattr(self.mono, name, value)
            self.parameter_changed.emit(name, value)
            
    def _check_changes(self):
        """检查外部对属性的修改"""
        if not self.mono:
            return
            
        for name, item in self.attr_items.items():
            current_value = getattr(self.mono, name)
            if current_value != item.get_value():
                item.set_value(current_value)
                
    def _save_config(self):
        """保存配置"""
        if not self.mono:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                config = {}
                for attr_name in dir(self.mono):
                    if not attr_name.startswith('_') and not callable(getattr(self.mono, attr_name)):
                        config[attr_name] = getattr(self.mono, attr_name)
                        
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                    
                QMessageBox.information(self, "Success", "Configuration saved successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")
                
    def _load_config(self):
        """加载配置"""
        if not self.mono:
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                for key, value in config.items():
                    if hasattr(self.mono, key):
                        setattr(self.mono, key, value)
                        
                self._update_ui()
                QMessageBox.information(self, "Success", "Configuration loaded successfully!")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")
                
    def _reset_config(self):
        """重置配置"""
        if not self.mono:
            return
            
        reply = QMessageBox.question(
            self, "Reset Configuration", 
            "Are you sure you want to reset all parameters to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 创建新的实例来重置
            new_mono = self.mono.__class__()
            
            # 复制属性值
            for attr_name in dir(self.mono):
                if not attr_name.startswith('_') and not callable(getattr(self.mono, attr_name)):
                    setattr(self.mono, attr_name, getattr(new_mono, attr_name))
                    
            self._update_ui()