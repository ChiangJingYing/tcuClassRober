import platform

class Platform:
    def __init__(self):
        self.platform = platform.system()
        self.machine = platform.machine().capitalize().lower()

        if self.platform == 'Darwin':
            self.platform = 'mac'
        elif self.platform == 'Windows':
            self.platform = 'win'

        if self.machine == 'x86-64' and self.platform == 'mac':
            self.machine = 'x64'
        elif self.machine == 'amd64' and self.platform == 'win':
            self.machine = '64'