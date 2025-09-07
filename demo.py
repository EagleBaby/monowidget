import sys
from PyQt6.QtWidgets import QApplication
from inspector import QMonoInspector
from mono import Mono, MonoAttr


class ImageProcessor(Mono):
    def __init__(self):
        super().__init__()
        self.input_path = "/path/to/image.jpg"
        self.output_path = "/path/to/output.jpg"
        self.brightness = 1.0
        self.contrast = 1.0
        self.saturation = 1.0
        self.sharpness = 1.0
        self.blur_radius = 0.0
        self.rotation_angle = 0.0
        self.flip_horizontal = False
        self.flip_vertical = False
        self.resize_width = 800
        self.resize_height = 600
        self.quality = 95
        self.format = "JPEG"
        self.grayscale = False
        self.sepia = False


class DataAnalyzer(Mono):
    def __init__(self):
        super().__init__()
        self.data_file = "/path/to/data.csv"
        self.output_file = "/path/to/results.csv"
        self.separator = ","
        self.encoding = "utf-8"
        self.header_row = 0
        self.skip_rows = 0
        self.max_rows = None
        self.columns_to_analyze = ["col1", "col2", "col3"]
        self.statistical_methods = ["mean", "median", "std"]
        self.plot_type = "line"
        self.plot_title = "Data Analysis Results"
        self.plot_xlabel = "X Axis"
        self.plot_ylabel = "Y Axis"
        self.save_plots = True
        self.show_plots = False


class TextGenerator(Mono):
    def __init__(self):
        super().__init__()
        self.prompt = "Once upon a time"
        self.max_length = 100
        self.temperature = 0.8
        self.top_p = 0.9
        self.frequency_penalty = 0.0
        self.presence_penalty = 0.0
        self.stop_sequences = ["\n", ".", "!", "?"]
        self.model_name = "gpt-3.5-turbo"
        self.output_file = "/path/to/generated_text.txt"
        self.save_to_file = True
        self.show_in_console = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 创建示例应用
    image_processor = ImageProcessor()
    data_analyzer = DataAnalyzer()
    text_generator = TextGenerator()
    
    # 创建参数检查器
    inspector = QMonoInspector()
    inspector.set_mono(image_processor)  # 默认显示图像处理器
    inspector.show()
    
    print("MonoWidget Demo Application Started")
    print("Available demo classes:")
    print("- ImageProcessor: Image processing parameters")
    print("- DataAnalyzer: Data analysis parameters")
    print("- TextGenerator: Text generation parameters")
    
    sys.exit(app.exec())