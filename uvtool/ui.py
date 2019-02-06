import os, psutil
from uvtool import config, controls
from uvtool.tabs import daemon, power, undervolt
from PySide2.QtWidgets import QWidget, QMessageBox, QTabWidget, QVBoxLayout

class UVTool(QWidget):
    display_name_tooltips = {
        "CPU": "Undervolt the CPU cores.",
        "GPU":
"""Undervolt the onboard graphics processor, if present.
Note that certain desktop motherboards allow to disable the IGP entirely when an external GPU is present.""",
        "CPU Cache": "Undervolt the CPU cache.",
        "System Agent":
"""Undervolt the uncore, sometimes named "uncore".
It controls things such as the L3 cache, the memory controller and certain bus controllers.""",
    }

    def active_service_warning(self):
        service_warning = QMessageBox(self)
        service_warning.setIcon(QMessageBox.Warning)
        service_warning.setWindowTitle("Active service warning")
        service_warning.setText("The intel-undervolt service is active.")
        service_warning.setInformativeText(
"""Because the configuration will be overriden, applying those settings now is not recommended.
If your settings are unstable, this may cause your system to hang when starting the service on boot.
It is recommended to disable the service first.""")
        service_warning.exec_()

    def confirm_undervolt_apply(self):
        confirm = QMessageBox(self)
        confirm.setIcon(QMessageBox.Question)
        confirm.setWindowTitle("Confirm undervolt")
        confirm.setText(
"""APPLYING THOSE CHANGES MAY LEAD TO SYSTEM UNSTABILITY, DATA LOSS OR HARDWARE DAMAGE!
If you are not sure what you are doing, please cancel now!
Please review the generated configuration file.""")
        confirm.setInformativeText("Override \"{}\" and proceed?".format(config.config_path))
        confirm.setDetailedText("# Here follows the contents of the generated \"/etc/intel-undervolt.conf\" file:")
        confirm.setStandardButtons(QMessageBox.Apply | QMessageBox.Cancel)

        return confirm.exec_() == QMessageBox.Apply

    def confirm_settings_loss(self):
        confirm = QMessageBox(self)
        confirm.setIcon(QMessageBox.Question)
        confirm.setWindowTitle("Confirm settings loss")
        confirm.setText("Current changes were not saved.")
        confirm.setInformativeText("Continue anyway?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        return confirm.exec_() == QMessageBox.Yes
    
    def find_offset_tooltip(self, name):
        return self.display_name_tooltips[name] if name in self.display_name_tooltips else None

    def reload_ui_from_vars(self, new_vars=None):
        if not new_vars is None:
            # TODO: check if anything changed
            if not self.confirm_settings_loss():
                return
            
            self.vars = new_vars
        
        print("Reloading UI")
    
    def check_environment(self):
        self.has_systemd = False
        self.has_polkit = False

        for process in psutil.process_iter():
            if process.name() == "systemd":
                self.has_systemd = True
            elif process.name() == "polkitd":
                self.has_polkit = True

        print("polkitd: {}".format(self.has_polkit))
        print("systemd: {}".format(self.has_systemd))

    def __init__(self):
        QWidget.__init__(self)

        self.check_environment()
        self.has_systemd = False # unimplemented

        if os.geteuid() == 0:  # Root
            if self.has_polkit:
                warning = QMessageBox(self)
                warning.setIcon(QMessageBox.Warning)
                warning.setWindowTitle("Running as root")
                warning.setText("Running this tool as root is unnecessary because PolicyKit is present and will be used to prompt administrator rights.")
                warning.exec_()
        else:
            if not self.has_polkit:
                warning = QMessageBox(self)
                warning.setIcon(QMessageBox.Warning)
                warning.setWindowTitle("Polkit missing")
                warning.setText("PolicyKit is not present and the tool is not running as root, so certain actions will be impossible.")
                warning.exec_()

        self.can_admin = os.geteuid() == 0 or self.has_polkit

        self.vars = config.UVToolVars()

        self.setWindowTitle("intel-undervolt-qt")

        self.layout = QVBoxLayout()

        self.undervolt_tab = undervolt.TabUndervolt(self)
        self.power_tab = power.TabPower(self)
        self.daemon_tab = daemon.TabDaemon(self)

        # TODO implement those
        # TODO also disable Daemon and read+apply when the tool is missing, and disable the systemd service group when it cannot be used
        # self.power_tab.setEnabled(False)
        # self.daemon_tab.setEnabled(False)

        if not self.can_admin:
            self.daemon_tab.setEnabled(False)

        self.tab = QTabWidget()
        self.tab.addTab(self.undervolt_tab, "Undervolt")
        self.tab.addTab(self.power_tab, "Power")
        self.tab.addTab(self.daemon_tab, "Daemon")
        self.layout.addWidget(self.tab)

        self.layout.addWidget(controls.MainControls(self))

        self.setLayout(self.layout)