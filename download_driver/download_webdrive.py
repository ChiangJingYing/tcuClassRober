import subprocess
import requests

from pathlib import Path
from json import load
from zipfile import ZipFile

from get_platform.Platform import Platform
from get_resource_path.resource_path import resource_path


def download_webdriver(chome_version: str):
    urls: dict

    # Find webdriver download url
    #   Get platfom string
    platform = Platform()
    if platform.platform == 'mac':
        platform_full = f'{platform.platform}-{platform.machine}'
    else:
        platform_full = platform.platform + platform.machine

    url = f'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{".".join(chome_version.split(".")[:3])}.0/{platform_full}/chromedriver-{platform_full}.zip'

    # Download file
    req = requests.get(url)
    with open(resource_path(f'assets/chromeDriver/{platform_full}.zip'), 'wb') as f:
        f.write(req.content)

    with ZipFile(resource_path(f'assets/chromeDriver/{platform_full}.zip')) as f:
        if platform.platform == 'mac':
            f.extract(f'chromedriver-{platform_full}/chromedriver',
                    resource_path(f'assets/chromeDriver'))
            subprocess.call(['chmod', 'u+x', resource_path(f'assets/chromeDriver/chromedriver-{platform_full}/chromedriver')])
        elif platform.platform == 'win':
            f.extract(f'chromedriver-{platform_full}/chromedriver.exe',
                    resource_path(f'assets/chromeDriver'))
    return resource_path(f'assets/chromeDriver/chromedriver-{platform_full}/chromedriver')