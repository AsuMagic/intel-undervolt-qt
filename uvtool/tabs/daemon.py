from PySide2.QtWidgets import QWidget, QBoxLayout, QPushButton, QSpinBox, QLabel, QGroupBox
from PySide2.QtCore import Qt

class SystemdControls(QWidget):
    def __init__(self, tool):
        QWidget.__init__(self)

        self.tool = tool

        self.layout = QBoxLayout(QBoxLayout.LeftToRight)

        self.start_toggle_button = QPushButton()
        self.start_toggle_button.setText("Start")
        self.layout.addWidget(self.start_toggle_button)

        self.enable_toggle_button = QPushButton()
        self.enable_toggle_button.setText("Enable")
        self.enable_toggle_button.setStyleSheet("QPushButton:!disabled { background-color: orange }")
        self.layout.addWidget(self.enable_toggle_button)

        self.setLayout(self.layout)

class DaemonIntervalControls(QWidget):
    def __init__(self, tool):
        QWidget.__init__(self)

        self.tool = tool

        self.layout = QBoxLayout(QBoxLayout.LeftToRight)

        self.layout.addWidget(QLabel("Update interval: "))

        self.period_select = QSpinBox()
        self.period_select.setRange(100, 1000 * 60 * 240)  # 240 seconds max
        self.period_select.setSingleStep(100)
        self.layout.addWidget(self.period_select)

        self.layout.addWidget(QLabel("ms"))

        self.layout.setStretch(1, 1)

        self.setLayout(self.layout)

class TabDaemon(QWidget):
    def __init__(self, tool):
        QWidget.__init__(self)

        self.tool = tool

        self.layout = QBoxLayout(QBoxLayout.TopToBottom)

        self.info_label = QLabel(
"""The system sometimes overrides the power and temperature limits.
The intel-undervolt daemon can be used to enforce them periodically.
Enabling the systemd service enables you to apply your settings on boot.""")
        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)

        self.layout.addWidget(DaemonIntervalControls(self.tool))

        systemd_group = QGroupBox("systemd service")
        self.systemd_controls = SystemdControls(self.tool)
        systemd_group.setLayout(self.systemd_controls.layout)
        systemd_group.setEnabled(self.tool.has_systemd)
        self.layout.addWidget(systemd_group)

        self.setLayout(self.layout)
