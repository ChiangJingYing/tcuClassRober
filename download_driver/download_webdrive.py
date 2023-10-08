import subprocess
import requests

from pathlib import Path
from json import load
from zipfile import ZipFile

from get_platform.Platform import Platform

def download_webdriver(chome_version: str):
    urls: dict

    # Find webdriver version urls
    with open(Path.cwd().joinpath('enviornment_check/webdriver.json'), "r") as f:
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
    with open(Path.cwd().joinpath(f'assets/chromeDriver/{platform}.zip'), 'wb') as f:
        f.write(req.content)

    with ZipFile(Path.cwd().joinpath(f'assets/chromeDriver/{platform}.zip')) as f:
        f.extract(f'chromedriver-{platform}/chromedriver',
                  Path.cwd().joinpath(f'assets/chromeDriver'))
        subprocess.call(['chmod', 'u+x', Path.cwd().joinpath(f'assets/chromeDriver')])
    return Path.cwd().joinpath(f'assets/chromeDriver/chromedriver-{platform}/chromedriver').absolute()