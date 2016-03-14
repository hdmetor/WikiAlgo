import re
import os
import json
import logging
import requests
from collections import namedtuple

logger = logging.getLogger(__name__)

ROOT = "https://en.wikipedia.org/w/index.php?title={}&action=raw"
DATA_FOLDER = 'data'
if not os.path.isdir(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def find_links(text, total=True):
    if not text:
        return None
    all_links = re.findall('\[\[(.*?)\]\]', text)
    #print(all_links)
    if total:
        return len(all_links)
    else:
        return (clean_link(link) for link in all_links if clean_link(link))

def clean_link(link):

    if "#" in link:
        # this specific algo seem not to have a page for itlsef, so we can skip that
        return None
    if "|" not in link:
        # there is no alternate name in the link
        url_link = format_link(link)
    if "|" in link:
        # a wiki link has the following strucutre:
        # actual link | name_on_screen
        # so we are inteested in the actual link only
        link_parts = link.split("|")
        try:
            assert len(link_parts) == 2
        except AssertionError:
            logger.debug('[WikiMarkDownSchemaError] {}'.format(link))
            return None
        url_link = format_link(link_parts[0])
    return url_link

def find_text(url_link):

    # reading the local cache
    local_path = build_local_path(url_link)
    if os.path.exists(local_path):
        return read_local(local_path)
    redirect = True
    try:
        while redirect and url_link:
            r = requests.get(ROOT.format(url_link))
            if r.status_code is not 200:
                raise requests.ConnectionError
            text = r.text
            if text.startswith("#REDIRECT"):
                url_link = clean_link(re.findall('\[\[(.*?)\]\]', text)[0])

            else:
                redirect = False
    except requests.ConnectionError:
        logger.debug('[ConnectionError] {}'.format(url_link))
        return None
    if url_link:
        save_local(local_path, text)
        return text
    else:
        return None

def build_local_path(url_link, folder=DATA_FOLDER):
    return os.path.join(DATA_FOLDER, url_link)

def save_local(path, text):
    with open(path, 'wt') as fp:
        fp.write(text)

def read_local(path):
    with open(path, 'rt') as fp:
        text = fp.read()
    return text

def format_link(link):
    'properly format link to create a valid wikipedia url'
    return link.rstrip().replace(" ", "_").replace("&minus;", "-")


if __name__ == '__main__':

    seed_text = find_text("List_of_algorithms")
    all_links = find_links(seed_text, total=False)
    print('Gathering data...')

    data = {\
        k: {
            "text_len" : len(find_text(k)),
            "links" : find_links(find_text(k)) \
            } for k in list(all_links) if k and find_links(find_text(k), total=True)}

    print('Saving {} items'.format(len(data)))

    with open('final.json' , 'w') as fp:
        json.dump(data, fp)

    print('Saved')
