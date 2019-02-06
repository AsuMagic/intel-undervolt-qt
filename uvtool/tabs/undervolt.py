from uvtool import slider
from PySide2.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel

class TabUndervolt(QWidget):
    def __init__(self, tool):
        QWidget.__init__(self)

        self.tool = tool

        self.sliders = [slider.Slider(
            self.tool,
            text=name,
            tooltip=self.tool.find_offset_tooltip(name),
            precision=0.01,
            minimal=-200,
            maximal=0,
            interval=10) for i, (name, default) in self.tool.vars.offsets.items()]

        self.slider_grid = slider.SliderGrid(self.tool, self.sliders)
        
        for i in range(len(self.sliders)):
            self.slider_grid.layout().addWidget(QLabel("mV"), i, 3)  # wtf why layout()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.slider_grid)

        self.setLayout(self.layout)