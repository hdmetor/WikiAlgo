import requests
import re

ROOT = "https://en.wikipedia.org/w/index.php?title={}&action=raw"

def find_links(page):
    with open(page, 'r') as fp:
        s = fp.read()
    return re.findall('\[\[(.*?)\]\]', s)

def check_link(link):
    if "#" in link:
        # this specific algo seem not to have a page for itlsef, so we can skip that
        return None
    if "|" not in link:
        # there is no alternate name in the link
        try:
            r = requests.get('https://api.github.com/user'


if __name__ == '__main__':
    find_links('raw.md')
