config_path = "/etc/intel-undervolt.conf"

class UVToolVars():
    def __init__(self):
        self.offsets = {
            0: ("CPU", 0),
            1: ("GPU", 0),
            2: ("CPU Cache", 0),
            3: ("System Agent", 0),
            4: ("Analog I/O", 0)
        }

        self.short_term_power_limit = None
        self.long_term_power_limit = None
        self.short_term_time_window = None
        self.long_term_time_window = None

        self.tjunction_offset = 0

        self.daemon_interval = 5000