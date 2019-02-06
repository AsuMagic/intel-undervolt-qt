from uvtool import slider
from PySide2.QtWidgets import QWidget, QBoxLayout, QGroupBox

class PowerDurationControls(QWidget):
    def __init__(self, tool):
        QWidget.__init__(self)
        self.tool = tool



class PowerControls(QWidget):
    def __init__(self, tool):
        QWidget.__init__(self)
        self.tool = tool

        self.layout = QBoxLayout(QBoxLayout.TopToBottom)

        self.sliders = [
            slider.Slider(self.tool, "Short term TDP", "Maximal TDP in the short term", 1, 1, 150, 5),
            slider.Slider(self.tool, "Long term TDP", "Maximal TDP in the long term", 1, 1, 150, 5)
        ]

        self.slider_grid = slider.SliderGrid(self.tool, self.sliders)
        self.layout.addWidget(self.slider_grid)

        self.duration_controls = PowerDurationControls(self.tool)
        duration_group = QGroupBox("Override power limit durations")
        duration_group.setCheckable(True)
        duration_group.setToolTip(
"""If checked, allows you to alter short term and long term package power limit durations.
This is used for Turbo Boost.""")
        duration_group.setLayout(self.duration_controls.layout())
        self.layout.addWidget(duration_group)

        self.setLayout(self.layout)

class TabPower(QWidget):
    def __init__(self, tool):
        QWidget.__init__(self)
        self.tool = tool

        self.layout = QBoxLayout(QBoxLayout.TopToBottom)

        self.tjunction_offset = slider.SliderGrid(
            self.tool,
            [slider.Slider(self.tool, "TJunction offset", "Offsets the temperature from which the CPU throttles", 1, -120, 0, 5)])
        self.layout.addWidget(self.tjunction_offset)

        self.power_controls = PowerControls(self.tool)
        power_group = QGroupBox("Override power limits")
        power_group.setCheckable(True)
        power_group.setLayout(self.power_controls.layout)
        self.layout.addWidget(power_group)

        self.setLayout(self.layout)