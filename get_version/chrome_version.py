import plistlib
import subprocess

from pathlib import Path

from get_platform.Platform import Platform


def get_chrome_version() -> (bool, str):
    system_platform = Platform().platform

    if system_platform == "win":
        try:
            chrome_version = subprocess.check_output(
                ['wmic', 'datafile', 'where', 'name="C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe"', 'get', 'Version']).decode('utf-8').strip()
            return 1, chrome_version
        except subprocess.CalledProcessError:
            return 0, "Chrome not found on Windows"

    elif system_platform == "mac":  # macOS
        try:
            chrome_version = subprocess.check_output(
                ['mdfind', 'kMDItemCFBundleIdentifier=="com.google.Chrome"']).decode('utf-8').strip()
            chrome_version = Path(chrome_version)
            chrome_info_plist = chrome_version/'Contents/Info.plist'

            if chrome_info_plist.exists():
                with open(chrome_info_plist, 'rb') as info_plist:
                    plist = plistlib.load(info_plist)
                    return 1, plist.get('CFBundleShortVersionString', 'Version not found')
            else:
                return "Chrome not found on macOS"
        except subprocess.CalledProcessError:
            return 0, "Chrome not found on macOS"

    else:
        return 0, "Unsupported operating system"
