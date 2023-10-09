import subprocess
import requests

from pathlib import Path
from json import load
from zipfile import ZipFile

from get_platform.Platform import Platform
from get_resource_path.resource_path import resource_path


def download_webdriver(chome_version: str):
    urls: dict

    # Find webdriver version urls
    with open(resource_path('assets/webdriver.json'), "r") as f:
        json = load(f)
        for version in json['versions']:
            if version['version'] == chome_version:
                urls = version['downloads']

    # Find webdriver download url
    #   Get platfom string
    platform = Platform()
    if platform.platform == 'mac':
        platform = f'{platform.platform}-{platform.machine}'
    else:
        platform = platform.platform + platform.machine

    #   Find download platform url
    for platforms in urls['chromedriver']:
        if platforms['platform'] == platform:
            url = platforms['url']

    # Download file
    req = requests.get(url)
    with open(resource_path(f'assets/chromeDriver/{platform}.zip'), 'wb') as f:
        f.write(req.content)

    with ZipFile(resource_path(f'assets/chromeDriver/{platform}.zip')) as f:
        f.extract(f'chromedriver-{platform}/chromedriver',
                  resource_path(f'assets/chromeDriver'))
        subprocess.call(['chmod', 'u+x', resource_path(f'assets/chromeDriver')])
    return resource_path(f'assets/chromeDriver/chromedriver-{platform}/chromedriver')