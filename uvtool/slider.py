from PySide2.QtWidgets import QWidget, QLabel, QDoubleSpinBox, QSlider, QGridLayout
from PySide2.QtCore import Qt

class Slider():
    def update_offset(self, pos):
        offset = round(pos, 2)
        return offset

    def __init__(self, tool, text, tooltip, precision, minimal, maximal, interval):
        self.tool = tool

        self.scale = precision

        self.name_label = QLabel(text)
        self.name_label.setAlignment(Qt.AlignLeft)

        if not tooltip == None:
            self.name_label.setToolTip(tooltip)

        self.offset_edit = QDoubleSpinBox()
        self.offset_edit.setRange(minimal, maximal)
        self.offset_edit.setSingleStep(precision)
        self.offset_edit.setDecimals(2)
        self.offset_edit.setAlignment(Qt.AlignRight)
        self.offset_edit.valueChanged.connect(lambda pos: self.slider.setSliderPosition(self.update_offset(pos) / self.scale))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(minimal / self.scale, maximal)
        self.slider.setTickInterval(interval / self.scale)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.valueChanged.connect(lambda pos: self.offset_edit.setValue(self.update_offset(pos * self.scale)))

        self.update_offset(0)

class SliderGrid(QWidget):
    def __init__(self, tool, sliders):
        QWidget.__init__(self)
        self.tool = tool
        self.sliders = sliders

        layout = QGridLayout()
        layout.setColumnMinimumWidth(1, 300)
        layout.setColumnMinimumWidth(2, 100)

        for n, slider in enumerate(sliders):
            layout.addWidget(slider.name_label, n, 0)
            layout.addWidget(slider.slider, n, 1)
            layout.addWidget(slider.offset_edit, n, 2)
        
        self.setLayout(layout)