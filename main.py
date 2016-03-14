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
            url_link = format_link(link)
            print("URL LINK ", url_link)
            r = requests.get(ROOT.format(url_link))
            if r.status_code is not 200:
                raise NetworkError
            print(r.text)
        except NetworkError:
            #log the eroor?
            return None

def format_link(link):
    'properly format link to create a valid wikipedia url'

    return link.rstrip().title().replace(" ", "_")


if __name__ == '__main__':
    #find_links('raw.md')
    check_link('Algorithm')
