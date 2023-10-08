from get_version.chrome_version import get_chrome_version
from download_driver.download_webdrive import download_webdriver


class Webdriver_Path:
    def __init__(self) -> None:
        chrome_version = get_chrome_version()
        print(f"Google Chrome Version: {chrome_version}")
        self.webdriver_path = download_webdriver(chrome_version[1])
        print(self.webdriver_path)


# Webdriver_Path()
