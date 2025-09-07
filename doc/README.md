# MonoWidget 文档

## 快速开始

### 1. 安装
```bash
pip install monowidget
```

### 2. 基本使用

#### 创建参数类
```python
from monowidget import Mono, MonoAttr
from monowidget.inspector import QMonoInspector

class MyApp(Mono):
    def __init__(self):
        super().__init__()
        self.name = "My Application"
        self.count = 10
        self.threshold = 0.5
        self.debug_mode = False
        self.output_path = "/tmp/output.txt"

# 使用示例
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    my_app = MyApp()
    inspector = QMonoInspector()
    inspector.set_mono(my_app)
    inspector.show()
    
    sys.exit(app.exec())
```

### 3. 支持的参数类型

- **布尔值**: `True`/`False`
- **整数**: `int` 类型
- **浮点数**: `float` 类型
- **字符串**: `str` 类型
- **列表**: `list` 类型
- **字典**: `dict` 类型

### 4. 高级功能

#### 保存和加载配置
```python
# 保存当前配置
inspector.save_config("config.json")

# 加载配置
inspector.load_config("config.json")
```

#### 参数变化监听
```python
def on_parameter_changed(name, value):
    print(f"参数 {name} 已更改为 {value}")

inspector.parameter_changed.connect(on_parameter_changed)
```

## API 参考

### Mono 类
基础参数容器类。

### MonoAttr 类
单个参数属性管理。

### QMonoInspector 类
Qt-based 参数可视化编辑器。

### QMonoAttrItemFactory 类
参数编辑器工厂类。