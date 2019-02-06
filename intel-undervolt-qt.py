#!/usr/bin/python3

import uvtool.ui, sys
from PySide2.QtWidgets import QApplication

app = QApplication(sys.argv)

widget = uvtool.ui.UVTool()
#widget.resize(800, 600)
widget.show()

app.exec_()