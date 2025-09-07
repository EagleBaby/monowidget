import sys
from PyQt6.QtWidgets import QApplication
from inspector import QMonoInspector
from mono import Mono, MonoAttr


class MyApp(Mono):
    def __init__(self):
        super().__init__()
        self.name = "My Application"
        self.version = "1.0.0"
        self.debug = False
        self.max_items = 100
        self.threshold = 0.75
        self.output_path = "/tmp/output.txt"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 创建应用实例
    my_app = MyApp()
    
    # 创建参数检查器
    inspector = QMonoInspector()
    inspector.set_mono(my_app)
    inspector.show()
    
    sys.exit(app.exec())