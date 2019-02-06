from uvtool import config
from PySide2.QtWidgets import QWidget, QBoxLayout, QFileDialog, QMessageBox, QPushButton
from PySide2.QtGui import QIcon

class MainControls(QWidget):
    def on_import(self):
        # TODO: if changes are present, ask if it's okay to override

        dialog = QFileDialog(self.tool)
        dialog.selectFile(config.config_path)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setFileMode(QFileDialog.ExistingFile)
        path = dialog.exec()

    def on_read(self):
        pass  #TODO

    def on_apply(self):
        # TODO: warning if systemd service is active...

        self.tool.active_service_warning()

        if self.tool.confirm_undervolt_apply():
            info = QMessageBox(self.tool)
            info.setIcon(QMessageBox.Information)
            info.setWindowTitle("Undervolt applied")
            info.setText(
"""The undervolt appears to be successful.
As a reminder, even if your system is stable now, it is not unlikely that you encounter a hang or data corruption later (even during idle).
If your system hangs, you may have to power cycle it forcefully.
It is recommended to run a stress test like mprime for a couple hours in order to check the system stability.
Finally, you may want to press the "Read current" button in the tool in order to check the exact applied undervolt.""")

            info.exec_()

    def __init__(self, tool):
        QWidget.__init__(self)

        self.tool = tool

        self.layout = QBoxLayout(QBoxLayout.LeftToRight)

        self.reset_button = QPushButton()
        self.reset_button.setText("Defaults")
        self.reset_button.setIcon(QIcon.fromTheme("document-revert"))
        self.reset_button.clicked.connect(lambda: tool.reload_ui_from_vars(config.UVToolVars()))
        self.layout.addWidget(self.reset_button)

        self.import_button = QPushButton()
        self.import_button.setText("Load")
        self.import_button.setIcon(QIcon.fromTheme("document-open"))
        self.import_button.clicked.connect(self.on_import)
        self.layout.addWidget(self.import_button)

        self.export_button = QPushButton()
        self.export_button.setText("Save")
        self.export_button.setIcon(QIcon.fromTheme("document-save-as"))
        self.layout.addWidget(self.export_button)

        self.read_button = QPushButton()
        self.read_button.setText("Read")
        self.read_button.setIcon(QIcon.fromTheme("computer"))
        self.read_button.setToolTip(
"""Read values currently set on the CPU.
This is useful to get accurate values after applying custom settings.""")
        self.read_button.clicked.connect(self.on_read)
        self.layout.addWidget(self.read_button)

        self.apply_button = QPushButton()
        self.apply_button.setText("Apply")
        self.apply_button.setToolTip(
"""Save the current settings to "{}" and apply.
This will override the existing configuration file.""".format(config.config_path))
        self.apply_button.setStyleSheet("QPushButton:!disabled { background-color: red }")
        self.apply_button.clicked.connect(self.on_apply)
        self.layout.addWidget(self.apply_button)

        self.setLayout(self.layout)