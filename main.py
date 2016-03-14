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
        url_link = format_link(link)
        return


    if "|" in link:
        # a wiki link has the following strucutre:
        # actual link | name_on_screen
        # so we are inteested in the actual link only
        link_parts = link.split("|")
        try:
            assert len(link_parts) == 2
        except AssertionError:
            # log the error
            return None
        url_link = format_link(link_parts[0])

    try:


        print("URL LINK ", url_link)
        r = requests.get(ROOT.format(url_link))
        print(ROOT.format(url_link))
        if r.status_code is not 200:
           raise NetworkError
        if r.startswith("#REDIRECT"):
            pass
        # redirect
    except NetworkError:
        #log the eroor?
        return None

def connect(url_link):
    redirect = True
    try:
        while redirect:

            print("URL LINK ", url_link)
            r = requests.get(ROOT.format(url_link))
            print(ROOT.format(url_link))
            if r.status_code is not 200:
               raise NetworkError
            text = r.text
            if text.startswith("#REDIRECT"):
                url_link = re.findall('\[\[(.*?)\]\]', text)[0]

            else:
                redirect = False
            # redirect
    except NetworkError:
            #log the eroor?
        return None
    print(text)
    return text


def format_link(link):
    'properly format link to create a valid wikipedia url'

    return link.rstrip().title().replace(" ", "_")


if __name__ == '__main__':
    #all_links = find_links('raw.md')
    #check_link('Algorithm')
    # list(map(check_link, all_links[:12]))
    connect('Stable_Marriage_Problem')
